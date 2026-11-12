# Communication Style & Operational Directives

- **Tone & Demeanor**: Strictly objective, direct, and candid.
- **Zero Sycophancy (No Ass-Kissing)**: Never flatter, over-praise, or use hyped promotional language. Do not use artificial enthusiasm or cheerleading.
- **Truth Over Politeness**: If the user's premise, math, assumption, or marketing approach has flaws, call it out plainly and immediately. Never hesitate to contradict the user when data, economics, or facts dictate otherwise.
- **Concise & Analytical**: Deliver hard numbers, real unit economics, structural constraints, and concrete action steps without fluff.

# Language Scope (MANDATORY)

- **English only**: The site is English-only. All translated language editions were removed on purpose.
- **Do not recreate translations**: Never create, restore, or port pages into language subdirectories (`/de/`, `/fr/`, `/ru/`, `/hu/`, etc.), and never add `hreflang` alternate tags, unless the user explicitly asks for a new language edition.

# Sitemap & Technical SEO Directives

- **XML Sitemap Architecture**:
  - Sitemap path: `sitemap.xml` (referenced in `robots.txt` via `Sitemap: https://luxurytraveltester.com/sitemap.xml`).
  - Automated generator: `scripts/generate_sitemap.py` (builds entries from each page's `<link rel="canonical">`).
  - Canonical Scope: Only the English canonical URLs (currently **14**: home, 3 hub articles, their subpages, about, contact, privacy). Update this count when pages are added or removed.
  - No `xhtml:link` hreflang annotations; there are no alternate language versions.
  - Zero Non-Canonical Submissions: only declared canonical URLs belong in `sitemap.xml`.

# Comparison Deck & Layout Architecture Directives

- **Single Primary Comparison Engine**:
  - The top comparison section uses the visual card deck (`#ltt-cards-deck` inside `.ltt-deck-container` / `#dubai-safari-deck`) with filter tabs, multi-photo sliders, verified specifications, pricing, and affiliate booking CTAs.
  - Do NOT duplicate content with an executive summary rows table above the cards deck. Keep the cards deck as the sole top comparison engine.
- **Detailed Reviews (Semantic HTML5 `<details open>`)**:
  - All 10 detailed breakdowns are wrapped in semantic `<details open class="bpa-details-card">` elements, open by default on static load for 100% crawlability.
  - **Zero Nested Dropdowns / No Load-More Cutoffs**: NEVER allow secondary nested dropdowns, artificial height clamps (e.g. `.load-more-div { height: 750px }`), or redundant `LOAD MORE →` buttons inside the review cards. When a review is open, all text, photos, and breakdown sections must flow completely and continuously without requiring a second click.
- **Review Badge Formatting & Affiliate Links**:
  - Do NOT print company names in text (e.g. `(GetYourGuide)`, `(TripAdvisor)`, `(Viator)`). The official platform icon conveys the brand cleanly while saving crucial horizontal space.
  - Each review badge must be rendered as an individual, clickable `<a>` pill (`.bpa-rev-badge`) linked directly to the corresponding affiliate product URL (`target="_blank"`, `rel="noopener nofollow sponsored"`).
  - Inside `<summary>`, badges MUST include `onclick="event.stopPropagation()"` to ensure clicking the review pill opens the affiliate partner without unintentionally toggling or collapsing the review card.

# Media & Image Slider Fidelity Directives (MANDATORY)

- **Exact Image Preservation**:
  - NEVER arbitrarily cap, slice, or truncate photo sliders (e.g. capping at 6 photos).
  - NEVER inject synthetic, borrowed, or duplicate filler images into sliders.
  - ALWAYS preserve the exact photo count, exact URLs, and exact order from the original Webflow source or live site.
- **Slider UI Logic by Count**:
  - **Multi-Photo Items (>1 photo)**: Render smooth horizontal scroll container (`.bpa-slider`), previous/next navigation buttons (`.bpa-arrow`), and dynamic index indicator pill (`.bpa-pill` displaying `1 / N`).
  - **Single-Photo Items (==1 photo)**: Render the single verified hero photo directly. Omit navigation arrows and counter pills completely to preserve clean presentation.
