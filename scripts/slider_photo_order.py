"""Order card slider photos so each sequence sells the card's promise.

First photo = the single strongest shot for the card's promise, then the story
(venue/boat, food/drinks, views, details). Off-topic shots (menus, payment
graphics, text boards, near-duplicates) are dropped. Orders were picked by
looking at contact sheets of every card, not by filename.

PHOTO_ORDER keys are page -> card number (1-based slider index on the page),
values are 1-based indexes into the card's current photo list. Indexes not
listed are dropped. The same order is applied to every language version that
uses the bpa-slider deck. The site is English only, so one file per page.

Usage: python3 scripts/slider_photo_order.py [--check]
"""
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent

PHOTO_ORDER = {
    "best-desert-safaris-dubai": {
        1: [  # buggy on the red dunes
            "68a1c9f3d9abe6be947799ac",
            "68a1c9f3d9abe6be94779993",
            "68a1c9f3d9abe6be9477999f",
            "68a1c9f3d9abe6be94779999",
            "68a1c9f3d9abe6be9477998e",
            "68a1c9f3d9abe6be947799a4",
        ],
        2: [  # camel ride in the dunes
            "68e1151e4c60e2add221d6f4",
            "68e117ff4c1750300b0a4cb7",
            "68a1c9f3d9abe6be947799d8",
            "68e11588728be1dc52f7cf27",
            "68e115dca6aa11f03c9e9c17",
            "68e1167b9bd27e94b9848be6",
            "68e1147cf593b354278d1a4e",
        ],
        3: [  # with the camel at the lit camp; drop printed flyer
            "68a1c9f3d9abe6be94779a32",
            "68e119569a3536f1e2ebb202",
            "68a1c9f3d9abe6be94779a27",
            "68a1c9f3d9abe6be94779a3d",
            "68e118908a57a7b5bdb69f34",
            "68e119cca6aa11f03c9f1294",
        ],
        4: [  # dune bashing in convoy
            "68a1c9f3d9abe6be94779a53",
            "68a1c9f3d9abe6be94779a74",
            "68a1c9f3d9abe6be94779a69",
            "68a1c9f3d9abe6be94779a80",
            "68a1c9f3d9abe6be94779a5e",
            "68e11d9c489d43d06d5c1f6b",
        ],
        5: [  # the vintage Land Rovers in the dunes
            "6928407a5b47e62eda4eeffd",
            "6928408cad4df7cbc00015d7",
            "69284089893d82ace6570519",
            "6928408da590daee17d28d9d",
            "6928408ca7118d680917b81f",
            "6928407f04d977e586b9b13f",
            "6928408d3e8d10b11d80f95f",
        ],
        6: [  # fire show in the desert
            "68a1c9f3d9abe6be94779a8b",
            "68a1c9f3d9abe6be94779aa1",
            "68a1c9f3d9abe6be94779aac",
            "68a1c9f3d9abe6be94779ab7",
            "68a1c9f3d9abe6be94779ac2",
            "68a1c9f3d9abe6be94779a96",
            "68a1c9f3d9abe6be94779acd",
        ],
        7: [  # sunrise over the dunes
            "68a1c9f3d9abe6be94779ae4",
            "68a1c9f3d9abe6be94779aed",
            "68a1c9f3d9abe6be94779ae1",
            "68a1c9f3d9abe6be94779aea",
            "68a1c9f3d9abe6be94779ae7",
            "68a1c9f3d9abe6be94779ade",
            "68a1c9f3d9abe6be94779ada",
        ],
    },
    "best-helicopter-tours-new-york": {
        1: [  # doors-off shoe selfie over Manhattan
            "6a47d3559ce91814c1df86f5",
            "6a3e93b4bf6f86ab17454b8d",
            "6a3e93b2e28f970c7412e70a",
            "6a4d3fc57f5b3867f83d5252",
            "6a3e93b5dcf4456feae7623e",
            "6a3e93b50943913cb88f4f15",
            "6a3e93b46620ac3fe0404510",
            "6a3e93b211878b3a96768334",
            "6a3e93b3a38fb94347f05413",
            "6a3e93b311f008c657a3bf3b",
            "6a3e93b3e1d5c0fa7380cb30",
            "6a3e93b361a3bd3efb23ed61",
            "6a3e93b48f0b68f713944d36",
            "6a3e93b210a69bc70a9e3411",
            "6a3e93b210fffa63fd5c45a8",
            "6a3e93b3f05dcdce2b1827b2",
            "6a3e93b356b7deb3a7017eac",
            "6a3e93b3299abbd41fe277b8",
        ],
        2: [  # Statue of Liberty from above; drop HeliNY logo screen
            "6a47dd8fbfa2dfc7559687ec",
            "6a47daf5c9ff2d5bf8d7508d",
            "6a47daf7b93c1b54617a3f13",
            "6a47daf77f4dc7d7180b895c",
            "6a47daf594f0a6341fe351db",
            "6a47daf71bd96559fa923d8f",
            "6a47daf5e65c811a8d65cb83",
            "6a47daf82994b45745fc6026",
            "6a47daf7e7a9ec87627f2a43",
            "6a47daf70dd18fd3b6f5cc27",
            "6a47daf78ebd68066b64c4a1",
        ],
        3: [  # helicopter passing the Statue of Liberty
            "6a49159eb550267ae3150903",
            "6a49159ed30e0dd535134b67",
            "6a49159e75e49a6ca9881c84",
            "6a49159e041c2a759ca559ff",
            "6a49159cf200933aba6c0701",
            "6a49159e215abbb8f21d7487",
            "6a49159de6393d203487a9b3",
            "6a49159e2f2b3aa805a18fd0",
        ],
        4: [  # skyline from the cockpit
            "6a491665d0e0f799d7955f37",
            "6a49166603ad4172d1a3b009",
            "6a491666a4873ec6180f8a63",
            "6a491666de2bced790ce3faf",
            "6a491665bef554b822b82057",
            "6a4916667d3b027f52b893b6",
            "6a4916664ece1b870de05d64",
            "6a49166670325ae14a945479",
            "6a4916668a1508d3eae97f40",
        ],
        5: [  # One World Trade from the cockpit at dusk
            "6a4919b54480068d7c8c5528",
            "6a4919b50a823a381952a387",
            "6a4919b487e679d5400c6ac7",
            "6a4919b567feb6e78cfda437",
            "6a4919b570325ae14a94e501",
            "6a4919b53052977cb135f301",
            "6a4919b5da8eb02bf62f9187",
            "6a4919b388f8dc3c9b651118",
            "6a4919b50a823a381952a36e",
        ],
    },
    "best-palm-jumeirah-hotels-dubai": {
        1: [  # Atlantis facade from the beach
            "68d00c728bf6d88cc1f839c1",
            "6839de1aeab4b121a1c66802",
            "6839db657624ed14a717b907",
            "688b5fba3db74958b61bea66",
            "6839ade52b0a09425b144743",
            "6839ddc652e38ea3363ff3f9",
            "682c7eff0229e52c41702a8a",
            "682db6ea3e5b974ad3bce559",
            "68398aaa2d3ce3fc474ed302",
            "689005d293d0d395be15582f",
        ],
        2: [  # Cloud 22 infinity pool with the skyline
            "689466dd0d525e1eb6e4c4a1",
            "68d00c723b22d1f981e039f3",
            "6894602ff9d372c730c7032e",
            "68900e49b4f740bb5a9dbc5e",
            "6891b1edec2bbcfee65a41c4",
            "6894656d821dd89d517baf7c",
            "689466673af77a3b434b6a50",
            "689464e0e695e42d76fad223",
            "689037caf058589e139e2893",
            "6890270565d6553560b74296",
        ],
        3: [  # aerial with the overwater villas
            "68d00c723ad453c89e94bd71",
            "68a1e2cdfff9efe619730c51",
            "6852e1a09cc817e56296d319",
            "6852eea347f0a6f04aed6ee8",
            "6852e1edac72dedab665044b",
            "6852e10390f7761e2dd4f991",
            "689da07c5efee7bf2aef929e",
            "6852e18bed7479bca8e1af58",
            "689ef25fa02514dac8923903",
            "6852f0d6261c0f64266c9165",
        ],
        4: [  # pool through the iconic frame
            "689db9323a7628e6dc9eccee",
            "6853f1ce78ae0e3b1f660173",
            "6853f57ccce8175a0ea26886",
            "6853f4e178da16599d88eb2a",
            "6853f37a6709cae4adf5b19e",
            "6853f4f81ae085b6b40e2fe7",
            "6853f88335e90e76a8fc36db",
            "6853f5bf5001118df6842673",
            "68a2fd769101044f51fc11df",
            "68a2fc4b36d34c60b9eff4c3",
        ],
    },
}

