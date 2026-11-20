#!/usr/bin/env python3
"""Wire new Dubai experience comparison pages (GetYourGuide specs) into the site. Idempotent.
Replaces the menu part of the older wire_batch.py now that the menu is data (data/menu/en.json).

    python3 scripts/wire_experiences.py best-theme-parks-dubai best-old-dubai-souk-tours ...

- menu: appended to the "DUBAI EXPERIENCES" mega-menu group and the "Dubai Experiences" drawer section;
- homepage: a card in the flagship guides list (#guides);
- contextual links: added to the "More Dubai Experiences, Compared" block on the desert safari page.
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
    "best-theme-parks-dubai": ("🎢", "Theme Parks"),
    "best-old-dubai-souk-tours": ("🕌", "Old Dubai & Souk Tours"),
    "best-abu-dhabi-tours-from-dubai": ("🏛️", "Abu Dhabi Day Trips"),
    "best-boat-tours-dubai": ("🚤", "Boat & Yacht Tours"),
    "best-museums-dubai": ("🖼️", "Museums"),
    "best-photoshoot-dubai": ("📸", "Photoshoots"),
    "best-horse-riding-dubai": ("🐎", "Horse Riding"),
    "best-musandam-tours-dubai": ("🐬", "Musandam Day Trips"),
    "best-kayaking-dubai": ("🛶", "Kayaking"),
    "best-dubai-attraction-passes": ("🎟️", "Attraction Passes"),
    "best-yacht-tours-dubai": ("🛥️", "Yacht Tours"),
}


def spec(slug):
    return json.loads((ROOT / "scripts" / "articles" / f"{slug}.json").read_text())


def frag(h):
    return BeautifulSoup(h, "html.parser")


def wire_menu(slugs):
    d = json.loads(MENU.read_text())
    dd = next(n for n in d["nav"] if n.get("type") == "dropdown")
    grp = next(g for c in dd["columns"] for g in c["groups"] if g.get("head") == "DUBAI EXPERIENCES")
    have = {s["href"] for s in grp["subitems"]}
    for sl in slugs:
        if f"/{sl}" not in have:
            e, lab = LABELS[sl]
            grp["subitems"].append({"href": f"/{sl}", "label": f"{e} {lab}"})
    sec = next(s for s in d["drawer"] if s.get("attrs", {}).get("id") == "ltt-mobile-experiences")
    items = sec["groups"][0]["items"]
    have = {s["href"] for s in items}
    for sl in slugs:
        if f"/{sl}" not in have:
            e, lab = LABELS[sl]
            items.append({"href": f"/{sl}", "title": f"{e} {lab}"})
    MENU.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")


def wire_home(slugs):
    s = BeautifulSoup(HOME.read_text(encoding="utf-8"), "html.parser")
    ul = s.select_one("#guides ul.hp-guides")
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


def wire_related(slugs, page="best-desert-safaris-dubai"):
    p = ROOT / page / "index.html"
    s = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    ul = s.select_one("#ltt-more-dubai ul")
    if ul is None:
        sys.exit(f"no #ltt-more-dubai list on {page}")
    have = {a.get("href") for a in ul.select("a")}
    for sl in slugs:
        if f"/{sl}" not in have:
            ul.append(frag(f'<li><a href="/{sl}">{spec(sl)["breadcrumb"]}</a></li>'))
    p.write_text(str(s), encoding="utf-8")


if __name__ == "__main__":
    slugs = [a for a in sys.argv[1:] if (ROOT / a / "index.html").is_file()]
    missing = [a for a in sys.argv[1:] if a not in slugs]
    if missing:
        sys.exit(f"no page for: {missing}")
    wire_menu(slugs)
    wire_home(slugs)
    wire_related(slugs)
    print(f"wired {len(slugs)} pages; now run menu.py build, sync_layout.py and generate_sitemap.py")
