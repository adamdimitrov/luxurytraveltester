#!/usr/bin/env python3
"""
Add the three one-pick verdict pages to the site menu on every page
(same pattern as thecruisedetective.com /best-* pages):

- desktop mega menu: a "🏆 ... My Pick" item right after its hub item
- mobile drawer: a "My #1 Picks" section after "Destinations & Guides"

Idempotent: re-running skips pages that already have the items. Run it
before scripts/build_verdict_pages.py, which copies the hub menus.
"""
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PICKS = [
    # hub, verdict slug, mega title, mega subtitle, mobile label
    ('best-desert-safaris-dubai', 'best-desert-safari-dubai', 'Best Desert Safari: My Pick',
     'The one I would book after testing 8', '🏆 Best Desert Safari: My Pick'),
    ('best-palm-jumeirah-hotels-dubai', 'best-palm-jumeirah-hotel-dubai', 'Best Palm Hotel: My Pick',
     'The one I would book after staying at 5', '🏆 Best Palm Jumeirah Hotel: My Pick'),
    ('best-helicopter-tours-new-york', 'best-helicopter-tour-new-york', 'Best NYC Helicopter Tour: My Pick',
     'The one I would book after flying the top 2', '🏆 Best NYC Helicopter Tour: My Pick'),
]

MOBILE_SECTION = '<div class="ltt-mobile-section">\n<div class="ltt-mobile-label">My #1 Picks</div>\n' + ''.join(
    f'<a class="ltt-mobile-link" href="/{slug}">\n<span>{label}</span>\n</a>\n'
    for _, slug, _, _, label in PICKS) + '</div>\n'


def patch(src):
    changed = False
    for hub, slug, title, sub, _ in PICKS:
        if f'class="ltt-mega-item" href="/{slug}"' in src or f'href="/{slug}">\n<span class="ltt-mega-icon">' in src:
            continue
        item = (f'<a class="ltt-mega-item" href="/{slug}">\n<span class="ltt-mega-icon">🏆</span>\n<div>\n'
                f'<strong>{title}</strong>\n<p>{sub}</p>\n</div>\n</a>\n')
        # hub mega item (may carry aria-current / active on the hub itself)
        pat = re.compile(r'(<a (?:aria-current="page" )?class="ltt-mega-item(?: active)?" href="/%s">.*?</a>\n)' % re.escape(hub), re.S)
        src, n = pat.subn(lambda m: m.group(1) + item, src, count=1)
        changed |= bool(n)
    if 'My #1 Picks</div>' not in src:
        pat = re.compile(r'(<div class="ltt-mobile-section">\n<div class="ltt-mobile-label">Destinations &amp; Guides</div>.*?</div>\n)', re.S)
        src, n = pat.subn(lambda m: m.group(1) + MOBILE_SECTION, src, count=1)
        changed |= bool(n)
    return src, changed


if __name__ == '__main__':
    files = subprocess.run(['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for rel in files:
        path = os.path.join(ROOT, rel)
        with open(path, encoding='utf-8') as f:
            src = f.read()
        if 'ltt-mega-menu' not in src:
            continue
        new, changed = patch(src)
        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new)
        print(('patched ' if changed else 'skipped ') + rel)
