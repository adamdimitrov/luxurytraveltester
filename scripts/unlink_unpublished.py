#!/usr/bin/env python3
"""Unwrap internal links to pages that will not be live when these specs ship.

    python3 scripts/unlink_unpublished.py --ship slug1,slug2 [--restore] spec1.json spec2.json ...

A link `<a href="/x">text</a>` in a spec stays only if /x is a live page (an index.html tracked in
git at HEAD) or one of the --ship slugs. Removed links are logged to scripts/articles/pending_links.json
so a later batch can put them back (--restore re-wraps the logged text once the target is live/shipping).
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "scripts" / "articles" / "pending_links.json"


def live_slugs():
    out = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", "HEAD"], capture_output=True, text=True, check=True).stdout
    return {p.split("/")[0] for p in out.splitlines() if p.count("/") == 1 and p.endswith("/index.html")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ship", default="")
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("specs", nargs="+")
    a = ap.parse_args()
    ok = live_slugs() | {s for s in a.ship.split(",") if s}
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    for sp in a.specs:
        p = Path(sp)
        t = p.read_text()
        slug = p.stem
        if a.restore:
            n = 0
            keep = []
            for target, text in log.get(slug, []):
                if target in ok and text in t:
                    t = t.replace(text, f'<a href=\\"/{target}\\">{text}</a>', 1)
                    n += 1
                else:
                    keep.append([target, text])
            log[slug] = keep
            print(f"{slug}: restored {n}")
        else:
            removed = []

            def rep(m):
                target = m.group(1).strip("/").split("#")[0]
                if not target or target in ok:
                    return m.group(0)
                removed.append([target, m.group(2)])
                return m.group(2)

            t = re.sub(r'<a href=\\"(/[a-z0-9-]*/?(?:#[^"\\]*)?)\\">(.*?)</a>', rep, t)
            if removed:
                log.setdefault(slug, []).extend(removed)
            print(f"{slug}: unlinked {len(removed)} -> {sorted({r[0] for r in removed})}")
        json.loads(t)
        p.write_text(t)
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