SLIDER_RE = re.compile(r'<div[^>]*class="bpa-slider"')
IMG_RE = re.compile(r"<img [^>]*>")
LD_LOG = []
PILL_RE = re.compile(r'(<span class="bpa-pill">1 / )(\d+)(</span>)')


def balanced_end(h, start):
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", h[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div")


def img_url(im):
    m = re.search(r'data-src="([^"]+)"', im) or re.search(r' src="([^"]+)"', im)
    return m.group(1)


def attr(im, name):
    m = re.search(r'\s%s="[^"]*"' % name, im)
    return m.group(0) if m else None


def fill_slot(template, im):
    """Put photo `im` into the slot `template` (keeps the slot's loading attrs)."""
    out = template
    out = re.sub(r'\salt="[^"]*"', lambda _: attr(im, "alt") or ' alt=""', out, count=1)
    u = img_url(im)
    if 'data-src="' in out:
        out = re.sub(r'data-src="[^"]*"', lambda _: 'data-src="%s"' % u, out, count=1)
    else:
        out = re.sub(r' src="[^"]*"', lambda _: ' src="%s"' % u, out, count=1)
    # responsive variants travel with the photo
    ss = re.search(r'\s(?:data-)?srcset="([^"]*)"', im)
    if ss:
        out = re.sub(r'(\s(?:data-)?srcset=")[^"]*"', lambda m: m.group(1) + ss.group(1) + '"', out, count=1)
    else:
        out = re.sub(r'\s(?:data-)?srcset="[^"]*"', "", out, count=1)
    oe_t, oe_i = attr(out, "onerror"), attr(im, "onerror")
    if oe_t and oe_i:
        out = out.replace(oe_t, oe_i, 1)
    return out


