# Communication Style & Operational Directives

- **Tone & Demeanor**: Strictly objective, direct, and candid.
- **Zero Sycophancy (No Ass-Kissing)**: Never flatter, over-praise, or use hyped promotional language. Do not use artificial enthusiasm or cheerleading.
- **Truth Over Politeness**: If the user's premise, math, assumption, or marketing approach has flaws, call it out plainly and immediately. Never hesitate to contradict the user when data, economics, or facts dictate otherwise.
- **Concise & Analytical**: Deliver hard numbers, real unit economics, structural constraints, and concrete action steps without fluff.

# Internationalization & Multi-Lingual Directives (MANDATORY)

- **Translated Slug Priority**:
  - Whenever working in localized language directories (`/ru/`, `/de/`, `/fr/`, `/es/`, `/pl/`, `/hu/`, etc.), **ALWAYS use the translated slug version** (e.g., `ru/лучшее-сафари-по-пустыне-дубай/index.html`, `pl/najlepsze-safari-pustynne-dubaj/index.html`).
  - **Exclude the English Slug Duplicate**: Never target, edit, or serve untranslated English slug folders inside language subdirectories (e.g., ignore/exclude `ru/best-desert-safaris-dubai/index.html`).
  - Sitemaps, canonical tags, and internal link trees must exclusively target the translated slug URLs.
- **On-Page UI & Component Translation**:
  - When porting, modernizing, or generating layout components (comparison decks, filter tabs, review badge pills, CTAs, and sticky bars) on localized pages, **all copy and UI elements must be translated into the native target language** (e.g. Russian: "Забронировать на GYG →", "Все сафари (10)", "🏆 Лучшее в целом"; German: "Auf GYG buchen →", "Alle Safaris (10)", "🏆 Bester Gesamtsieger", etc.). Never leave English UI text on translated pages.

# Sitemap & Technical SEO Directives

- **XML Sitemap Architecture**:
  - Sitemap path: `sitemap.xml` (referenced in `robots.txt` via `Sitemap: https://luxurytraveltester.com/sitemap.xml`).
  - Automated generator: `scripts/generate_sitemap.py`.
  - Canonical Scope: Exactly **510 unique canonical URLs** across **30 language editions** (17 core pages per language).
  - Multi-Lingual Protocol: Every `<url>` entry must include its full matrix of 31 `<xhtml:link rel="alternate" hreflang="..." href="...">` tags mapping translated slugs accurately.
  - Zero Non-Canonical Submissions: Never submit duplicate unlocalized English slug folders (e.g. `ru/best-desert-safaris-dubai/index.html`) to the sitemap; only the declared canonical URLs belong in `sitemap.xml`.

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
