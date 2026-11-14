#!/usr/bin/env python3
"""Make every affiliate / OTA / booking-partner link carry
rel="nofollow sponsored noopener".

Idempotent. Only the rel attribute of matching <a> tags changes; hrefs,
tracking parameters, target and link text are left as they are. Other rel
tokens are kept, missing ones are appended, nothing is duplicated.

Scans served HTML plus the generators / templates that emit links
(*.py, *.js, *.json, *.md outside .git/.claude/node_modules).

    python3 scripts/fix_affiliate_rel.py            # fix in place, print counts
    python3 scripts/fix_affiliate_rel.py --check    # exit 1 if any link is missing tokens
    python3 scripts/fix_affiliate_rel.py --report   # per-file before counts, no writes

scripts/sync_layout.py calls run() too, so `sync_layout.py` fixes these links
and `sync_layout.py --check` (the CI layout check) fails on a missing token.
"""
import html
import os
import re
import sys
from urllib.parse import urlsplit, parse_qsl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ("nofollow", "sponsored", "noopener")
SKIP_DIRS = {".git", ".claude", "node_modules", ".vercel"}
EXTS = (".html", ".py", ".js", ".json", ".md")

# Hosts that are always affiliate / OTA / booking partners (suffix match).
AFFILIATE_HOSTS = (
    "getyourguide.com", "tiqets.com", "viator.com", "fareharbor.com",
    "tp.media", "tpm.lv", "travelpayouts.com", "tp.st",
    "booking.com", "expedia.com", "hotels.com", "trip.com", "agoda.com",
    "klook.com", "musement.com", "civitatis.com", "headout.com",
    "awin1.com", "prf.hn", "go2cloud.org", "flynyon.com",
)
# tripadvisor.<any tld>
TRIPADVISOR_RE = re.compile(r"(^|\.)tripadvisor\.[a-z.]+$")
# Any other host with one of these query params counts as affiliate.
AFFILIATE_PARAMS = {"partner_id", "partner", "ref", "aid", "affiliate",
                    "affiliate_id", "affid", "marker", "pid", "sub_id"}

A_TAG_RE = re.compile(r"<a\b[^>]*>", re.I | re.S)
HREF_RE = re.compile(r"""\bhref\s*=\s*(["'])(.*?)\1""", re.I | re.S)
REL_RE = re.compile(r"""\brel\s*=\s*(["'])(.*?)\1""", re.I | re.S)


def is_affiliate(href: str) -> bool:
    href = html.unescape(href).strip()
    if href.startswith("//"):
        href = "https:" + href
    if not href.lower().startswith(("http://", "https://")):
        return False
    try:
        parts = urlsplit(href)
    except ValueError:
        return False
    host = (parts.hostname or "").lower()
    if not host or host.endswith("luxurytraveltester.com"):
        return False
    if any(host == h or host.endswith("." + h) for h in AFFILIATE_HOSTS):
        return True
    if TRIPADVISOR_RE.search(host):
        return True
    keys = {k.lower() for k, _ in parse_qsl(parts.query, keep_blank_values=True)}
    return bool(keys & AFFILIATE_PARAMS)


def fix_tag(tag: str):
    """Return (new_tag, was_affiliate, was_missing)."""
    m = HREF_RE.search(tag)
    if not m or "{" in m.group(2) and not m.group(2).startswith("http"):
        # Template placeholder like href="{h["link"]}": can't judge the host.
        return tag, False, False
    if not is_affiliate(m.group(2)):
        return tag, False, False
    r = REL_RE.search(tag)
    tokens = r.group(2).split() if r else []
    lower = [t.lower() for t in tokens]
    missing = [t for t in REQUIRED if t not in lower]
    if not missing:
        return tag, True, False
    if r:
        q = r.group(1)
        new_rel = f"rel={q}{' '.join(tokens + missing)}{q}"
        tag = tag[:r.start()] + new_rel + tag[r.end():]
    else:
        q = m.group(1)
        insert = f" rel={q}{' '.join(REQUIRED)}{q}"
        tag = tag[:m.end()] + insert + tag[m.end():]
    return tag, True, True


def process(text: str):
    stats = {"affiliate": 0, "fixed": 0}

    def sub(mo):
        new, aff, miss = fix_tag(mo.group(0))
        stats["affiliate"] += aff
        stats["fixed"] += miss
        return new

    return A_TAG_RE.sub(sub, text), stats


def iter_files():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith(EXTS) and f != "fix_affiliate_rel.py":
                yield os.path.join(d, f)


def run(write: bool):
    """Scan (and with write=True fix) every file. Returns [(relpath, affiliate, missing)]."""
    rows = []
    for path in sorted(iter_files()):
        with open(path, encoding="utf-8", errors="surrogateescape") as fh:
            text = fh.read()
        new, st = process(text)
        if not st["affiliate"]:
            continue
        rows.append((os.path.relpath(path, ROOT), st["affiliate"], st["fixed"]))
        if write and new != text:
            with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(new)
    return rows


def main():
    check = "--check" in sys.argv
    report = "--report" in sys.argv
    rows = run(write=not (check or report))
    total_aff = sum(r[1] for r in rows)
    total_fixed = sum(r[2] for r in rows)
    width = max((len(r[0]) for r in rows), default=10)
    label = "missing" if (check or report) else "fixed"
    for rel, a, f in rows:
        if f or report:
            print(f"{rel:<{width}}  affiliate={a:<4} {label}={f}")
    print(f"TOTAL affiliate links={total_aff} {label}={total_fixed} files={len(rows)}")
    if check and total_fixed:
        print("FAIL: affiliate links without rel=\"nofollow sponsored noopener\". "
              "Fix with: python3 scripts/fix_affiliate_rel.py", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
