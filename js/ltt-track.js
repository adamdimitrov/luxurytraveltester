/*
 * ltt-track.js: carry the Google Ads click ID into Travelpayouts (Booking.com) links.
 *
 * 1. On landing, store gclid / wbraid / gbraid from the URL for 90 days (cookie + localStorage).
 * 2. Rewrite every tp.media link's marker "404154.<placement>" into
 *    "404154.<placement>_GC_<hex(gclid)>" (WB_ for wbraid, GB_ for gbraid).
 *
 * Travelpayouts SubIDs may only contain letters, digits and "_", while click IDs
 * contain "-", so the click ID is hex-encoded. scripts/sync_travelpayouts_conversions.py
 * decodes it from the booking's sub_id and uploads the sale to Google Ads.
 * Visitors without a click ID (organic, crawlers) keep the static links untouched.
 */
(function () {
  var KEY = '_ltt_click';
  var DAYS = 90;
  var TYPES = { gclid: 'GC', wbraid: 'WB', gbraid: 'GB' };

  function readStored() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) {
        var o = JSON.parse(raw);
        if (o && o.t && o.v && o.exp > Date.now()) return o;
      }
    } catch (e) {}
    var m = document.cookie.match(new RegExp('(?:^|; )' + KEY + '=([^;]*)'));
    if (m) {
      var parts = decodeURIComponent(m[1]).split('|');
      if (parts.length === 2 && TYPES[parts[0]]) return { t: parts[0], v: parts[1] };
    }
    return null;
  }

  function store(t, v) {
    var exp = Date.now() + DAYS * 864e5;
    try { localStorage.setItem(KEY, JSON.stringify({ t: t, v: v, exp: exp })); } catch (e) {}
    document.cookie = KEY + '=' + encodeURIComponent(t + '|' + v) +
      '; expires=' + new Date(exp).toUTCString() + '; path=/; SameSite=Lax; Secure';
  }

  function capture() {
    var params;
    try { params = new URLSearchParams(location.search); } catch (e) { return readStored(); }
    for (var t in TYPES) {
      var v = params.get(t);
      if (v && /^[A-Za-z0-9_-]{10,}$/.test(v)) { store(t, v); return { t: t, v: v }; }
    }
    return readStored();
  }

  function hex(s) {
    var out = '';
    for (var i = 0; i < s.length; i++) out += ('0' + s.charCodeAt(i).toString(16)).slice(-2);
    return out;
  }

  var click = capture();
  if (!click) return;
  var suffix = '_' + TYPES[click.t] + '_' + hex(click.v);

  function decorate(a) {
    if (!a || !a.href || a.href.indexOf('tp.media/r') === -1) return;
    try {
      var url = new URL(a.href);
      var marker = url.searchParams.get('marker');
      if (!marker || /_(GC|WB|GB)_[0-9a-f]+$/.test(marker)) return;
      var dot = marker.indexOf('.');
      var base = dot === -1 ? marker : marker.slice(0, dot);
      var sub = dot === -1 ? 'ltt' : marker.slice(dot + 1).replace(/[^A-Za-z0-9_]/g, '_');
      url.searchParams.set('marker', base + '.' + sub + suffix);
      a.href = url.toString();
    } catch (e) {}
  }

  function decorateAll() {
    var links = document.querySelectorAll('a[href*="tp.media/r"]');
    for (var i = 0; i < links.length; i++) decorate(links[i]);
  }

  // Catch links added later and any click that beats the initial pass.
  ['mousedown', 'touchstart', 'keydown', 'click'].forEach(function (ev) {
    document.addEventListener(ev, function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a') : null;
      decorate(a);
    }, true);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', decorateAll);
  } else {
    decorateAll();
  }
})();
