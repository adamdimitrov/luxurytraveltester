#!/usr/bin/env python3
"""
Build the single-winner "verdict" pages from the three hub listicles.

  /best-helicopter-tour-new-york   pick: HeliNY (#2 in the hub, chosen on purpose)
  /best-desert-safari-dubai        pick: Excursion Point (#1 in the hub)
  /best-palm-jumeirah-hotel-dubai  pick: Atlantis, The Palm (#1 in the hub)

Each page reuses its hub's <head>, navbar, footer and runtime scripts, and swaps
the <main> content for a short verdict article (format ported from the
thecruisedetective.com /best-* verdict pages; styles in verdict_page_styles.css).
Ratings, prices, times and anchors are read live from the hub's cards, so the
verdict never drifts from the verified card data. Re-run after editing a hub:

    python3 scripts/build_verdict_pages.py
"""
import html as H
import json
import os
import re

from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://luxurytraveltester.com'
CDN = '/assets/cdn/67d02edca7795b0f57073b59/'
DATE_ISO = '2026-11-12'
DATE_TXT = 'Nov 12, 2026'
AVATAR = CDN + '67d02edca7795b0f57073f57_Adam-dimitrov-portrait-75x75.webp'

EXTRA_CSS = """
.review-article{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:17px;line-height:1.7;color:#334155}
.review-article p{margin:0 0 1rem}
.review-article ul{padding-left:1.2rem}
.adv-page-container{margin-top:1.5rem}
.adv-content-img{width:100%;height:auto;border-radius:12px;margin:.5rem 0 1rem;display:block}
.adv-hero-image{width:100%;height:auto;display:block}
.adv-compare .ltt-tested{display:inline-block;margin-top:4px;font-size:11px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#166534;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:999px;padding:1px 8px}
.adv-compare .bpa-summary-reviews{margin-top:4px}
.adv-tldr-box .bpa-summary-reviews{margin:.25rem 0 .5rem}
.adv-video{position:relative;width:100%;padding-top:56.25%;border-radius:12px;overflow:hidden;margin:.5rem 0 1.25rem;background:#0f172a}
.adv-table-note{font-size:14px;color:#64748b;margin:-.75rem 0 1.5rem}
.adv-cta-btn{display:block;text-align:center;text-decoration:none;padding:1rem 1.5rem;margin:1rem 0}
@media (max-width:600px){.adv-facts{grid-template-columns:1fr}.adv-page-container{padding:0 16px}}
"""


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def esc(s):
    return H.escape(s, quote=True)


# ---------------------------------------------------------------- tracking --
def gyg(url, cmp):
    """Same GetYourGuide product + partner id, verdict-specific campaign tag."""
    url = H.unescape(url)
    return re.sub(r'cmp=[^&"]*', 'cmp=' + cmp, url)


def tp(url, placement):
    """Travelpayouts link with a verdict placement (letters, digits, _ only)."""
    url = H.unescape(url)
    return re.sub(r'marker=404154\.[A-Za-z0-9_]+', 'marker=404154.' + placement, url)


def retag(fragment, fn):
    """Rewrite every affiliate href inside a fragment (rating popovers)."""
    def sub(m):
        href = H.unescape(m.group(1))
        return 'href="' + esc(fn(href)) + '"'
    return re.sub(r'href="([^"]+)"', sub, fragment)


# ------------------------------------------------------------- card data ---
def cards(hub_html):
    soup = BeautifulSoup(hub_html, 'html.parser')
    out = {}
    for c in soup.select('#ltt-cards-deck .bpa-card'):
        t = c.select_one('.bpa-title')
        rate = c.select_one('.bpa-summary-reviews')
        sub = c.select_one('.bpa-sublink')
        out[c['id']] = {
            'href': t['href'],
            'rating': str(rate) if rate else '',
            'price': c.select_one('.bpa-price').get_text(' ', strip=True),
            'anchor': sub['href'] if sub else '',
            'imgs': [i.get('data-src') or i.get('src') for i in c.select('.bpa-slider img')],
        }
    return out


# ----------------------------------------------------------- page pieces ---
def img(src, alt, eager=False):
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="{esc(src)}" alt="{esc(alt)}" class="adv-content-img" {load}/>'


def cta(href, label, big=False):
    style = ' style="font-size: 1.25rem; padding: 1.25rem 2rem;"' if big else ''
    return (f'<a href="{esc(href)}" class="adv-cta-btn" target="_blank" '
            f'rel="nofollow sponsored noopener"{style}>{label}</a>')


def table(rows, hub):
    body = []
    for r in rows:
        name = f'<strong>{r["name"]}</strong>'
        if r.get('winner'):
            name = f'<strong>🏆 {r["name"]}</strong>'
        else:
            name = f'<a href="/{hub}{r["anchor"]}">{name}</a>'
        tested = '<br><span class="ltt-tested">✓ Tested in person</span>' if r.get('tested') else ''
        cls = ' class="is-winner"' if r.get('winner') else ''
        body.append(
            f'<tr{cls}><td>{name}<br><small>{r["meta"]}</small>{tested}{r["rating"]}</td>'
            f'<td>{r["price"]}</td><td>{r["best"]}</td><td>{r["con"]}</td></tr>')
    return ('<div class="adv-table-wrap"><table class="adv-compare"><thead><tr>'
            f'<th>{rows[0]["col"]}</th><th>Price</th><th>Best for</th><th>Main drawback</th>'
            '</tr></thead><tbody>' + ''.join(body) + '</tbody></table></div>')


def faq_html(faqs):
    items = []
    for i, (q, a) in enumerate(faqs):
        op = ' open' if i == 0 else ''
        items.append(f'<details{op}><summary>{q}</summary><p>{a}</p></details>')
    return '<div class="adv-faq">' + ''.join(items) + '</div>'


