#!/usr/bin/env python3
"""Wire new Dubai hotel comparison pages (Booking.com specs) into the site. Idempotent.

    python3 scripts/wire_hotels.py best-luxury-hotels-dubai best-hotels-dubai-marina ...

- menu (data/menu/en.json): a "DUBAI HOTELS" group in the third mega-menu column and a
  "Dubai Hotels" section in the mobile drawer (after Dubai Experiences);
- homepage: a "Dubai Hotels Compared" section after the flagship guides, one card per page;
- contextual links: a "More Dubai hotels, compared" block on the Palm hotels hub.
Then run: python3 scripts/menu.py build && python3 scripts/sync_layout.py && python3 scripts/generate_sitemap.py
"""
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
MENU = ROOT / "data" / "menu" / "en.json"
HOME = ROOT / "index.html"
LABELS = {
    "best-luxury-hotels-dubai": ("💎", "Luxury Hotels"),
    "best-beach-resorts-dubai": ("🏖️", "Beach Resorts"),
    "best-family-resorts-dubai": ("👨‍👩‍👧", "Family Resorts"),
    "best-hotels-dubai-marina": ("⛵", "Dubai Marina Hotels"),
    "best-hotels-downtown-dubai": ("🏙️", "Downtown Hotels"),
    "best-hotels-jbr-dubai": ("🌊", "JBR Hotels"),
    "best-hotels-business-bay-dubai": ("🏢", "Business Bay Hotels"),
    "best-hotels-dubai-creek": ("🛶", "Creek & Deira Hotels"),
    "best-hotels-dubai-airport": ("✈️", "Airport Hotels"),
    "best-hotels-private-pool-dubai": ("🏊", "Private Pool Hotels"),
    "best-desert-resorts-dubai": ("🏜️", "Desert Resorts"),
    "best-adults-only-hotels-dubai": ("🍹", "All-Inclusive & Adults-Only"),
    "best-boutique-hotels-dubai": ("🎨", "Boutique Hotels"),
}


def spec(slug):
    return json.loads((ROOT / "scripts" / "articles" / f"{slug}.json").read_text())


def frag(h):
    return BeautifulSoup(h, "html.parser")


def wire_menu(slugs):
    d = json.loads(MENU.read_text())
    dd = next(n for n in d["nav"] if n.get("type") == "dropdown")
    col = dd["columns"][2]
    grp = next((g for g in col["groups"] if g.get("head") == "DUBAI HOTELS"), None)
    if grp is None:
        grp = {"head": "DUBAI HOTELS", "subitems": []}
        col["groups"].insert(0, grp)
    have = {s["href"] for s in grp["subitems"]}
    for sl in slugs:
        if f"/{sl}" not in have:
            e, lab = LABELS[sl]
            grp["subitems"].append({"href": f"/{sl}", "label": f"{e} {lab}"})
    sec = next((s for s in d["drawer"] if s.get("attrs", {}).get("id") == "ltt-mobile-hotels"), None)
    if sec is None:
        sec = {"type": "section", "groups": [{"head": "Dubai Hotels", "items": []}], "attrs": {"id": "ltt-mobile-hotels"}}
        i = next(i for i, s in enumerate(d["drawer"]) if s.get("attrs", {}).get("id") == "ltt-mobile-experiences")
        d["drawer"].insert(i + 1, sec)
    items = sec["groups"][0]["items"]
    have = {s["href"] for s in items}
    for sl in slugs:
        if f"/{sl}" not in have:
            e, lab = LABELS[sl]
            items.append({"href": f"/{sl}", "title": f"{e} {lab}"})
    MENU.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")


def wire_home(slugs):
    s = BeautifulSoup(HOME.read_text(encoding="utf-8"), "html.parser")
    sec = s.select_one("#dubai-hotels")
    if sec is None:
        sec = frag('<section class="ltt-section hp-compact" id="dubai-hotels"><div class="ltt-container">'
                   '<div class="ltt-section-header"><div class="ltt-section-eyebrow">WHERE TO STAY IN DUBAI</div>'
                   '<h2 class="ltt-section-title">Dubai Hotels Compared by Area and Style</h2></div>'
                   '<ul class="hp-guides"></ul></div></section>')
        s.select_one("#guides").insert_after(sec)
        sec = s.select_one("#dubai-hotels")
    ul = sec.select_one("ul.hp-guides")
    have = {a.get("href") for a in ul.select("a.hp-guide")}
    for sl in slugs:
        if f"/{sl}" in have:
            continue
        sp = spec(sl)
        img = sp["items"][0]["photos"][0]
        ul.append(frag(f'<li><a class="hp-guide" href="/{sl}"><img alt="{sp["breadcrumb"]}" decoding="async" height="64" loading="lazy" '
                       f'src="{img}" width="64"/><span class="hp-guide-txt"><h3>{sp["h1"]}</h3></span>'
                       f'<span aria-hidden="true" class="hp-guide-go">›</span></a></li>'))
    HOME.write_text(str(s), encoding="utf-8")


def wire_hub(slugs, page="best-palm-jumeirah-hotels-dubai"):
    p = ROOT / page / "index.html"
    s = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    old = s.select_one("#ltt-more-hotels")
    if old:
        prev = [a["href"].lstrip("/") for a in old.select("a")]
        slugs = prev + [x for x in slugs if x not in prev]
        old.decompose()
    items = "".join(f'<li><a href="/{sl}">{spec(sl)["breadcrumb"]}</a></li>' for sl in slugs)
    block = frag(f'<div class="w-richtext" id="ltt-more-hotels"><h2>More Dubai Hotels, Compared</h2><p>Not set on the Palm? '
                 f'These guides compare hotels in the other parts of Dubai the same way, on price for the same date, guest score and location:</p>'
                 f'<ul role="list">{items}</ul></div>')
    anchor = s.select_one("#ltt-more-dubai")
    if anchor:
        anchor.insert_before(block)
    else:
        (s.select_one("#content .container-33") or s.select_one("main")).append(block)
    p.write_text(str(s), encoding="utf-8")


if __name__ == "__main__":
    slugs = [a for a in sys.argv[1:] if (ROOT / a / "index.html").is_file()]
    missing = [a for a in sys.argv[1:] if a not in slugs]
    if missing:
        sys.exit(f"no page for: {missing}")
    wire_menu(slugs)
    wire_home(slugs)
    wire_hub(slugs)
    print(f"wired {len(slugs)} pages; now run menu.py build, sync_layout.py and generate_sitemap.py")
