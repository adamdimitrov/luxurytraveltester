#!/usr/bin/env python3
"""
Upload Booking.com sales (via Travelpayouts) that came from Google Ads clicks
to Google Ads as offline purchase conversions, valued at our commission.

How the click ID gets here: js/ltt-track.js rewrites tp.media markers to
"404154.<placement>_GC_<hex(gclid)>" (WB_ = wbraid, GB_ = gbraid). Travelpayouts
returns that as the booking's sub_id in its statistics API.

Same Google Ads upload path as cruisedetective/sync_tiqets_conversions.py
(Data Manager API events:ingest), but a SEPARATE conversion action so hotel
sales never mix with Tiqets sales.

Env (read from luxurytraveltester/.env, then cruisedetective/.env for shared Google creds):
  TRAVELPAYOUTS_API_TOKEN               Travelpayouts -> Profile -> API token
  GOOGLE_ADS_PALM_CONVERSION_ACTION_ID  conversion action for Booking sales (required)
  GOOGLE_ADS_CLIENT_ID / _CLIENT_SECRET / _REFRESH_TOKEN / _CUSTOMER_ID
  GMAIL_CLIENT_ID / _CLIENT_SECRET / _REFRESH_TOKEN, ALERT_EMAIL (optional email alert)

Usage:
  python3 scripts/sync_travelpayouts_conversions.py            # sync last 45 days
  python3 scripts/sync_travelpayouts_conversions.py --dry-run  # print, upload nothing
  python3 scripts/sync_travelpayouts_conversions.py --validate # Google validateOnly upload
"""
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATHS = [
    os.path.join(REPO_DIR, '.env'),
    os.path.join(os.path.dirname(REPO_DIR), 'cruisedetective', '.env'),
]
STATE_FILE = os.path.join(REPO_DIR, 'scripts', 'uploaded_travelpayouts_actions.json')
BOOKING_CAMPAIGN_ID = 84
LOOKBACK_DAYS = 45
TP_API = 'https://api.travelpayouts.com/statistics/v1'
CLICK_RE = re.compile(r'_(GC|WB|GB)_([0-9a-f]+)$')
CLICK_TYPES = {'GC': 'gclid', 'WB': 'wbraid', 'GB': 'gbraid'}

DRY_RUN = '--dry-run' in sys.argv
VALIDATE_ONLY = '--validate' in sys.argv


def load_env():
    env = {}
    for path in reversed(ENV_PATHS):  # first path wins
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.startswith(('GOOGLE_', 'TRAVELPAYOUTS_', 'GMAIL_', 'ALERT_'))})
    return env


ENV = load_env()


def http_json(url, data=None, headers=None, method=None):
    body = json.dumps(data).encode() if isinstance(data, (dict, list)) else data
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def decode_click(sub_id):
    """'.palm_hub_cta_x_GC_4a6b...' -> {'type': 'gclid', 'value': ..., 'placement': ...}"""
    if not sub_id:
        return None
    sub = sub_id.lstrip('.')
    m = CLICK_RE.search(sub)
    if not m:
        return None
    try:
        value = bytes.fromhex(m.group(2)).decode('ascii')
    except ValueError:
        return None
    if not re.fullmatch(r'[A-Za-z0-9_-]{10,}', value):
        return None
    return {'type': CLICK_TYPES[m.group(1)], 'value': value, 'placement': sub[:m.start()]}


# ---------- Travelpayouts ----------

def tp_headers():
    token = ENV.get('TRAVELPAYOUTS_API_TOKEN')
    if not token:
        sys.exit('Missing TRAVELPAYOUTS_API_TOKEN (Travelpayouts -> Profile -> API token) in .env')
    return {'X-Access-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'}


def tp_profit_field():
    """Pick the commission field the API offers for Booking (unconfirmed vs confirmed)."""
    data = http_json(f'{TP_API}/get_fields_list?campaign_id={BOOKING_CAMPAIGN_ID}', headers=tp_headers())
    names = {f['name'] for f in data.get('fields', [])}
    for candidate in ('profit_eur', 'processing_profit_eur', 'paid_profit_eur'):
        if candidate in names:
            return candidate, names
    sys.exit(f'No EUR profit field in Travelpayouts fields list: {sorted(names)}')


def tp_fetch_actions():
    profit_field, names = tp_profit_field()
    fields = ['action_id', 'sub_id', 'price_eur', profit_field, 'state', 'created_at', 'updated_at']
    if profit_field != 'paid_profit_eur' and 'paid_profit_eur' in names:
        fields.append('paid_profit_eur')
    since = (datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)).strftime('%Y-%m-%d')
    rows, offset = [], 0
    while True:
        query = {
            'fields': fields,
            'filters': [
                {'field': 'type', 'op': 'eq', 'value': 'action'},
                {'field': 'campaign_id', 'op': 'eq', 'value': BOOKING_CAMPAIGN_ID},
                {'field': 'date', 'op': 'ge', 'value': since},
            ],
            'sort': [{'field': 'date', 'order': 'asc'}],
            'offset': offset,
            'limit': 1000,
        }
        data = http_json(f'{TP_API}/execute_query', data=query, headers=tp_headers(), method='POST')
        batch = data.get('results', [])
        rows.extend(batch)
        offset += len(batch)
        if not batch or offset >= int(data.get('total_rows', 0)):
            break
    return rows, profit_field