def article(p):
    feats = ''.join(
        f'<h3 class="adv-feature-subhead">{i}. {f["h"]}</h3>' + f['body']
        for i, f in enumerate(p['features'], 1))
    cons = ''.join(f'<li><strong>{a}</strong> {b}</li>' for a, b in p['cons'])
    facts = ''.join(f'<div><span>{a}</span><strong>{b}</strong><em>{c}</em></div>' for a, b, c in p['facts'])
    return f'''
<div class="adv-page-container">
  <article class="review-article">
    <div class="ltt-top-bar">
      <nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
        <a href="/">Home</a><span class="ltt-bc-sep">›</span><a href="/{p['hub']}">{p['hub_label']}</a><span class="ltt-bc-sep">›</span><span class="ltt-bc-current" aria-current="page">{p['crumb']}</span>
      </nav>
      <span class="ltt-hero-kicker-badge">✓ Field-Tested Verdict</span>
    </div>
    <h1 class="ltt-editorial-h1 adv-headline">{p['h1']} <span class="ltt-h1-muted">{p['h1_muted']}</span></h1>
    <div class="ltt-trust-bar">
      <div class="ltt-author-cluster">
        <div class="ltt-author-avatar-wrap"><img alt="Adam Dimitrov" class="ltt-author-avatar" src="{AVATAR}" width="42" height="42"/></div>
        <div class="ltt-author-meta">
          <div class="ltt-author-line">By <a href="/about">Adam Dimitrov</a>, Founder &amp; Lead Field Inspector</div>
          <div class="ltt-author-role">{p['role']}</div>
        </div>
      </div>
      <div class="ltt-trust-pills"><span class="ltt-trust-pill"><strong>Last updated</strong>: {DATE_TXT}</span></div>
    </div>

    <div class="adv-hero-image-container">
      <img src="{esc(p['hero'])}" alt="{esc(p['hero_alt'])}" class="adv-hero-image" fetchpriority="high" loading="eager" width="800" height="500"/>
      <p class="adv-image-caption">{p['hero_caption']}</p>
    </div>

    <div class="article-body">
      <div class="adv-tldr-box">
        <p><strong>⏱️ TL;DR:</strong> {p['tldr']}</p>
        {p['rating']}
        <div class="adv-facts">{facts}</div>
        {cta(p['link']('tldr'), p['cta_top'])}
      </div>

      <div class="adv-pickskip">
        <div class="adv-pick"><strong>✓ Book it if</strong> {p['pick']}</div>
        <div class="adv-skip"><strong>✕ Skip it if</strong> {p['skip']}</div>
      </div>

      {p['intro']}

      <h2 class="adv-section-title" id="compare" style="scroll-margin-top:80px">{p['compare_h2']}</h2>
      {table(p['rows'], p['hub'])}
      {p.get('table_note', '')}

      <h2 class="adv-section-title">{p['why_h2']}</h2>
      {p['why']}

      <div class="adv-expanded-features">{feats}</div>

      <h2 class="adv-section-title">What I Didn't Love</h2>
      <ul class="adv-feature-list adv-cons">{cons}</ul>

      {cta(p['link']('middle'), p['cta_mid'])}

      <h2 class="adv-section-title">Quick Questions</h2>
      {faq_html(p['faqs'])}

      <div class="adv-final-box">
        <h3>{p['final_h3']}</h3>
        <p>{p['final']}</p>
        {cta(p['link']('bottom'), p['cta_bottom'], big=True)}
        <p class="adv-secure-tag">{p['secure']}</p>
      </div>
    </div>
  </article>
</div>
'''


def schema(p):
    url = f'{SITE}/{p["slug"]}'
    strip = lambda s: re.sub(r'<[^>]+>', '', s)
    graph = [
        {'@type': 'Article', '@id': url + '#article', 'headline': strip(p['h1'] + ' ' + p['h1_muted']),
         'description': p['desc'], 'image': SITE + p['hero'], 'datePublished': DATE_ISO,
         'dateModified': DATE_ISO, 'mainEntityOfPage': url, 'inLanguage': 'en',
         'author': {'@type': 'Person', 'name': 'Adam Dimitrov', 'url': SITE + '/about'},
         'publisher': {'@type': 'Organization', 'name': 'Luxury Travel Tester', 'url': SITE + '/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': p['hub_label'], 'item': f'{SITE}/{p["hub"]}'},
            {'@type': 'ListItem', 'position': 3, 'name': p['crumb'], 'item': url}]},
        {'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': strip(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}}
            for q, a in p['faqs']]},
    ]
    return ('<script id="ltt-schema-jsonld" type="application/ld+json">'
            + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
            + '</script>')


