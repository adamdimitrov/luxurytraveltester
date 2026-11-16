---
name: new-article
description: Create a new "best X" comparison article on luxurytraveltester.com from live GetYourGuide/Tiqets listings - topic gate, harvest listings in the user's Chrome, write a JSON spec, build it with scripts/build_article.py, wire it into the site, run /qc-article until clean. Use when the user says new article, write about X, or a /cover-keywords batch runs on LTT.
---

# /new-article (Luxury Travel Tester)

Pipeline: **gate → harvest → spec → build → wire → /qc-article → ship**. Same rules as the Cruise Detective pipeline; the LTT difference is that pages are generated from `scripts/articles/<slug>.json` by `scripts/build_article.py` (shell = best-desert-safaris-dubai), never hand-copied.

## 0. Worktree
Global rule: work in a worktree branch, never the main checkout.

## 1. Topic gate (3-6 lines)
- One buying intent, not covered by an existing page (grep slugs, sitemap.xml, search index). Product overlap with any existing page ≤ 50%.
- 5+ genuinely different bookable products on GetYourGuide/Tiqets (price, duration, what's included, pickup, private vs shared). If fewer, merge into a broader best-X page or stop.
- Room on page 1 (look at the top results in the user's Chrome).

## 2. Harvest (user's Chrome, GYG tab, same-origin fetch)
In a getyourguide.com tab define a fetcher that reads each product page's JSON-LD (`Product` name, `aggregateRating`, `offers.lowPrice`) and the gallery (`"type":"activityImage"` ids, 64-hex). **Pace it: one request every ~9 s and back off 2 min on 429**; GYG's Cloudflare blocks bursts and we never try to bypass a challenge. Export via an injected `<article>` + `get_page_text` (javascript_tool output is cut at ~1 KB and blocks query strings).
Record per product: name, rating, review count, from-price, duration, meeting point/pickup, included/excluded, languages, cancellation, 9-10 gallery ids.
Tiqets: if the same product is on Tiqets, look up its est. commission in the affiliate portal; Tiqets wins above 11%.

## 3. Spec
Write `scripts/articles/<slug>.json` (format: `scripts/articles/README.md`). Load the growandconvert-content skill for copy. Mandatory:
- Original side-by-side analysis in `guide` (comparison table with the real decision axes, price per hour/person, what's extra, pickup vs meet-there, best time).
- Every card: specific Pick it / Skip it, ≤ 4 pills, each pill a dropdown that adds facts.
- No "tested" unless the user tested it; no invented experience; no em dashes; no OTA names or review totals in title/meta/intro; no platform narration; no "prices checked on" lines.

## 4. Build
```bash
python3 scripts/build_article.py --photos scripts/articles/<slug>.json
```
Fix any "shell words left" warning (leftover safari copy) in the spec or builder.

## 5. Wire
- Menu: add the page to the layout master (`scripts/layout_config.json` → masters.en), then `python3 scripts/sync_layout.py`.
- Homepage card/link, contextual links in from 2+ related live pages and out to related money pages.
- `python3 scripts/generate_sitemap.py`; update the canonical count in GEMINI.md.

## 6. QC
`/qc-article` (automated `qc_article.py` + judgment checklist), ideally by a reviewer that did not write the spec. Fix until PASS. HOLD anything unresolved.

## 7. Ship
`/ship`-style: commit, PR, merge, Search Console sitemap + indexing. For /cover-keywords batches the user allows publishing without preview approval (memory: backlog-batches-auto-publish); everything else stops at the preview link.