def commission(row, profit_field):
    for key in ('paid_profit_eur', profit_field):
        try:
            v = float(row.get(key) or 0)
        except (TypeError, ValueError):
            v = 0.0
        if v > 0:
            return round(v, 2)
    return 0.0


# ---------- Google ----------

def google_token(prefix='GOOGLE_ADS'):
    data = urllib.parse.urlencode({
        'client_id': ENV.get(f'{prefix}_CLIENT_ID', ''),
        'client_secret': ENV.get(f'{prefix}_CLIENT_SECRET', ''),
        'refresh_token': ENV.get(f'{prefix}_REFRESH_TOKEN', ''),
        'grant_type': 'refresh_token',
    }).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())['access_token']


def upload(row, click, value, token):
    action_id = ENV.get('GOOGLE_ADS_PALM_CONVERSION_ACTION_ID')
    customer_id = ENV.get('GOOGLE_ADS_CUSTOMER_ID', '').replace('-', '')
    if not action_id or not customer_id:
        sys.exit('Missing GOOGLE_ADS_PALM_CONVERSION_ACTION_ID or GOOGLE_ADS_CUSTOMER_ID in .env')
    created = (row.get('created_at') or '').strip()
    try:
        ts = datetime.strptime(created, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    payload = {
        'destinations': [{
            'operatingAccount': {'accountType': 'GOOGLE_ADS', 'accountId': customer_id},
            'productDestinationId': action_id,
        }],
        'events': [{
            'eventName': 'purchase',
            'eventTimestamp': ts,
            'eventSource': 'WEB',
            'conversionValue': value,
            'currency': 'EUR',
            'transactionId': 'TP-' + str(row['action_id']),
            'adIdentifiers': {click['type']: click['value']},
        }],
        'validateOnly': VALIDATE_ONLY,
    }
    try:
        res = http_json('https://datamanager.googleapis.com/v1/events:ingest', data=payload,
                        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                        method='POST')
        return True, res.get('requestId', '')
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        if 'ALREADY_EXISTS' in err:
            return True, 'duplicate'
        return False, f'{e.code} {err[:300]}'


def email_alert(lines):
    if not (ENV.get('GMAIL_CLIENT_ID') and ENV.get('GMAIL_REFRESH_TOKEN')):
        return
    to = ENV.get('ALERT_EMAIL') or ENV.get('GMAIL_USER')
    if not to:
        return
    msg = MIMEText('\n'.join(lines), 'plain', 'utf-8')
    msg['Subject'] = f'Palm hotels: {len(lines)} Google Ads booking update(s)'
    msg['To'] = to
    try:
        token = google_token('GMAIL')
        http_json('https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
                  data={'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()},
                  headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                  method='POST')
    except Exception as e:  # alerts must never block the sync
        print(f'[EMAIL ERROR] {e}')


# ---------- main ----------

def main():
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)

    rows, profit_field = tp_fetch_actions()
    print(f'Travelpayouts: {len(rows)} Booking.com actions in the last {LOOKBACK_DAYS} days (profit field: {profit_field})')

    token, alerts, changed = None, [], False
    for row in rows:
        aid = str(row.get('action_id'))
        click = decode_click(row.get('sub_id'))
        if not click:
            continue  # organic booking
        st = (row.get('state') or '').lower()
        value = commission(row, profit_field)
        prev = state.get(aid)

        if st in ('canceled', 'cancelled'):
            if prev and prev.get('uploaded') and not prev.get('cancel_noted'):
                alerts.append(f'CANCELLED after upload: {aid} ({click["placement"]}) EUR {prev.get("value")}. '
                              'Google Ads still counts it; retract manually if it skews ROAS.')
                prev['cancel_noted'] = True
                changed = True
            continue
        if prev and prev.get('uploaded'):
            continue

        line = f'{aid} | {st} | booking EUR {row.get("price_eur")} | commission EUR {value} | {click["placement"]} | {click["type"]}'
        if DRY_RUN:
            print('[DRY RUN]', line)
            continue
        if value <= 0:
            print('[SKIP no commission yet]', line)
            continue
        token = token or google_token()
        ok, info = upload(row, click, value, token)
        print('[UPLOADED]' if ok else '[ERROR]', line, info)
        if ok and not VALIDATE_ONLY:
            state[aid] = {'uploaded': True, 'value': value, 'at': datetime.now(timezone.utc).isoformat()}
            alerts.append('New Google Ads hotel booking: ' + line)
            changed = True

    if changed:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    if alerts:
        email_alert(alerts)


if __name__ == '__main__':
    main()
