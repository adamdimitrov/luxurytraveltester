#!/usr/bin/env python3
"""Wire a batch of new articles into the site: menu (layout master), mobile drawer,
homepage guide list, and contextual "more Dubai experiences" links on the existing
Dubai money pages. Idempotent. Then run generate_sitemap.py and sync_layout.py.

    python3 scripts/wire_batch.py best-water-parks-dubai best-burj-khalifa-tickets ...
"""
import json, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "best-desert-safaris-dubai" / "index.html"
HOME = ROOT / "index.html"
LABELS = {
    "best-water-parks-dubai": ("💦", "Water Parks"),
    "best-burj-khalifa-tickets": ("🏙️", "Burj Khalifa Tickets"),
    "best-adrenaline-experiences-dubai": ("🪂", "Skydive & Adrenaline"),
    "best-hot-air-balloon-dubai": ("🎈", "Hot Air Balloon Rides"),
    "best-helicopter-tours-dubai": ("🚁", "Helicopter Tours"),
    "best-scuba-diving-dubai": ("🤿", "Scuba Diving"),
    "best-dinner-cruises-dubai": ("🍽️", "Dinner Cruises"),
    "best-dune-buggy-tours-dubai": ("🏎️", "Dune Buggy Tours"),
    "best-dubai-city-tours": ("🗺️", "City Tours"),
    "best-jet-ski-tours-dubai": ("🌊", "Jet Ski Tours"),
}


def spec(slug):
    return json.loads((ROOT / "scripts" / "articles" / f"{slug}.json").read_text())


def frag(html):
    return BeautifulSoup(html, "html.parser")


def wire_menu(slugs):
    s = BeautifulSoup(MASTER.read_text(encoding="utf-8"), "html.parser")
    h = s.select_one("header.ltt-navbar")
    mega = h.select_one(".ltt-mega-menu")
    if not mega.select_one("#ltt-mega-experiences"):
        links = "".join(f'<a class="ltt-mega-subitem" href="/{sl}">{LABELS[sl][0]} {LABELS[sl][1]}</a>' for sl in slugs)
        col = frag(f'<div class="ltt-mega-col" id="ltt-mega-experiences"><div class="ltt-mega-head">DUBAI EXPERIENCES</div><div>{links}</div></div>')
        first = mega.select_one(".ltt-mega-col")
        first.insert_after(col)
    mob = h.select_one(".ltt-mobile-section")
    if mob and not h.select_one("#ltt-mobile-experiences"):
        links = "".join(f'<a class="ltt-mobile-link" href="/{sl}"><span>{LABELS[sl][0]} {LABELS[sl][1]}</span></a>' for sl in slugs)
        mob.insert_after(frag(f'<div class="ltt-mobile-section" id="ltt-mobile-experiences"><div class="ltt-mobile-label">Dubai Experiences</div>{links}</div>'))
    if "ltt-mega-experiences-css" not in str(s.head):
        s.head.append(frag('<style id="ltt-mega-experiences-css">#ltt-mega-experiences .ltt-mega-subitem{display:block}'
                           '#ltt-mega-experiences .ltt-mega-subitem:hover{color:#855a00}</style>'))
    MASTER.write_text(str(s), encoding="utf-8")


def wire_home(slugs):
    s = BeautifulSoup(HOME.read_text(encoding="utf-8"), "html.parser")
    ul = s.select_one("ul.hp-guides")
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


def wire_related(slugs, page, intro):
    p = ROOT / page / "index.html"
    s = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    if s.select_one("#ltt-more-dubai"):
        s.select_one("#ltt-more-dubai").decompose()
    items = "".join(f'<li><a href="/{sl}">{spec(sl)["breadcrumb"]}</a></li>' for sl in slugs)
    block = frag(f'<div class="w-richtext" id="ltt-more-dubai"><h2>{intro}</h2><p>Planning the rest of your Dubai days? These side-by-side guides compare the other bookable experiences the same way:</p><ul role="list">{items}</ul></div>'
                 '<style id="ltt-more-dubai-css">#ltt-more-dubai{margin:36px 0 0}#ltt-more-dubai a{color:#855a00;font-weight:600}#ltt-more-dubai a:hover{color:#5c3e00}</style>')
    cont = s.select_one("#content .container-33") or s.select_one("main")
    cont.append(block)
    p.write_text(str(s), encoding="utf-8")


if __name__ == "__main__":
    slugs = [a for a in sys.argv[1:] if (ROOT / a / "index.html").is_file()]
    print("wiring", len(slugs), "pages")
    wire_menu(slugs)
    wire_home(slugs)
    wire_related(slugs, "best-desert-safaris-dubai", "More Dubai Experiences, Compared")
    wire_related(slugs, "best-palm-jumeirah-hotels-dubai", "Things to Book Around Your Palm Stay")
    print("done; now run generate_sitemap.py and sync_layout.py")
