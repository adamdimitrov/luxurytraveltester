# Writer brief: one LTT "best hotels in <area> Dubai" article (Booking.com via Travelpayouts)

Same pipeline and hard rules as `WRITER_BRIEF.md` (read it first). This file lists only what differs for hotel pages.
Work ONLY on your own files: `scripts/articles/<slug>.json`, `assets/<slug>/`, `<slug>/index.html`. No git, no browser, no menus/homepage/sitemap/builder edits.

## Inputs
`scripts/articles/harvest/<topic>.json`, harvested live from Booking.com for **13–14 January 2027, 1 night, 2 adults, prices in EUR**:
- `cards[]`: search-result cards (name, url, stars, score text "Scored 9.1 … 994 reviews", `price` = cheapest nightly price for that date, `text` = full card text incl. taxes line and distance).
- `hotels[]`: the hotel pages: `name`, `url`, `card`, `ld` (description, address, rating, reviews), `desc` (Booking property description), `highlights`, `popular` (top facilities), `facilities`, `rules` (check-in/out, children, cots/extra beds, pets, cards), `rooms[]` (room table rows: room name, beds, size, what the rate includes/excludes, taxes, breakfast, cancellation, price), `subscores` (Location, Cleanliness, Value…), `photos[]` (`id`, `k`, `alt` = Booking caption).

## Page rules
- **10 hotels** (memory: listicle-ten-options-minimum). Genuinely different: price levels, styles (resort, city, apartments), brands, positions. If the harvest can't give 10 real options, take fewer and say so in your final message (never pad).
- Never "tested", "stayed", "we slept", "I tried". The value is the side-by-side comparison for one fixed date.
- `"partner": "booking"` at the top level. `cmp` = short snake tag (e.g. `marina_hotels_dubai`): it becomes the Travelpayouts sub_id.
- `link` = the hotel's Booking URL from the harvest, e.g. `https://www.booking.com/hotel/ae/intercontinental-dubai-marina.en-gb.html` (the builder turns it into the Travelpayouts deep link). No query string.
- `rating10` = Booking score out of 10 (e.g. 9.1), `reviews` = Booking review count. Do NOT set `rating` (the builder derives the 5-point value).
- `price` = the card price (cheapest nightly rate for the date, EUR). `price_unit`: `"per night, 2 adults"`. Say in copy that taxes/fees come on top where the card text says so ("+ taxes and charges" / AED tourism fee from the rooms table).
- `operator` = brand or group as Booking shows it (e.g. "Marriott Bonvoy", "IHG", "Jumeirah", "independent"); `duration` = category like "5★ hotel", "4★ hotel apartments", "5★ beach resort"; `place` = the micro-location ("Marina promenade", "JBR Walk", "Palm Jumeirah trunk"); `map_q` = hotel name + "Dubai".
- `gallery` = 9-10 full photo URLs `https://cf.bstatic.com/xdata/images/hotel/max1024x768/<id>.jpg?k=<k>` from that hotel's own `photos[]`, in selling order: money shot first (pool/beach/view/exterior or the signature room), then room, bathroom/lobby, dining, spa. Use the `alt` captions to choose. No floor plans, no near-duplicates, no logos, no text boards.
- **Pills (6-8)**, order: 🕒 check-in/out (`"kind": "time"`, from `rules`), 🛏️ rooms (size/type of the cheapest room from `rooms`), 👨‍👩‍👧 kids & access (`"kind": "access"`: child policy, cots/extra beds, accessibility from `rules`/`highlights`), 2-4 pills on what you get (pool, beach, breakfast price or "included", spa, metro/walk distances from `desc`), then the vibe (`"kind": "vibe"`). Every body adds facts beyond its label.
- **facts** labels (the card's 5 traveller questions are built from these, keep the exact labels): `Check-in`, `Breakfast`, `Rooms`, `Pools` or `Pool`, `Beach`, `Getting there`, `Airport`, `Metro`, `Parking`, `Dining`, `Spa`, `Kids' club`, `Policies`, `Pets`. Give at least 5 that you can fill from the data.
- `trust`: only what the rooms table shows for some rate, e.g. "Free cancellation on rates that show it", "No prepayment on some rates", "Breakfast-included rates available". `cancel` (buy card perk) similar, never a promise for every rate.
- Spec top level also needs: `"filter_rows": [{"label": "Style", "cats": ["beach", "city"]}, {"label": "Who & budget", "cats": ["family", "couples", "budget"]}]` covering every filter cat exactly once; `"sticky_trust": "No booking fee"`; `"price_note": "Lowest nightly rate for 2 adults on 13–14 January 2027. Dates, room type and board change it; taxes and the Dubai tourism fee are added at booking."`
- `guide` (mandatory): (1) comparison table: hotel, stars, price/night, Booking score, location score (from `subscores`), beach/pool, breakfast (included or price), best for; (2) "Which one should you book?"; (3) practical: which part of the area to stay in, getting around (metro/tram/taxi distances from `desc`), what costs extra (tourism fee, breakfast, resort beach access), best months. Only facts in the data.
- Lead: two short paragraphs, kit style. 1) the buying answer: which hotel for whom, with concrete prices; 2) what all 10 were compared on (price for the same date, score, location, pool/beach, breakfast, room size) and the next step (filters / ranking). No dates in the lead, no review totals, no OTA names.
- Title like "10 Best Hotels in Dubai Marina (2026): Prices Compared" (≤ 60 chars). No "Booking.com" in title/meta/h1/lead.
- Do not narrate the platform ("Booking.com shows", "only 2 rooms left", "We have 5 left"). Card badges already name the site.

## Build and QC
```bash
python3 scripts/build_article.py --photos scripts/articles/<slug>.json
python3 ~/.claude/skills/qc-article/qc_article.py --site-dir . --page <slug>/index.html
```
Fix every FAIL except `[wiring]` (done later). Final message: slug, table (rank, hotel, price, score/reviews, photos), what you dropped and why, rules you could not meet.