def norm(u):
    """Compare slider URLs (&amp;, spaces) with JSON-LD URLs (%26, %20)."""
    return unquote(html.unescape(u)).lstrip("/")


def ld_url(u, like):
    return ("/" if like.startswith("/") else "") + quote(norm(u), safe="/:()")


def cluster_files(page):
    return [("en", ROOT / page / "index.html")]


def photo_key(u):
    """Webflow asset hash when there is one, else the file name."""
    b = norm(u).split("/")[-1]
    m = re.match(r"([0-9a-f]{24})_", b)
    return m.group(1) if m else b


class MissingPhoto(Exception):
    pass


def reorder_page(h, orders):
    sliders = []
    for m in SLIDER_RE.finditer(h):
        sliders.append((m.start(), balanced_end(h, m.start())))
    urls = [[img_url(i) for i in IMG_RE.findall(h[a:b])] for a, b in sliders]
    first_swaps = []
    card_lists = {}
    for idx in sorted(orders, reverse=True):
        order = orders[idx]
        a, b = sliders[idx - 1]
        s = h[a:b]
        imgs = IMG_RE.findall(s)
        by_key = {photo_key(img_url(i)): i for i in imgs}
        new = []
        for k in order:
            if k in by_key:
                new.append(by_key[k])
            elif k.startswith("/assets/") and (ROOT / k.lstrip("/")).exists():
                # a photo added to the card: same alt as the card's other photos
                new.append('<img%s src="%s"/>' % (attr(imgs[0], "alt") or ' alt=""', k))
            else:
                raise MissingPhoto((idx, k))
        card_lists[idx] = ([img_url(i) for i in imgs], [img_url(i) for i in new])
        rest_t = imgs[1] if len(imgs) > 1 else imgs[0]
        tags = [fill_slot(imgs[0], new[0])] + [fill_slot(rest_t, im) for im in new[1:]]
        head = s[:s.find("<img ")]
        tail = s[s.rfind(">", 0, s.rfind("</div>")) + 1:]
        # keep the separator used between tags
        sep = "\n" if "\n<img " in s else ""
        new_s = head + sep.join(tags) + tail
        pre_start = h.rfind('<div class="bpa-media"', 0, a)
        pre = h[pre_start:a]
        pre_new, n = PILL_RE.subn(lambda m: m.group(1) + str(len(order)) + m.group(3), pre)
        assert n <= 1
        h = h[:pre_start] + pre_new + new_s + h[b:]
        if img_url(imgs[0]) != img_url(new[0]):
            first_swaps.append((idx, img_url(imgs[0]), img_url(new[0])))
    # JSON-LD: each card's ListItem image (and the Article lead image for card 1)
    # follows the card's first photo. Replace as text to keep the formatting, but
    # only when every occurrence of the old URL sits in one of those spots.
    def fix_ld(m):
        block = m.group(0)
        body = block[block.find(">") + 1:block.rfind("<")]
        try:
            data = json.loads(body)
        except ValueError:
            return block
        nodes = []
        def walk(o):
            if isinstance(o, dict):
                nodes.append(o)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        def imgs_of(o):
            im = o.get("image")
            if isinstance(im, str):
                return [im]
            if isinstance(im, list):
                return [x for x in im if isinstance(x, str)]
            return []
        def count(lst, u):
            return sum(1 for x in lst if norm(x).endswith(norm(u)))
        for idx, old, new_u in first_swaps:
            allowed = 0
            for n in nodes:
                if n.get("@type") == "ListItem" and n.get("position") == idx and isinstance(n.get("item"), dict):
                    allowed += count(imgs_of(n["item"]), old)
                if idx == 1 and n.get("@type") in ("Article", "BlogPosting", "WebPage"):
                    allowed += count(imgs_of(n), old)
            total = sum(count(imgs_of(n), old) for n in nodes)
            spellings = {x for x in re.findall(r'"([^"]+)"', block)
                         if "/assets/" in x and norm(x).endswith(norm(old))}
            if allowed and allowed == total and sum(block.count('"%s"' % x) for x in spellings) == allowed:
                for x in spellings:
                    block = block.replace('"%s"' % x, '"%s%s"' % (x[:x.find("/assets/")], ld_url(new_u, "/")))
                LD_LOG.append((idx, "ok"))
            elif total:
                LD_LOG.append((idx, "skip: old url also used elsewhere (%d/%d)" % (allowed, total)))
        # Multi-photo image lists made from one card's slider (hostels): follow
        # the new slider order, drop removed photos, lead with the new first photo.
        def fix_list(lm):
            items = re.findall(r'"([^"]*)"', lm.group(2))
            if len(items) < 2:
                return lm.group(0)
            for idx, (old_list, new_list) in card_lists.items():
                old_n = [norm(u) for u in old_list]
                if not all(norm(u) in old_n for u in items):
                    continue
                new_n = [norm(u) for u in new_list]
                kept = sorted([u for u in items if norm(u) in new_n], key=lambda u: new_n.index(norm(u)))
                if not kept or norm(kept[0]) != new_n[0]:
                    kept = [ld_url(new_list[0], items[0])] + kept
                kept = kept[:len(items)]
                if kept == items:
                    return lm.group(0)
                inner = lm.group(2)
                lead = re.match(r'\s*', inner).group(0)
                trail = re.search(r'\s*$', inner).group(0)
                sep = re.search(r'",(\s*)"', inner)
                sep = "," + (sep.group(1) if sep else " ")
                LD_LOG.append((idx, "list reordered"))
                return lm.group(1) + lead + sep.join('"%s"' % u for u in kept) + trail + "]"
            return lm.group(0)
        block = re.sub(r'("image":\s*\[)([^\]]*)\]', fix_list, block)
        return block
    h = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', fix_ld, h, flags=re.S)
    return h, urls, first_swaps


def main():
    check = "--check" in sys.argv
    report = {}
    for page, orders in PHOTO_ORDER.items():
        files = cluster_files(page)
        done, skipped = [], []
        for lang, f in files:
            h = f.read_text()
            if 'class="bpa-slider"' not in h:
                skipped.append(lang + " (old w-slider template)")
                continue
            try:
                new_h, urls, _ = reorder_page(h, orders)
            except MissingPhoto as e:
                skipped.append("%s (different photo set: %s)" % (lang, e))
                continue
            if new_h != h:
                if not check:
                    f.write_text(new_h)
                done.append(lang)
        report[page] = {"changed": done, "skipped": skipped}
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
