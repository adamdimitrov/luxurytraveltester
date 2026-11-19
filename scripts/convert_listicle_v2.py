#!/usr/bin/env python3
"""Move a batch-1 comparison page (built by scripts/build_article.py in the old desert-safari
shell) to the kit listicle design of best-desert-safaris-dubai.

    python3 scripts/convert_listicle_v2.py <slug> [<slug> ...]

What it does, per page (everything else on the page stays byte for byte):
  - cards: written as data to data/listicles/<slug>--index.json from the page's spec
    (scripts/articles/<slug>.json), then rendered by the kit (scripts/listicle.py build).
    Thumbnails, price dropdown, green trust box and 5 "questions travellers ask" per card.
    The questions are built only from the card's own Quick Facts (same words as the
    review below), so no fact is added.
  - head: inline bpa-lang/bpa-card2 CSS -> shared /css/listicle-*.css (+ cd-trust-css).
  - hero: flat filter pills -> grouped filter box (same filter categories and labels).
  - deck: sticky "Filters" shortcut (cd-fmini).
  - end of body: inline bpa-lang-js -> shared /js/listicle-*.js + the three small helpers of
    the desert page (price dropdown hover, sticky trust, sticky price).
  - JSON-LD: the card questions are added to the page's FAQPage.
  - site.json: page added to listicle.pages.
Small thumbnails (240x160 AVIF) are made locally from the card photos.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "best-desert-safaris-dubai" / "index.html"
E = html.escape
REL = "noopener nofollow sponsored"
LAZY = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"

# Filter rows per page: (row label, [filter cats]). The first row is always shown; the others
# fold under "More filters" on phones. Cats and labels are the page's existing filters.
ROWS = {
    "best-adrenaline-experiences-dubai": [("Where", ["sky", "water"]), ("Who & budget", ["kids", "couples", "budget"])],
    "best-burj-khalifa-tickets": [("Ticket", ["fasttrack", "premium", "combo"]), ("Who & budget", ["family", "budget"])],
    "best-dinner-cruises-dubai": [("Boat", ["dhow", "megayacht"]), ("On board", ["show", "openbar"]), ("Budget", ["budget"])],
    "best-dubai-city-tours": [("Tour", ["guided", "hoho", "private"]), ("When & budget", ["night", "budget"])],
    "best-dune-buggy-tours-dubai": [("Ride", ["hour", "private"]), ("Extras & who", ["bbq", "family", "budget"])],
    "best-helicopter-tours-dubai": [("Flight", ["short", "long"]), ("Extras", ["pickup", "combo", "value"])],
    "best-hot-air-balloon-dubai": [("Package", ["flight", "breakfast", "camel"]), ("Style & budget", ["luxury", "budget"])],
    "best-jet-ski-tours-dubai": [("Ride", ["palm", "long"]), ("Extras & budget", ["photos", "budget"])],
    "best-scuba-diving-dubai": [("Level", ["beginner", "certified"]), ("Where", ["sea", "pool", "snorkel"])],
    "best-water-parks-dubai": [("Park", ["thrill", "kids"]), ("Ticket", ["combo", "daytrip", "budget"])],
}

# Quick Facts label -> question. Order = which facts become the 5 questions first.
QUESTIONS = [
    ("Included", "What is included?"),
    ("Included in every tier", "What does every tier include?"),
    ("Not included", "What is not included?"),
    ("Cancellation", "What is the cancellation policy?"),
    ("Meeting point", "Where does it start?"),
    ("Location", "Where is it?"),
    ("Pickup", "What about hotel pickup?"),
    ("Pickup area", "Where is pickup?"),
    ("Time", "What time does it run?"),
    ("Hours", "What are the opening hours?"),
    ("Schedule", "What is the schedule?"),
    ("Flight lengths", "How long is the flight?"),
    ("Itinerary", "What is the route?"),
    ("Landmarks", "Which landmarks will I see?"),
    ("Not suitable for", "Who should not book it?"),
    ("Requirements", "What are the requirements?"),
    ("Restrictions", "What are the restrictions?"),
    ("Age", "What are the age rules?"),
    ("Children", "What about children?"),
    ("Kids", "What about kids?"),
    ("Riders", "How many riders per jet ski?"),
    ("Capacity", "How many people per balloon?"),
    ("Seats", "How are seats assigned?"),
    ("Group", "How big is the group?"),
    ("Group size", "How big is the group?"),
    ("Deluxe and premium", "What do Deluxe and Premium add?"),
    ("Premium only", "What does only Premium include?"),
    ("Camp", "What happens at the camp?"),
    ("Return", "Where does it end?"),
    ("Entry", "How does entry work?"),
    ("Access", "How accessible is it?"),
    ("Meal times", "When are meals served?"),
    ("Aquarium hours", "When is the aquarium open?"),
    ("Fridays", "What about Fridays?"),
    ("Closed", "When is it closed?"),
    ("Rules", "Any rules to know?"),
    ("Optional", "What can I add?"),
    ("Optional extra", "What can I add?"),
    ("Before you go", "What should I know before I go?"),
    ("What to bring", "What should I bring?"),
    ("Accessibility", "How accessible is it?"),
    ("Languages", "Which languages are offered?"),
]
QMAP = dict(QUESTIONS)
QORDER = [k for k, _ in QUESTIONS]


def money(v):
    v = float(v)
    return f"€{v:.0f}" if v >= 10 or v == int(v) else f"€{v:.2f}"


def compact(n):
    n = int(n)
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k+"
    return str(n)


def sentence(s):
    s = s.strip()
    s = s[0].upper() + s[1:]
    return s if s[-1] in ".!?" else s + "."


def trust_line(t):
    m = re.match(r"(Free cancellation)( .*)?$", t)
    if m:
        return f"<b>{m.group(1)}</b>{E(m.group(2) or '')}"
    m = re.match(r"(Reserve now, pay later)$", t)
    if m:
        return "<b>Reserve now, pay later</b>"
    m = re.match(r"(.+?)( (?:included|available|accessible))$", t)
    if m:
        return f"<b>{E(m.group(1))}</b>{E(m.group(2))}"
    return f"<b>{E(t)}</b>"


def faq_items(it):
    facts = {k: v for k, v in it["facts"]}
    labels = sorted(facts, key=lambda k: QORDER.index(k) if k in QORDER else 999)
    out, seen = [], set()
    for k in labels:
        q = QMAP.get(k)
        if not q or q in seen:
            continue
        seen.add(q)
        a = sentence(facts[k])
        out.append({"q": q, "a": a})
        if len(out) == 5:
            break
    if len(out) < 5:
        out.insert(min(3, len(out)), {"q": "How much does it cost?",
                                      "a": f"From {money(it['price'])} {E(it.get('price_unit', 'per person'))}. "
                                           "The final price for your date is shown before you pay."})
    if len(out) < 5:
        sys.exit(f"  ! {it['title']}: only {len(out)} questions from facts {list(facts)}")
    return out


def thumb(slug, src):
    p = ROOT / src.lstrip("/")
    t = p.with_name(p.stem + "-t.avif")
    if not t.exists():
        im = Image.open(p).convert("RGB")
        im.thumbnail((240, 160))
        im.save(t, "AVIF", quality=50)
    return "/" + str(t.relative_to(ROOT))


def card(n, it, spec, live):
    alt = it["title"]
    photos = []
    for i, src in enumerate(it["photos"]):
        if i == 0:
            at = [["alt", alt]]
            if n == 1:
                at.append(["fetchpriority", "high"])
            at += [["height", "500"], ["loading", "eager" if n == 1 else "lazy"], ["sizes", SIZES], ["src", src], ["width", "800"]]
        else:
            at = [["alt", alt], ["data-src", src], ["decoding", "async"], ["height", "500"], ["loading", "lazy"],
                  ["sizes", SIZES], ["src", LAZY], ["width", "800"]]
        photos.append(at)
    link = live["link"]
    gyg = {"kind": "link", "site": "GetYourGuide", "score": f"{it['rating']:.1f}", "count": f"({compact(it['reviews'])})",
           "url": link, "rel": REL, "target": "_blank"}
    pills = []
    for p in it["pills"][:4]:
        note = f'<span class="bpa-lang-note">{p["note"]}</span>' if p.get("note") else ""
        pills.append({"cls": "bpa-lang", "emoji": p["emoji"], "label": E(p["label"]),
                      "pop_html": f'<strong>{E(p["lead"])}</strong> {p["body"]}{note}'})
    rows = [{"label": "Starting price", "small": E(it.get("price_unit", "per person")), "price": money(it["price"])}]
    note = "The price depends on the date and the option you pick. Final price shown before you pay."
    if it.get("price_was") and float(it["price_was"]) > float(it["price"]):
        pct = round((1 - float(it["price"]) / float(it["price_was"])) * 100)
        rows.append({"label": "Price before the current discount", "small": f"−{pct}%", "price": f"<s>{money(it['price_was'])}</s>"})
    return {
        "id": f"card-{n}",
        "cats": it["cat"].split(),
        "gallery": {"rank": {"text": it["rank_tag"], "medal": it["rank_class"]}, "photos": photos,
                    "thumbs": [{"src": thumb(spec["slug"], s)} for s in it["photos"]]},
        "kicker": [E(it["operator"]), f"⏱️ {E(it['duration'])}",
                   {"url": "https://maps.google.com/?q=" + it["map_q"].replace(" ", "+"), "rel": "noopener noreferrer",
                    "target": "_blank", "onclick": "event.stopPropagation()", "map": f"📍 {E(it['place'])}"}],
        "title": {"url": link, "rel": REL, "target": "_blank", "text": E(it["title"])},
        "reviews": {"ratings": {"stars": f"{it['rating']:.2f}", "score": f"{it['rating']:.1f}",
                                "meta": f"{compact(it['reviews'])} reviews · 1 site", "heading": "Rating on GetYourGuide",
                                "sites": [gyg]}},
        "pills": pills,
        "best_for": {"pick_html": it["pick"], "skip_html": it["skip"]},
        "faq": {"items": faq_items(it)},
        "price": {"main": money(it["price"]), "sub": "from, " + E(it.get("price_unit", "per person")),
                  "_heading": "Price", "rows": rows, "note": note},
        "cta": {"btn": {"url": link, "rel": REL, "target": "_blank", "text": "Check Availability →"},
                "via": "Booked securely via GetYourGuide",
                "trust": [trust_line(t) for t in it.get("trust", [])],
                "sublink": {"url": live["sublink"], "text": "Read Review ↓"}},
    }


def block(t, kind, bid):
    m = re.search(r'<%s[^>]*id="%s"[^>]*>.*?</%s>' % (kind, re.escape(bid), kind), t, re.S)
    if not m:
        sys.exit(f"  ! block {kind}#{bid} not found")
    return m


def live_cards(t):
    out = []
    for m in re.finditer(r'<div class="bpa-card" data-cat="([^"]*)" id="card-(\d+)">(.*?)<a class="bpa-sublink" href="([^"]+)"', t, re.S):
        body = m.group(3)
        link = html.unescape(re.search(r'<a class="bpa-title" href="([^"]+)"', body).group(1))
        title = html.unescape(re.search(r'<a class="bpa-title"[^>]*>(.*?)</a>', body).group(1))
        price = re.search(r'<div class="bpa-price">From (€[\d.]+)</div>', body).group(1)
        photos = re.findall(r'<img alt="[^"]*"(?: fetchpriority="high")? (?:data-src="([^"]+)"|height="500" loading="\w+" src="([^"]+)")', body)
        out.append({"cat": m.group(1), "link": link, "title": title, "price": price,
                    "photos": [a or b for a, b in photos], "sublink": m.group(4)})
    return out


def filter_box(spec, rows):
    things = spec["things"].lower()
    n = len(spec["items"])
    labels = {f["cat"]: f["label"] for f in spec["filters"]}
    used = [c for _, cs in rows for c in cs]
    if sorted(used) != sorted(labels):
        sys.exit(f"  ! filter rows {sorted(used)} != page filters {sorted(labels)}")
    out = [f'<div class="ltt-integrated-filter-bar cd-fbox" id="cd-filters" role="group" aria-label="Filter {E(things)}">']
    for i, (lab, cats) in enumerate(rows):
        btns = "".join(
            f'<button class="ltt-tab-btn" data-cat="{c}" onclick="lttFilterSafaris(\'{c}\', this)" type="button" '
            f'aria-pressed="false">{E(labels[c])} <span class="cd-n"></span></button>' for c in cats)
        out.append(f'<div class="cd-frow {"cd-frow-main" if i == 0 else "cd-frow-more"}"><span class="cd-flab">{E(lab)}</span>'
                   f'<div class="cd-fchips">{btns}</div></div>')
    out.append('<button type="button" class="cd-fmore" aria-expanded="false" hidden>More filters <span class="cd-fmore-n"></span> ▾</button>'
               f'<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>{n}</b> of {n} {E(things)}</span>'
               '<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden onclick="lttFilterSafaris(\'all\')">Clear all</button></div></div>')
    mini = ('<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
            'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button>'
            f'<span class="cd-fmini-res"><b>{n}</b> of {n} {E(things)}</span></div></div>')
    return "".join(out), mini


def convert(slug):
    page = ROOT / slug / "index.html"
    spec = json.loads((ROOT / "scripts" / "articles" / f"{slug}.json").read_text())
    t = page.read_text(encoding="utf-8")
    ref = REF.read_text(encoding="utf-8")
    if "/css/listicle-cards.css" in t:
        sys.exit(f"  ! {slug} is already converted")

    live = live_cards(t)
    if len(live) != len(spec["items"]):
        sys.exit(f"  ! {slug}: {len(live)} cards on the page, {len(spec['items'])} in the spec")
    for n, (lv, it) in enumerate(zip(live, spec["items"]), 1):
        probs = []
        if lv["title"] != it["title"]:
            probs.append(f"title {lv['title']!r} != {it['title']!r}")
        if lv["price"] != f"{money(it['price'])}":
            probs.append(f"price {lv['price']} != {money(it['price'])}")
        if lv["photos"] != it["photos"]:
            probs.append("photos differ")
        if lv["cat"] != it["cat"]:
            probs.append("cats differ")
        if "mkt_cmp=true" not in lv["link"] or f"cmp={spec['cmp']}" not in lv["link"]:
            probs.append("link tags")
        if probs:
            sys.exit(f"  ! {slug} card {n}: " + "; ".join(probs))

    data = {"format": 1, "icons": json.loads((ROOT / "data/listicles/best-desert-safaris-dubai--index.json").read_text())["icons"],
            "cards": [card(n, it, spec, lv) for n, (it, lv) in enumerate(zip(spec["items"], live), 1)]}
    (ROOT / "data/listicles" / f"{slug}--index.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

    # head CSS
    a, b = block(t, "style", "bpa-lang-css"), block(t, "style", "bpa-card2-css")
    if t[a.end():b.start()].strip():
        sys.exit("  ! bpa-lang-css and bpa-card2-css not adjacent")
    r1 = re.search(r'<link rel="stylesheet" href="/css/listicle-base.css[^>]*>', ref).group(0)
    r2 = re.search(r'<link rel="stylesheet" href="/css/listicle-cards.css[^>]*>', ref).group(0)
    t = t[:a.start()] + r1 + "\n" + r2 + block(ref, "style", "cd-trust-css").group(0) + t[b.end():]

    # filters
    box, mini = filter_box(spec, ROWS[slug])
    m = re.search(r'<div class="ltt-integrated-filter-bar">\n<span class="ltt-filter-label">Filters:</span>\n'
                  r'<div class="ltt-integrated-pills">.*?</div>\n</div>', t, re.S)
    t = t[:m.start()] + box + t[m.end():]

    # deck: fmini + cards (comments between cards go; the kit renders the card region)
    t = re.sub(r"<!-- #\d+: .*? -->\n?", "", t)
    t = t.replace('<div class="bpa-deck-wrap" id="ltt-cards-deck">', '<div class="bpa-deck-wrap" id="ltt-cards-deck">\n' + mini + "\n", 1)

    # sticky trust
    t = t.replace('<span class="hybrid-active-trust">🛡️ Free 24h Cancel</span>',
                  '<span class="hybrid-active-trust" id="sticky-trust">Free cancellation</span>', 1)

    # scripts
    js = block(t, "script", "bpa-lang-js")
    ui = {"showing": f"Showing <b>{{shown}}</b> of {{total}} {spec['things'].lower()}",
          "mini_count": f"<b>{{shown}}</b> of {{total}} {spec['things'].lower()}",
          "breakdown_filtered": f"Showing {{shown}} of {{total}} {spec['things'].lower()} matching your filters"}
    tags = re.search(r'<script src="/js/listicle-lang.js.*?<script src="/js/listicle-peek.js[^>]*></script>', ref, re.S).group(0)
    helpers = "".join(block(ref, "script", i).group(0) for i in ("pdd-hover-js", "cd-sticky-trust-js", "ltt-sticky-price-js"))
    t = (t[:js.start()] + '<script type="application/json" id="listicle-ui">' + json.dumps(ui, ensure_ascii=False)
         + "</script>" + tags + helpers + t[js.end():])

    # JSON-LD: card questions join the page FAQ
    m = block(t, "script", "ltt-schema-jsonld")
    body = re.search(r">(.*)</script>$", m.group(0), re.S).group(1)
    ld = json.loads(body)
    faq = next((g for g in ld["@graph"] if g["@type"] == "FAQPage"), None)
    if faq is None:
        faq = {"@type": "FAQPage", "mainEntity": []}
        ld["@graph"].append(faq)
    for c, it in zip(data["cards"], spec["items"]):
        for x in c["faq"]["items"]:
            faq["mainEntity"].append({"@type": "Question", "name": f"{it['title']}: {x['q']}",
                                      "acceptedAnswer": {"@type": "Answer", "text": x["a"]}})
    t = t[:m.start()] + m.group(0).replace(body, "\n" + json.dumps(ld, ensure_ascii=False, indent=1) + "\n") + t[m.end():]

    page.write_text(t, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts/listicle.py"), "build", str(page)], check=True)

    cfg = json.loads((ROOT / "site.json").read_text())
    pages = cfg["listicle"]["pages"]
    if f"{slug}/index.html" not in pages:
        pages.append(f"{slug}/index.html")
        (ROOT / "site.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
    print(f"converted {slug}: {len(data['cards'])} cards")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        convert(s)
