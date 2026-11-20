# Writer brief: one LTT "best X in Dubai" article

Repo (worktree): `/Users/adamdimitrov/Development/luxurytraveltester/worktrees/backlog-dubai`. Work ONLY on your own files:
`scripts/articles/<slug>.json`, `assets/<slug>/`, `<slug>/index.html`. Do not edit menus, homepage, sitemap, other pages, the builder or the shell. Do not commit, push or use git. No browser needed.

## Inputs
- Harvested live GetYourGuide data (checked today): `scripts/articles/harvest/<topic>.json` — per product: `p` (GYG path), `name`, `rating`, `reviews`, `price` (EUR from-price), `desc`, `gallery` (image ids), `text` (listing text: cancellation, duration, languages, highlights, description, sometimes includes/meeting point), `search_card`.
- Spec format: `scripts/articles/README.md`. Example of a finished page's look: `best-desert-safaris-dubai/index.html` (the builder uses its shell).
- Copy style: read `~/.claude/skills/growandconvert-content/SKILL.md` and follow it.

## Steps
1. Read your harvest file. Drop products that duplicate another (same thing sold twice) unless the difference matters; keep 6-8 genuinely different options. Rank them honestly (best overall first, then distinct "best for" picks).
2. Write `scripts/articles/<slug>.json`. Use only facts present in the harvest data. If a fact (meeting point, what's included, languages) is not in the data, leave it out. Never invent.
3. Build: `python3 scripts/build_article.py --photos scripts/articles/<slug>.json`
4. QC: `python3 ~/.claude/skills/qc-article/qc_article.py --site-dir . --page <slug>/index.html` — fix every FAIL except the `[wiring]` ones (sitemap/menu/homepage/inbound links are done later by the orchestrator). Rebuild and re-run until only wiring fails remain. Also aim for 2+ internal links OUT of the guide copy (see "Links").
5. Re-read your built page's text once as a strict editor (step 2 rules below) and fix anything off.
6. Final message: slug, number of cards, a table (rank, product id, title, price, rating/reviews), anything you dropped and why, and any rule you could not satisfy.

## Content rules (hard)
- Title tag ≤ 60 chars, format like "8 Best Helicopter Tours in Dubai (2026): Prices Compared". Meta 110-160 chars. No em dashes (—) anywhere: use commas, colons, periods. En dash only in ranges (12–25 minutes, €175–437).
- Never say tested / personally tested / I tried / we tried / field-tested. The user has not done these. The value is the side-by-side comparison. author_role example: "8 helicopter flights compared on flight time, route, price per minute and pickup".
- No OTA names (GetYourGuide, Viator, Tripadvisor, Tiqets) and no review totals in title, meta, h1, lead. No "GetYourGuide showed…", no "only N spots left", no "prices checked on <date>", no "to keep this honest", no "based on listings". Card buttons/badges already name the booking site; that's fine.
- Lead (2-4 short paragraphs): answer the buying question immediately (which one to book for whom, with a concrete number), then what decides it. No "Dubai is a city of…" openers. No AI tells: delve, whether you're, in the heart of, unforgettable, nestled, look no further, embark, tapestry, elevate.
- Every card: specific `pick` ("for … because …") and `skip` ("if …"); 6-8 pills (two full rows, like the river cruise cards on budapestadventures), in this order: 🕒 start times/duration (`"kind": "time"`), 🗣️ languages, ♿ access & kids (`"kind": "access"`), 2-4 pills on what you actually get, then the vibe (`"kind": "vibe"`); each pill's `body` adds facts not in its label (e.g. label "12 min" → body: route, seat count, what you see). `pros`/`cons` 3-5 each, concrete.
- `review`: 2-4 paragraphs of original analysis per product: what you actually get for the money, how it differs from the neighbours, who it suits, catches (extras, timing, pickup). Facts only from data.
- `guide` (mandatory, this is the page's value): at least
  1. a side-by-side comparison table (`<div class="ltt-guide-tablewrap"><table>…</table></div>`) on the real decision axes for this topic (e.g. price, duration, price per minute/hour, pickup, private/shared, what's included), with computed numbers;
  2. "Which one should you book?" decision section;
  3. practical section (best time, what to bring, how to get there, what costs extra) using only data you have.
- `faqs`: 5-7 real buyer questions with direct answers.
- `methodology`: short, positive: what was compared (number of options, the axes, live listing prices for a normal date). No apologies.
- `filters`: 3-5 buyer-intent filters with emoji labels, `cat` values used on items.
- rank_class: #1 bpa-gold, #2 bpa-silver, #3 bpa-bronze, rest bpa-accent. rank_tag like "🏆 #1 Best Overall", "🥈 #2 Best Value", "🥉 #3 Most Luxurious", "⭐ #4 Best for Families".
- `photo_slug`: short kebab of the product (e.g. "palm-12min"). `short_title` ≤ 45 chars.
- `price_unit`: "per person" unless the listing is per group/vehicle (then say e.g. "per buggy (2 seats)").
- `trust`: only what the listing states (e.g. "Free cancellation up to 24 hours before", "Pickup included", "Reserve now, pay later").

## Links (internal, put them in guide/faq copy as `<a href="/slug">anchor</a>`)
Live pages: `/best-desert-safaris-dubai` (10 desert safaris compared), `/best-palm-jumeirah-hotels-dubai` (Palm hotels), `/best-desert-safari-dubai` (one-pick safari verdict).
Sibling pages publishing in the same batch (link where genuinely relevant): `/best-water-parks-dubai`, `/best-burj-khalifa-tickets`, `/best-adrenaline-experiences-dubai`, `/best-hot-air-balloon-dubai`, `/best-helicopter-tours-dubai`, `/best-scuba-diving-dubai`, `/best-dinner-cruises-dubai`, `/best-dune-buggy-tours-dubai`, `/best-dubai-city-tours`, `/best-jet-ski-tours-dubai`.