def build(p):
    src = read(p['hub'] + '/index.html')
    head_end = src.index('</head>')
    head = src[:head_end]
    url = f'{SITE}/{p["slug"]}'
    title = p['title']

    def meta(attr, key, val):
        nonlocal head
        pat = re.compile(r'<meta content="[^"]*" %s="%s"/>' % (attr, re.escape(key)))
        new = f'<meta content="{esc(val)}" {attr}="{key}"/>'
        head, n = pat.subn(lambda m: new, head)
        if not n:
            head += new

    head = re.sub(r'<title>[^<]*</title>', lambda m: f'<title>{esc(title)}</title>', head)
    meta('name', 'description', p['desc'])
    meta('property', 'og:title', title)
    meta('property', 'og:description', p['desc'])
    meta('property', 'og:image', SITE + p['hero'])
    meta('property', 'og:url', url)
    meta('name', 'twitter:title', title)
    meta('name', 'twitter:description', p['desc'])
    meta('name', 'twitter:image', SITE + p['hero'])
    head = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', head)
    head = re.sub(r'<link as="image"[^>]*/?>', '', head)  # hub hero preloads
    head = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', head, flags=re.S)
    css = read('scripts/verdict_page_styles.css') + EXTRA_CSS
    head += (f'<link href="{url}" rel="canonical"/>'
             f'<link rel="preload" as="image" href="{esc(p["hero"])}" fetchpriority="high"/>'
             f'<style id="ltt-verdict-styles">{css}</style>\n')

    main_open = '<main id="main" role="main">'
    i_main = src.index(main_open, head_end) + len(main_open)
    nav_js = re.search(r'<script id="ltt-nav-script">.*?</script>', src[i_main:], re.S).group(0)
    body_top = src[head_end:i_main] + '\n' + nav_js

    i_foot = src.index('<section class="footer-dark">', i_main)
    i_foot_end = src.index('</section>', i_foot) + len('</section>')
    footer = src[i_foot:i_foot_end]
    i_main_end = src.index('</main>', i_foot_end)
    runtime = ''.join(re.findall(r'<script[^>]*src="[^"]*(?:jquery|webflow)[^"]*"[^>]*></script>',
                                 src[i_foot_end:i_main_end]))
    after = src[i_main_end + len('</main>'):]
    after = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', after, flags=re.S)
    after = re.sub(r'<script id="bpa-slider-perf-runtime">.*?</script>', '', after, flags=re.S)
    extra_js = '<script defer src="/js/ltt-yt.js"></script>' if 'ltt-yt' in p['why'] + str(p['features']) else ''
    out = (head + body_top + article(p) + footer + runtime + '</main>' + extra_js
           + schema(p) + after)
    # nav/footer: the verdict page is not the hub, so drop the hub's "current" markers
    out = out.replace('aria-current="page" ', '').replace(' w--current', '')
    out = out.replace('class="ltt-mega-item active"', 'class="ltt-mega-item"').replace('class="ltt-nav-link active"', 'class="ltt-nav-link"')
    os.makedirs(os.path.join(ROOT, p['slug']), exist_ok=True)
    with open(os.path.join(ROOT, p['slug'], 'index.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    print('wrote', p['slug'], len(out))


# =============================================================== HELI ======
def heli():
    hub = 'best-helicopter-tours-new-york'
    c = cards(read(hub + '/index.html'))
    win = c['card-2']
    link = lambda slot: gyg(win['href'], 'heli-verdict-' + slot)
    rate = lambda cid, key: retag(c[cid]['rating'], lambda u: gyg(u, 'heli-verdict-reviews-' + key) if 'getyourguide' in u else u)
    hy = lambda n: CDN + {
        1: '6a47daf594f0a6341fe351db_best-helicopter-tours-nyc-heliny-1.avif',
        2: '6a47daf7e7a9ec87627f2a43_best-helicopter-tours-nyc-heliny-2.avif',
        5: '6a47dd8fbfa2dfc7559687ec_best-helicopter-tours-nyc-heliny-5_result.avif',
        12: '6a47daf5c9ff2d5bf8d7508d_best-helicopter-tours-nyc-heliny-12.avif',
        13: '6a47daf5e65c811a8d65cb83_best-helicopter-tours-nyc-heliny-13.avif',
        15: '6a47daf70dd18fd3b6f5cc27_best-helicopter-tours-nyc-heliny-15.avif',
        18: '6a47daf78ebd68066b64c4a1_best-helicopter-tours-nyc-heliny-18.avif',
    }[n]
    col = 'Tour'
    rows = [
        dict(col=col, winner=True, tested=True, name='HeliNY Manhattan Sightseeing Tour', meta='12 to 30 min, Pier 6 Manhattan',
             rating=rate('card-2', 'heliny'), price='From $272', best='First-timers who want an easy, all-in flight from Manhattan',
             con='Closed windows can cause reflections in photos'),
        dict(col=col, tested=True, name='FlyNYON Doors-Off', anchor=c['card-1']['anchor'], meta='16 or 30 min, Kearny NJ',
             rating=rate('card-1', 'flynyon'), price='From $149/seat + fees', best='Doors-off shoe selfies and night flights',
             con='Terminal in New Jersey, fees added at checkout'),
        dict(col=col, name='Charm Aviation', anchor=c['card-3']['anchor'], meta='12 to 30 min, Pier 6 Manhattan',
             rating=rate('card-3', 'charm'), price='From $272', best='A backup from the same heliport if HeliNY is sold out',
             con='Does not fly on Sundays'),
        dict(col=col, name='Zip Aviation', anchor=c['card-4']['anchor'], meta='15 to 30 min, Pier 6 Manhattan',
             rating=rate('card-4', 'zip'), price='From $269', best='Statue of Liberty and skyline routes',
             con='Pre-recorded narration, a $40 boarding fee can apply'),
        dict(col=col, name='Wings Air Private for Couples', anchor=c['card-5']['anchor'], meta='30 to 45 min, Westchester',
             rating=rate('card-5', 'wings'), price='From $995 per couple', best='A private flight for two',
             con='$35 airport fee each, far from Manhattan'),
    ]
    a = lambda cid, text: f'<a href="/{hub}{c[cid]["anchor"]}">{text}</a>'
    return dict(
        slug='best-helicopter-tour-new-york', hub=hub, hub_label='NYC Helicopter Tours', crumb='Best Helicopter Tour',
        title='Best Helicopter Tour in New York (2026): I Flew the 2 Most Popular',
        desc='I flew FlyNYON and HeliNY myself. For most visitors HeliNY from Pier 6 in Manhattan is the one to book: heliport fees included, 12 to 30 minutes, from $272.',
        h1="I Flew New York's 2 Most Popular Helicopter Tours.", h1_muted="Here's the One Most Visitors Should Book.",
        role='2 Most Popular Companies Flown in Person • Day &amp; Night Flights • 100% Self-Funded',
        hero=hy(1), hero_alt='The HeliNY helicopter on the pad at the Downtown Manhattan Heliport',
        hero_caption='The HeliNY helicopter at the Downtown Manhattan Heliport. My photo from the test flight.',
        tldr='I spent a month in New York and booked the two most popular helicopter companies myself: FlyNYON (doors off, from New Jersey) and HeliNY (closed doors, from Manhattan). <strong>HeliNY</strong> is the one I recommend for most visitors: you board at Pier 6 in Lower Manhattan, 5 minutes on foot from the subway, the heliport fees are already in the price and you can cancel for free up to 24 hours before.',
        rating=rate('card-2', 'heliny'),
        facts=[('Price', 'From $272', 'per person, heliport fees included'),
               ('Duration', '12 to 30 min', 'three route lengths to choose from'),
               ('Heliport', 'Pier 6, Manhattan', '5-minute walk from South Ferry station'),
               ('Cancellation', 'Free', 'up to 24 hours before')],
        link=link, cta_top='CHECK DATES FROM $272 →', cta_mid='SEE AVAILABLE TIMES FROM $272 →', cta_bottom='CHECK DATES &amp; BOOK →',
        pick='it is your first helicopter flight over New York, you are staying in Manhattan, or you want one price with no fees added at checkout.',
        skip=f'you want the doors-off shoe selfie (pick {a("card-1", "FlyNYON")}, from $149 per seat plus fees) or a private flight for two (pick {a("card-5", "Wings Air from Westchester")}, from $995 per couple).',
        intro='<p>Every New York helicopter company promises the Statue of Liberty and the Manhattan skyline, and the prices look alike until the fees appear at checkout. The real differences are where you take off, whether the doors are on and what you end up paying. So I booked and flew the <strong>two most popular companies</strong> myself: FlyNYON at night with the doors off, and HeliNY by day in a closed cabin.</p>'
              f'<p>I judged the logistics, the route, the cabin, the commentary and the value for money. Below is the short version: which one I recommend, why, and when another tour is the better pick for you. The full reviews and all my photos are in <a href="/{hub}">my complete NYC helicopter tour ranking</a>.</p>',
        compare_h2='How the 5 NYC Helicopter Tours in My Ranking Compare', rows=rows,
        table_note='<p class="adv-table-note">I flew HeliNY and FlyNYON myself. Charm Aviation, Zip Aviation and Wings Air are compared from their current GetYourGuide listings.</p>',
        why_h2='Why HeliNY Is the One I Would Book',
        why='<p>To be honest, FlyNYON gave me the bigger thrill: dangling my legs out of an open door over Manhattan at night is hard to beat. But it is also the harder flight to reach, and the price you see is not the price you pay. HeliNY is the tour I would send a friend on for a first trip: <strong>easier to reach, simpler to book and priced all-in</strong>. Here is what I found.</p>',
        features=[
            dict(h='You Board in Manhattan, No Trip to New Jersey', body=img(hy(15), 'Helicopters on the pads at the Downtown Manhattan Heliport, Pier 6')
                 + '<p>The Downtown Manhattan Heliport at <strong>Pier 6 is a 5-minute walk from the South Ferry subway station</strong>. Check-in was quick: a security check, the waiver and the safety video, then my bags went into a locker. The helipads are right next to the terminal, so there is no shuttle van to wait for.</p>'
                 + img(hy(18), 'The HeliNY check-in area inside the Downtown Manhattan Heliport terminal')
                 + '<p>FlyNYON flies from Kearny, New Jersey. I needed a train and then an Uber, and a freight train blocking the road nearly made me late for check-in.</p>'),
            dict(h='One Price, Heliport Fees Included', body='<p>On GetYourGuide HeliNY starts at <strong>$272 per person with the heliport fees already included</strong>, and you can cancel for free up to 24 hours before. FlyNYON starts at $149 per seat for 16 minutes and $330 for 30 minutes, but fees are added at checkout.</p>'),
            dict(h='Three Route Lengths, All Past the Statue of Liberty', body=img(hy(5), 'The Statue of Liberty seen from the HeliNY helicopter')
                 + '<p>Every route circles the <strong>Statue of Liberty and Ellis Island</strong> and passes Battery Park, Wall Street and One World Trade Center:</p>'
                 + '<ul class="adv-feature-list"><li><strong>12 to 15 minutes:</strong> the harbor loop with the essentials.</li><li><strong>17 to 20 minutes:</strong> continues up the Hudson for Midtown and the southern edge of Central Park. This is the most popular choice.</li><li><strong>25 to 30 minutes:</strong> the full length of Manhattan, up to the George Washington Bridge and Yankee Stadium.</li></ul>'
                 + img(hy(12), 'Midtown Manhattan and the Hudson River seen from the HeliNY helicopter')),
            dict(h='A Closed Cabin With Live Pilot Narration', body=img(hy(13), 'Adam Dimitrov in the HeliNY helicopter wearing a headset')
                 + '<p>The doors stay closed, so nobody needs a harness and the flight works in any weather. You wear a <strong>headset with live English narration from the pilot</strong>. It is the calmer choice if open doors make you nervous, or in winter, when an open door can make it too cold to enjoy.</p>'
                 + img(hy(2), 'A HeliNY staff member photographing passengers in front of the helicopter before boarding')
                 + '<p>Right before boarding, the staff take a photo of each group in front of the helicopter.</p>'),
        ],
        cons=[('The cabin got hot on my flight.', 'I flew during a June heat wave and the air conditioning blew cold air straight at me. With the closed cabin, I felt motion sick by the halfway mark. If you get motion sick easily, keep this in mind.'),
              ('Closed windows can cause reflections.', 'Hold your phone close to the glass for cleaner photos.'),
              ('No doors-off shoe selfie.', 'That is what FlyNYON is for.'),
              ('The group photo costs extra.', 'Digital copies of the pre-flight photos were $40.'),
              ('Bags go in a locker.', 'You cannot take them on board.')],
        faqs=[('How long is the flight?', 'You choose 12 to 15, 17 to 20 or 25 to 30 minutes. The 17 to 20 minute route is the most popular, because it adds Midtown and the edge of Central Park to the harbor loop.'),
              ('Where do I board?', 'At the Downtown Manhattan Heliport, Pier 6, a 5-minute walk from the South Ferry subway station. The helipads are next to the terminal, with no shuttle.'),
              ('Are the fees included?', 'Yes. The GetYourGuide listing includes the heliport fees. The only extra I paid for was the optional $40 photo package.'),
              ('What times does it fly?', 'On the GetYourGuide calendar for Saturday 14 November 2026: 12 to 15 minute flights every 30 minutes from 10:30 to 18:30, 17 to 20 minutes from 10:00 to 15:30, and 25 to 30 minutes at 10:00, 12:00, 12:30 and 16:00. Times change by season.'),
              ('HeliNY or FlyNYON?', 'HeliNY for an easy closed-door flight from Manhattan with the fees included. FlyNYON for a doors-off or night flight from New Jersey, from $149 per seat plus fees.')],
        final_h3='My pick for your NYC helicopter tour',
        final='HeliNY from Pier 6 in Downtown Manhattan. If your budget allows, take the 17 to 20 minute route to see Midtown, not just the harbor.',
        secure='🔒 Instant mobile ticket • Free cancellation up to 24 hours • Secure checkout via GetYourGuide',
        callout='my one-pick verdict: the NYC helicopter tour most visitors should book',
    )


# ============================================================= DESERT ======
def desert():
    hub = 'best-desert-safaris-dubai'
    c = cards(read(hub + '/index.html'))
    win = c['card-1']
    link = lambda slot: gyg(win['href'], 'desert-verdict-' + slot)
    rate = lambda cid, key: retag(c[cid]['rating'], lambda u: gyg(u, 'desert-verdict-reviews-' + key))
    im = lambda f: CDN + f
    spec = [
        ('card-1', 'Excursion Point Red Dunes Safari', '4 to 7 h, Al Lahbab red dunes', 'A full first safari with dinner and shows', 'Only 2 soft drinks included, alcohol extra'),
        ('card-2', 'Funtours Morning Safari', '4 to 7 h, Lahbab desert', 'A morning safari, back before lunch', 'No dinner or camp on the 4-hour tour'),
        ('card-3', 'OceanAir Al Khayma Camp', '4 to 7 h, red dunes', 'The most-reviewed safari, with shisha and BBQ', 'No stargazing or telescopes'),
        ('card-4', 'Ammar Tours Quad Safari', '4 to 7 h, Lahbab red sand', 'The cheapest way to add a 35-min self-drive quad', 'Quad bikes only, no dune buggy'),
        ('card-5', 'Platinum Heritage Land Rover', '7 h, Desert Conservation Reserve', 'Vintage Land Rovers, falconry and a 4-course dinner', 'No dune bashing, highest price'),
        ('card-6', 'Noble Life Camp', '6 h, Al Marmoom desert', 'Fire and dance shows, VIP seating option', 'Buffet, not a served dinner'),
        ('card-7', 'Odyssey Sunrise Safari', '4 h, Dubai Desert Reserve', 'Sunrise, oryx feeding and a picnic breakfast', 'Pickup around 04:15'),
        ('card-8', 'Dream Journey Red Dunes', '4 h, Lahbab dunes', 'A short safari with 45 min of dune bashing', 'No dinner'),
    ]
    rows = []
    for i, (cid, name, meta, best, con) in enumerate(spec):
        rows.append(dict(col='Safari', winner=i == 0, tested=True, name=name, anchor=c[cid]['anchor'], meta=meta,
                         rating=rate(cid, cid.replace('card-', 's')),
                         price=c[cid]['price'].replace(' | per person', ''), best=best, con=con))
    a = lambda cid, text: f'<a href="/{hub}{c[cid]["anchor"]}">{text}</a>'
    return dict(
        slug='best-desert-safari-dubai', hub=hub, hub_label='Dubai Desert Safaris', crumb='Best Desert Safari',
        title='Best Desert Safari in Dubai (2026): I Tested 8, This One Won',
        desc="I tested 8 Dubai desert safaris in person. Excursion Point's red dunes safari won: dune bashing, sandboarding, a camel ride and a BBQ dinner with shows, from €29.",
        h1='I Tested 8 Desert Safaris in Dubai.', h1_muted="Here's the One Worth Your Money.",
        role='8 Desert Safaris Tested in Person • Every Camp Photographed • 100% Self-Funded',
        hero=im('68bc785d7ec299de43630344_6870b32641b42598b411e2d9_5915AF38-AD32-4A54-9558-275305769954_1_105_c_result.webp'),
        hero_alt='The lounge area of the desert camp at sunset on the Excursion Point safari',
        hero_caption='The camp lounge at sunset on my Excursion Point safari. My photo from the test tour.',
        tldr="I booked 8 of the most popular desert safaris in Dubai and did them one by one. <strong>Excursion Point's Desert Safari, Camel Ride, Quad Bike &amp; BBQ Dinner</strong> is the one I would book: a guide who actually guided, a schedule that ran on time, the best sandboarding of all my safaris and an evening show that beat the \"luxury\" camps.",
        rating=rate('card-1', 's1'),
        facts=[('Price', 'From €29', 'per person'),
               ('Duration', '4 to 7 hours', 'the 7-hour option adds BBQ dinner and shows'),
               ('Desert', 'Al Lahbab red dunes', 'about 1 hour from the city'),
               ('Cancellation', 'Free', 'up to 24 hours before')],
        link=link, cta_top='CHECK DATES FROM €29 →', cta_mid='SEE AVAILABLE DATES FROM €29 →', cta_bottom='CHECK DATES &amp; BOOK →',
        pick='it is your first desert safari and you want it all in one afternoon and evening: dune bashing, sandboarding, a camel ride, a BBQ dinner and shows.',
        skip=f'you want a quiet nature drive without dune bashing (pick {a("card-5", "Platinum Heritage")}, from €195) or you only have a morning free (pick {a("card-2", "the Funtours morning safari")}, from €27).',
        intro='<p>Every Dubai desert safari promises dune bashing, camels and a BBQ under the stars, and most have thousands of 5-star reviews. Prices run from €24 to €195 and the guides, camps and shows are very different, so it is easy to end up in a crowded camp with a bored driver. So I booked <strong>8 of the most popular desert safaris</strong> myself and paid for every one.</p>'
              f'<p>I judged the guide, the cars and the dune bashing, the activities, the camp, the food, the shows and the value for money. Below is the short version: which one won, why, and when one of the other seven is the better pick for you. The full reviews and photos are in <a href="/{hub}">my complete Dubai desert safari ranking</a>.</p>',
        compare_h2='How the 8 Desert Safaris I Tested Compare', rows=rows,
        why_h2='Why Excursion Point Took the #1 Spot',
        why='<p>Several safaris came close on price, and Noble Life and Platinum Heritage had fancier settings. Excursion Point was the one with <strong>no weak link</strong>: an on-time pickup, a real guide, well-kept vehicles, activities that were thrilling but safe, and the best camp evening of all 8. If you only book one desert safari in Dubai, book this one. Here is what I found.</p>',
        features=[
            dict(h='A Guide, Not Just a Driver', body=img(im('68bc785f92fadf41297ea997_6870b32811e696b1d3577fe2_16391129-1AFE-476A-89B4-BBAA5DDD8CE3_1_105_c_result.webp'), 'Ismail, the Excursion Point guide, in the desert')
                 + '<p>Pickup was set for 2:45 PM and the driver arrived at 2:44. On the hour-long, 90 km drive our guide Ismail talked about Dubai\'s population, architecture, nature and history, explained how the desert\'s three sand colours formed and <strong>answered every question</strong>. I fact-checked him later: he was right. Across the whole 7-hour tour there were no delays and no waiting around.</p>'),
            dict(h='Its Own Quad and Buggy Station', body=img(im('68bc785e9af6b76e9a3f1ff7_68727f3ed7b8488590723816_Buggy.webp'), 'A dune buggy at the Excursion Point quad and buggy station')
                 + '<p>Excursion Point uses <strong>its own quad and buggy station</strong> instead of a shared rental yard: spotless restrooms, an air-conditioned shop, brand-new quads and well-kept buggies. I upgraded to a 1000cc buggy, about four times the power of the 250cc quads, and it was the highlight of the day. The upgrade costs extra, and it is much cheaper booked online in advance than paid on the spot.</p>'),
            dict(h='Hard Dune Bashing, Done Safely', body=img(im('68bc785ed95f81619ad167ac_6873a475db4d07b96bb82b32_Untitled_result.webp'), 'The Excursion Point convoy of 4x4s in the red dunes')
                 + '<p>Ismail checked every seatbelt, then floored it: about <strong>20 minutes of intense dune bashing</strong> and 10 more of a gentler ride. The tyres were let down almost flat for better grip and smoother turns, something most operators only do halfway. Afterwards the team even cleaned the sand off our shoes.</p>'),
            dict(h='The Best Sandboarding of All 8 Safaris', body=img(im('68bc785ea6383274efc20f29_6873a5ec630a6b5552a632e7_B5B26C27-CF6B-42DC-B7BF-F97FA617103C_1_105_c_result.webp'), 'Standing sandboarding down a dune on the Excursion Point safari')
                 + '<p>The guides took the time to show how to ride sitting down, which no other operator did. Sitting, I had <strong>my fastest, longest and smoothest run of any safari</strong>. There is also a falcon photo stop in the open desert for about 20 AED (around €5), payable by card.</p>'),
            dict(h='A Camp and Show That Beat the "Luxury" Camps', body=img(im('68bc785e774f16d715f497da_6870b329ff3fffa236c03ca3_C9776415-0EE5-49C2-8BA2-8C6538033508_1_105_c_result.webp'), 'The fortress-style desert camp used on the Excursion Point safari')
                 + '<p>The evening is spent at a large <strong>fortress-style camp run by Arabian Adventures</strong>, an Emirates Group brand: spotless, with sun loungers, campfires, a camel ride, henna, shisha and even football and badminton courts. The BBQ buffet was delicious with just enough variety.</p>'
                 + img(im('68bc785dba2e9e3847dd7efb_6877d538ac6ff0e7bc624109_Fire%2520Show_result.webp'), 'The fire show at the desert camp')
                 + '<p>The show opened with a Tanoura dancer, then the best belly dancer I saw on any tour, and finished with a 20-minute fire show. The drive back took about 50 minutes, so I was in the city by 10 PM.</p>'),
        ],
        cons=[('Only two soft drinks are included.', 'Water is unlimited, but alcohol, juices and extra soft drinks cost extra at the camp.'),
              ('The back row is cramped for tall people.', 'At 190 cm I was fine because only two people sat in the back, but sit further forward if you can.'),
              ('The buggy upgrade is extra.', 'And the ride depends a lot on your guide and the speed of the group.'),
              ('It is a long day.', 'The dinner option runs about 7 hours from pickup.'),
              ('The falcon photo costs extra.', 'About 20 AED, and falcons are not careful with your shirt.')],
        faqs=[('Morning or evening safari?', 'The afternoon option with the BBQ dinner and shows is the one I tested and recommend. The morning tours skip dinner and the camp evening.'),
              ('What is included?', 'Dune bashing, sandboarding and a camel ride, plus the BBQ dinner and Tanoura show on the dinner option. Two soft drinks and unlimited water are included. Quad bike time depends on the option you choose.'),
              ('Is alcohol available?', 'Yes, at the camp bar, but you pay for it separately.'),
              ('What are the pickup times?', 'On the GetYourGuide calendar for Saturday 14 November 2026: morning tours at 07:00, 08:00, 09:00 and 10:00, afternoon tours with the camp dinner at 14:00, 15:00 and 15:30. Times change by season.'),
              ('Which languages does the guide speak?', 'English, Hindi and Urdu, as listed on GetYourGuide.')],
        final_h3='My pick for your Dubai desert safari',
        final="Excursion Point's red dunes safari with the BBQ dinner option. Hand over your phone before sandboarding, and do not wear your favourite shirt for the falcon photo.",
        secure='🔒 Instant mobile ticket • Free cancellation up to 24 hours • Secure checkout via GetYourGuide',
        callout='my one-pick verdict: the desert safari I would book first',
    )


# =============================================================== PALM ======
def palm():
    hub = 'best-palm-jumeirah-hotels-dubai'
    c = cards(read(hub + '/index.html'))
    win = c['card-1']
    link = lambda slot: tp(win['href'], 'palm_verdict_' + slot)
    rate = lambda cid, key: retag(c[cid]['rating'], lambda u: tp(u, 'palm_verdict_reviews_' + key) if 'tp.media' in u else u)
    im = lambda f: CDN + f
    spec = [
        ('card-1', 'Atlantis, The Palm', '5★ mega resort, Crescent Road', 'Families and first-time visitors', 'The busiest resort on the Palm', 'atlantis_palm'),
        ('card-2', 'Atlantis The Royal', '5★ ultra-luxury, Crescent Road', 'A splurge: Cloud 22 rooftop pool, chef-led restaurants', 'Rooms rarely drop below €1,000 a night', 'atlantis_royal'),
        ('card-3', 'Anantara The Palm', '5★ Thai resort, East Crescent', 'Calm couples stays, lagoon pools, overwater villas', 'Far from Dubai Marina nightlife', 'anantara'),
        ('card-4', 'FIVE Palm Jumeirah', '5★ party resort, Palm West Beach', 'Pool and beach club parties with daily DJs', 'Not for young kids or early nights', 'five'),
        ('card-5', 'Rixos The Palm', '5★ all-inclusive, East Crescent', 'All-inclusive meals and drinks', 'You pay for meals even when you eat out', 'rixos'),
    ]
    rows = [dict(col='Hotel', winner=i == 0, tested=True, name=name, anchor=c[cid]['anchor'], meta=meta,
                 rating=rate(cid, key), price=c[cid]['price'], best=best, con=con)
            for i, (cid, name, meta, best, con, key) in enumerate(spec)]
    a = lambda cid, text: f'<a href="/{hub}{c[cid]["anchor"]}">{text}</a>'
    video = ('<div class="adv-video"><a class="ltt-yt" href="https://www.youtube.com/watch?v=bOwF1V0GFEE" data-yt="bOwF1V0GFEE" '
             'data-title="Atlantis The Palm: The Best 5-Star Palm Hotel in Dubai (Full Review)" aria-label="Play video: Atlantis The Palm: The Best 5-Star Palm Hotel in Dubai (Full Review)" '
             'target="_blank" rel="noopener" style="position:absolute;top:0;left:0;width:100%;height:100%;display:block;margin:0">'
             '<img src="/assets/video/bOwF1V0GFEE.webp" alt="Atlantis The Palm: The Best 5-Star Palm Hotel in Dubai (Full Review)" width="800" height="450" loading="lazy" decoding="async" '
             'style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;margin:0;max-width:none;border:0">'
             '<span class="ltt-yt-play" aria-hidden="true" style="position:absolute;top:50%;left:50%;width:68px;height:48px;transform:translate(-50%,-50%);line-height:0">'
             '<svg viewBox="0 0 68 48" width="68" height="48" focusable="false"><path d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79.13 34 0 34 0S12.21.13 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C.06 13.05 0 24 0 24s.06 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 47.87 34 48 34 48s21.79-.13 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C67.94 34.95 68 24 68 24s-.06-10.95-1.48-16.26z" fill="#212121" fill-opacity=".8"/><path d="M45 24 27 14v20" fill="#fff"/></svg></span></a></div>'
             '<p class="adv-image-caption">My video review of Atlantis, The Palm.</p>')
    return dict(
        slug='best-palm-jumeirah-hotel-dubai', hub=hub, hub_label='Palm Jumeirah Hotels', crumb='Best Palm Jumeirah Hotel',
        title='Best Hotel on Palm Jumeirah (2026): I Stayed at 5, This One Won',
        desc='I stayed at 5 Palm Jumeirah resorts and paid for every night. Atlantis, The Palm is the best all-rounder: Aquaventure and The Lost Chambers included, from €300 a night.',
        h1='I Stayed at 5 Hotels on Palm Jumeirah.', h1_muted="Here's the One Worth Your Money.",
        role='5 Palm Resorts Stayed at in Person • Every Room Photographed • 100% Self-Funded',
        hero=im('682c7f5e372dcede8c3a9dc1_IMG_1711.webp'),
        hero_alt='The view of Atlantis, The Palm and its pools from a Palm King room balcony',
        hero_caption='The view from my Palm King room balcony at Atlantis, The Palm. My photo from the stay.',
        tldr='I stayed at 5 of the most popular hotels on Palm Jumeirah and paid for every night myself. <strong>Atlantis, The Palm</strong> is the one I would book for most people, especially on a first trip to Dubai: the Aquaventure waterpark and The Lost Chambers aquarium are included for guests, the buffets were the best of all the hotels and the service was excellent from start to finish.',
        rating=rate('card-1', 'atlantis_palm'),
        facts=[('Price', 'From €300', 'per night on Booking.com'),
               ('Included', 'Aquaventure &amp; aquarium', 'free entry for hotel guests'),
               ('Location', 'Crescent Road', 'the centre of the Palm\'s crescent'),
               ('Check-in', '15:00', 'check-out until 12:00')],
        link=link, cta_top='CHECK PRICES FROM €300 →', cta_mid='SEE PRICES FOR YOUR DATES →', cta_bottom='CHECK AVAILABILITY &amp; BOOK →',
        pick='you are travelling with kids, it is your first stay on the Palm, or you want a resort with something to do all day.',
        skip=f'you want peace and quiet (pick {a("card-3", "Anantara The Palm")}, from €200), a no-limits splurge (pick {a("card-2", "Atlantis The Royal")}, from €1,000) or all meals and drinks included (pick {a("card-5", "Rixos The Palm")}, from €350).',
        intro='<p>Every Palm Jumeirah resort promises a private beach, sea views and 5-star service, and prices run from about €160 to well over €1,000 a night. What you actually get for the money is very different, so I stayed at <strong>5 of the most popular resorts on the Palm</strong> and paid for every stay myself. At Atlantis, The Palm I spent 5 nights in a Palm King room.</p>'
              f'<p>I judged the rooms, the food, the pools and beach, the service and what is included in the price. Below is the short version: which one won, why, and when one of the other four is the better pick for you. The full reviews and photos are in <a href="/{hub}">my complete Palm Jumeirah hotel ranking</a>.</p>',
        compare_h2='How the 5 Palm Jumeirah Hotels I Stayed At Compare', rows=rows,
        table_note='<p class="adv-table-note">Prices are the lowest nightly rates on Booking.com when checked on 12 November 2026 and change with your dates.</p>',
        why_h2='Why Atlantis, The Palm Took the #1 Spot',
        why='<p>Atlantis The Royal is more luxurious and Anantara is calmer, but Atlantis, The Palm gave me <strong>the most for the money</strong>. The waterpark and aquarium alone would cost a family hundreds, and the rooms, food and service were all top level. It is the best all-round stay on the Palm, which is why it is my top recommendation.</p>' + video,
        features=[
            dict(h='Aquaventure and The Lost Chambers Are Included', body=img(im('688fffd268b6787dbc77c0ba_Image%20(34).avif'), 'Water slides at Aquaventure World next to Atlantis, The Palm')
                 + '<p>Hotel guests get <strong>free entry to Aquaventure World</strong>, with over 105 slides and attractions, rapids and a 1 km private beach. I tried it all. It is a blast, but expect plenty of stairs and queues.</p>'
                 + img(im('688b5fd2e2496c5e3f1f5f97_best-palm-hotels-dubai-atlantis-palm24.avif'), 'A school of rays in The Lost Chambers Aquarium at Atlantis, The Palm')
                 + '<p><strong>The Lost Chambers Aquarium</strong> has over 65,000 marine animals in 21 exhibits, with glass tunnels full of sharks and rays. It is open daily from 10 AM to 9 PM and free for resort guests.</p>'),
            dict(h='Big, Comfortable Rooms, Even at Entry Level', body=img(im('682c889734c61dad7347bced_IMG_1709.webp'), 'The king bed in a Palm King room at Atlantis, The Palm')
                 + '<p>I booked the cheapest <strong>Palm King room</strong> and paid 9,659.79 AED (about €2,432) for 5 nights. The bed was exceptionally comfortable, the room has a Nespresso machine and a marble work desk, and sheets and towels were changed every day.</p>'
                 + img(im('682c7e20793f852eb6ff6280_IMG_1673.webp'), 'The Palm view over the resort pools and Palm Jumeirah from a Palm King room')
                 + '<p>Pick the <strong>Palm view over the Ocean view</strong>: you look over the courtyard, Palm Jumeirah and the Dubai skyline, while the sea side has much less to see.</p>'),
            dict(h='The Best Buffets of All the Hotels I Tested', body=img(im('68398b64e5ba075d884ac541_IMG_1766.webp'), 'The breakfast buffet hall at Atlantis, The Palm')
                 + '<p>Breakfast runs from 7:00 to 11:30 at Saffron and Kaleidoscope, which serve the same food. Arrive before 9 AM to skip the queue. At dinner, <strong>Saffron is Dubai\'s largest Asian buffet</strong>, with over 220 dishes and a different theme every night. Both were the best buffets I had at any hotel on the Palm.</p>'
                 + '<p>On top of that there are celebrity-chef and Michelin-starred restaurants such as Ossiano, Hakkasan, Nobu and FZN, at extra cost.</p>'),
            dict(h='Service That Went Above and Beyond', body=img(im('682c7cf2c604204b37726d31_best-palm-hotels-dubai-atlantis-the-palm-main-hall%20(5).webp'), 'The Grand Lobby of Atlantis, The Palm with its Dale Chihuly glass sculpture')
                 + '<p>Staff took my luggage straight from the Uber to my room, and I was let into the room by 11 AM without asking for early check-in. Housekeeping left small gifts without being asked, a mouse pad and a glasses cloth. <strong>Every member of staff I dealt with was friendly and quick to help.</strong></p>'),
            dict(h='Easy for Families', body=img(im('6839ddf5f52cab8a62063650_IMG_1851.webp'), 'Sun loungers on the private beach at Atlantis, The Palm')
                 + '<p>The Family Pool has shallow areas and lifeguards, and the <strong>private beach comes with free sun loungers, umbrellas and towels</strong>. The Atlantis Explorers Club keeps kids aged 4 to 12 busy with themed zones and workshops, and there is a supervised play area for toddlers, run by staff trained in paediatric first aid.</p>'),
        ],
        cons=[("The room doors aren't soundproof.", 'I could hear slamming doors, conversations and children in the hallway, especially in the morning.'),
              ('The Wi-Fi was unstable.', 'Video calls dropped and pages loaded slowly when I tried to work.'),
              ('It is busy.', 'It is the busiest resort on the Palm, and Aquaventure has queues.'),
              ('Breakfast is not always in the rate.', 'If it is not, it costs €42 per person.'),
              ('The top restaurants cost extra.', 'So does the WHITE Beach club.')],
        faqs=[('Is Aquaventure included?', 'Yes. Hotel guests get free entry to Aquaventure World and The Lost Chambers Aquarium.'),
              ('Which room should I book?', 'The Palm King room with a Palm view. It is the cheapest category and the view over the Palm and the skyline beats the Ocean view.'),
              ('What are the check-in and check-out times?', 'Check-in from 15:00 and check-out until 12:00, as listed on Booking.com. Members of the free Atlantis Unlocked programme can ask for a late check-out.'),
              ('Atlantis, The Palm or Atlantis The Royal?', 'Atlantis, The Palm for value and families, from €300 a night. Atlantis The Royal for a splurge, from €1,000 a night.'),
              ('Is breakfast included?', 'It depends on your rate. If it is not included, breakfast costs €42 per person.')],
        final_h3='My pick for your Palm Jumeirah stay',
        final='Atlantis, The Palm in a Palm King room with the Palm view. Get to breakfast before 9 AM and to Aquaventure early.',
        secure='🔒 Secure booking via Booking.com',
        callout='my one-pick verdict: the Palm Jumeirah hotel I would book first',
    )


# ============================================================ hub callout ==
CALLOUT_ID = 'ltt-verdict-callout'


def add_callout(p):
    path = os.path.join(ROOT, p['hub'], 'index.html')
    with open(path, encoding='utf-8') as f:
        src = f.read()
    src = re.sub(r'<p id="%s".*?</p>' % CALLOUT_ID, '', src, flags=re.S)
    box = (f'<p id="{CALLOUT_ID}" style="margin:12px 0 0;padding:10px 14px;background:#fdfaf2;border:1px solid #f2e0b6;'
           f'border-radius:10px;font-size:14.5px;line-height:1.5;color:#334155">⏱️ <strong>Short on time?</strong> Read '
           f'<a href="/{p["slug"]}" style="color:#9f6e0d;font-weight:700">{p["callout"]}</a>.</p>')
    anchor = '<div class="ltt-integrated-filter-bar">'
    lead_end = src.index(anchor)
    src = src[:lead_end] + box + '\n' + src[lead_end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(src)


if __name__ == '__main__':
    for page in (heli(), desert(), palm()):
        build(page)
        add_callout(page)
