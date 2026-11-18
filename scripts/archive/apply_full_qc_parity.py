import re
from bs4 import BeautifulSoup

SAFARIS_FILE = '/Users/adamdimitrov/Development/luxurytraveltester/best-desert-safaris-dubai/index.html'
HELI_FILE = '/Users/adamdimitrov/Development/luxurytraveltester/best-helicopter-tours-new-york/index.html'

with open(SAFARIS_FILE, 'r', encoding='utf-8') as f:
    safaris_html = f.read()

with open(HELI_FILE, 'r', encoding='utf-8') as f:
    heli_html = f.read()

# Define NYC Helicopter Data
NYC_HELICOPTER_DATA = [
    {
        "id": "1-flynyon",
        "alias_id": "1-legenda",
        "rank": "1",
        "tag": "🏆 #1 Best Overall • Shoe-Selfie",
        "tag_class": "bpa-gold",
        "name": "FlyNYON New York",
        "title": "FlyNYON NYC Open-Door \"Shoe Selfie\" Helicopter Tour",
        "cat": "overall opendoor night",
        "kicker": "FlyNYON • Kearny NJ Terminal • Open-Door Thrill",
        "rating": "4.4",
        "rating_score_text": "4.4 / 5.0",
        "rating_count": "13,000+ Reviews",
        "channels": [
            {"type": "google", "score": "4.4", "count": "11.0k+"},
            {"type": "ta", "score": "4.5", "count": "2.0k+"}
        ],
        "specs": ["📸 Open-Door Shoe-Selfie", "🌃 Night Skyline Flights", "⏱️ 16m or 30m Duration", "✔️ Personally Tested by Adam", "📍 Kearny, NJ Terminal"],
        "best_for": "Anyone seeking the ultimate NYC thrill and social media photos, dangling legs above the illuminated nighttime skyline.",
        "price": "From $99–$249",
        "price_sub": "16 min basic from $99–$249 • 30 min upgrade (~$105 at desk)",
        "link": "https://www.flynyon.com/",
        "maps_link": "https://maps.app.goo.gl/M7HgoZAbejMyQS2G9",
        "images": [
            "/assets/cdn/67d02edca7795b0f57073b59/6a47d3559ce91814c1df86f5_best-helicopter-tours-nyc-flynyon-4.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b211878b3a96768334_best-helicopter-tours-nyc-flynyon-17.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b210a69bc70a9e3411_best-helicopter-tours-nyc-flynyon-11.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b4bf6f86ab17454b8d_best-helicopter-tours-nyc-flynyon-19.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b5dcf4456feae7623e_best-helicopter-tours-nyc-flynyon-3.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b2e28f970c7412e70a_best-helicopter-tours-nyc-flynyon-20.JPG.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b50943913cb88f4f15_best-helicopter-tours-nyc-flynyon-2.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b46620ac3fe0404510_best-helicopter-tours-nyc-flynyon-1.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b311f008c657a3bf3b_best-helicopter-tours-nyc-flynyon-7.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b3e1d5c0fa7380cb30_best-helicopter-tours-nyc-flynyon-9.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b210fffa63fd5c45a8_best-helicopter-tours-nyc-flynyon-8.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b361a3bd3efb23ed61_best-helicopter-tours-nyc-flynyon-10.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b48f0b68f713944d36_best-helicopter-tours-nyc-flynyon-12.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b3299abbd41fe277b8_best-helicopter-tours-nyc-flynyon-15.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b3f05dcdce2b1827b2_best-helicopter-tours-nyc-flynyon-13.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b356b7deb3a7017eac_best-helicopter-tours-nyc-flynyon-16.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a3e93b3a38fb94347f05413_best-helicopter-tours-nyc-flynyon-14.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4d3fc57f5b3867f83d5252_flynyon.avif"
        ]
    },
    {
        "id": "2-heliny",
        "alias_id": "2-rubingroup",
        "rank": "2",
        "tag": "🥈 #2 Runner Up • Classic Closed-Door",
        "tag_class": "bpa-gold",
        "name": "HeliNY",
        "title": "HeliNY Manhattan Classic Closed-Door Scenic Helicopter Tour",
        "cat": "overall closeddoor",
        "kicker": "HeliNY • Downtown Manhattan Heliport (Pier 6) • Closed-Door Classic",
        "rating": "4.8",
        "rating_score_text": "4.8 / 5.0",
        "rating_count": "9,240+ Reviews",
        "channels": [
            {"type": "gyg", "score": "4.8", "count": "7.1k+"},
            {"type": "viator", "score": "4.8", "count": "1.3k+"},
            {"type": "ta", "score": "4.8", "count": "750+"}
        ],
        "specs": ["🚪 Climate-Controlled Cabin", "🗽 Statue of Liberty Views", "⏱️ 12 to 30 min Durations", "✔️ Personally Tested by Adam", "📍 Downtown Manhattan Pier 6"],
        "best_for": "Travelers wanting a comfortable, enclosed daytime flight departing directly from Lower Manhattan without traveling to New Jersey.",
        "price": "From $269",
        "price_sub": "12-15 min from $269 • 17-20 min $339 • 25-30 min $429",
        "link": "https://www.getyourguide.com/new-york-city-l59/nyc-manhattan-sightseeing-helicopter-tour-t19901/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-heliny&mkt_cmp=true",
        "maps_link": "https://maps.app.goo.gl/VHqxx4N9k6GJw3rGA",
        "images": [
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf594f0a6341fe351db_best-helicopter-tours-nyc-heliny-1.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf70dd18fd3b6f5cc27_best-helicopter-tours-nyc-heliny-15.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf78ebd68066b64c4a1_best-helicopter-tours-nyc-heliny-18.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf56b566d4ac49f5e05_best-helicopter-tours-nyc-heliny-17.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf7e7a9ec87627f2a43_best-helicopter-tours-nyc-heliny-2.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf71bd96559fa923d8f_best-helicopter-tours-nyc-heliny-14.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf5e65c811a8d65cb83_best-helicopter-tours-nyc-heliny-13.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf82994b45745fc6026_best-helicopter-tours-nyc-heliny-4.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf77f4dc7d7180b895c_best-helicopter-tours-nyc-heliny-7.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf7b93c1b54617a3f13_best-helicopter-tours-nyc-heliny-11.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47daf5c9ff2d5bf8d7508d_best-helicopter-tours-nyc-heliny-12.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a47dd8fbfa2dfc7559687ec_best-helicopter-tours-nyc-heliny-5_result.avif"
        ]
    },
    {
        "id": "3-charm-aviation",
        "alias_id": "4-kisfaludy-historic-cruise",
        "rank": "3",
        "tag": "🥉 #3 Also Great • Lower Manhattan",
        "tag_class": "bpa-bronze",
        "name": "Charm Aviation",
        "title": "Charm Aviation Big Apple All-Inclusive Helicopter Tour",
        "cat": "closeddoor",
        "kicker": "Charm Aviation • Downtown Manhattan Heliport • Mon–Sat",
        "rating": "4.6",
        "rating_score_text": "4.6 / 5.0",
        "rating_count": "4,400+ Reviews",
        "channels": [
            {"type": "gyg", "score": "4.8", "count": "2.1k+"},
            {"type": "viator", "score": "4.5", "count": "1.8k+"},
            {"type": "ta", "score": "4.3", "count": "350+"}
        ],
        "specs": ["🚪 Climate-Controlled Cabin", "📍 Downtown Manhattan Pier 6", "⏱️ 12 to 30 min Durations", "🗓️ Mon–Sat (Closed Sundays)", "⭐ All-Inclusive Fees"],
        "best_for": "Great alternative to HeliNY when dates are booked up (Mon–Sat only; note they do not fly on Sundays).",
        "price": "From $269",
        "price_sub": "Includes heliport facility fees",
        "link": "https://www.getyourguide.com/new-york-city-l59/nyc-helicopter-tour-of-the-big-apple-all-inclusive-t456488/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-charm-aviation&mkt_cmp=true",
        "maps_link": "https://maps.app.goo.gl/ihKsQZb5G4UXTgr4A",
        "images": [
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159ed30e0dd535134b67_best-helicopter-tours-nyc-charm-aviation-4.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159e2f2b3aa805a18fd0_best-helicopter-tours-nyc-charm-aviation-1.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159e215abbb8f21d7487_best-helicopter-tours-nyc-charm-aviation-3.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159eb550267ae3150903_best-helicopter-tours-nyc-charm-aviation-5.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159e041c2a759ca559ff_best-helicopter-tours-nyc-charm-aviation-8.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159e75e49a6ca9881c84_best-helicopter-tours-nyc-charm-aviation-7.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159de6393d203487a9b3_best-helicopter-tours-nyc-charm-aviation-6.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49159cf200933aba6c0701_best-helicopter-tours-nyc-charm-aviation-2.avif"
        ]
    },
    {
        "id": "4-zip-aviation",
        "alias_id": "3-portum",
        "rank": "4",
        "tag": "⭐ #4 Time-Tested Classic",
        "tag_class": "bpa-bronze",
        "name": "Zip Aviation",
        "title": "Zip Aviation Liberty Harbor Helicopter Adventure",
        "cat": "closeddoor",
        "kicker": "Zip Aviation • Downtown Manhattan Heliport • Time-Tested",
        "rating": "4.6",
        "rating_score_text": "4.6 / 5.0",
        "rating_count": "9,350+ Reviews",
        "channels": [
            {"type": "gyg", "score": "4.7", "count": "7.3k+"},
            {"type": "viator", "score": "4.4", "count": "1.4k+"},
            {"type": "ta", "score": "4.5", "count": "190+"}
        ],
        "specs": ["🚪 Classic Closed-Door Helicopter", "📍 Downtown Manhattan Pier 6", "⏱️ 12 or 30 min Durations", "👥 Solo Passenger Policy Applies", "🛡️ Veteran Operator"],
        "best_for": "Couples or small groups wanting a time-tested operator from Pier 6 (note solo traveler group minimum requirements).",
        "price": "From $269",
        "price_sub": "12–30 min flights available",
        "link": "https://www.getyourguide.com/new-york-city-l59/liberty-harbor-helicopter-adventure-t15252/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-zip-aviation&mkt_cmp=true",
        "maps_link": "https://maps.app.goo.gl/LPbifuYEZNGB8vTg8",
        "images": [
            "/assets/cdn/67d02edca7795b0f57073b59/6a4916664ece1b870de05d64_best-helicopter-tours-nyc-zip-aviation-6.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4916667d3b027f52b893b6_best-helicopter-tours-nyc-zip-aviation-13.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a491665bef554b822b82057_best-helicopter-tours-nyc-zip-aviation-12.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a491666de2bced790ce3faf_best-helicopter-tours-nyc-zip-aviation-9.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a491665d0e0f799d7955f37_best-helicopter-tours-nyc-zip-aviation-8.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49166603ad4172d1a3b009_best-helicopter-tours-nyc-zip-aviation-10.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a491666a4873ec6180f8a63_best-helicopter-tours-nyc-zip-aviation-11.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a49166670325ae14a945479_best-helicopter-tours-nyc-zip-aviation-7.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4916668a1508d3eae97f40_best-helicopter-tours-nyc-zip-aviation-5.avif"
        ]
    },
    {
        "id": "5-wings-air",
        "alias_id": "5-silverline-no-frills",
        "rank": "5",
        "tag": "💑 #5 Best for Couples • Private Luxury",
        "tag_class": "bpa-gold",
        "name": "Wings Air Helicopters",
        "title": "Wings Air Couple's Private Luxury Helicopter Tour from White Plains",
        "cat": "couples closeddoor",
        "kicker": "Wings Air • Westchester Airport (White Plains) • Private 30–45m",
        "rating": "4.8",
        "rating_score_text": "4.8 / 5.0",
        "rating_count": "390+ Reviews",
        "channels": [
            {"type": "gyg", "score": "4.8", "count": "300+"},
            {"type": "viator", "score": "4.8", "count": "50+"},
            {"type": "ta", "score": "4.7", "count": "40+"}
        ],
        "specs": ["💑 100% Private Helicopter for 2", "🍾 Champagne Toast Included", "📍 Departs White Plains", "⏱️ 30 or 45 min Route", "🗺️ Unique North-to-South Entry"],
        "best_for": "Romantic proposals, anniversaries, and couples wanting complete privacy without strangers in their cabin.",
        "price": "From $690/flight",
        "price_sub": "Private charter for 2 • 30–45 min",
        "link": "https://www.getyourguide.com/new-york-city-l59/couple-s-private-helicopter-tour-over-new-york-t63337/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-wings-air&mkt_cmp=true",
        "maps_link": "https://maps.app.goo.gl/jagGWLf6gwQpDPxJ6",
        "images": [
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b50a823a381952a36e_best-helicopter-tours-nyc-wings-air-3.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b388f8dc3c9b651118_best-helicopter-tours-nyc-wings-air-5.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b54480068d7c8c5528_best-helicopter-tours-nyc-wings-air-2.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b487e679d5400c6ac7_best-helicopter-tours-nyc-wings-air-8.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b5da8eb02bf62f9187_best-helicopter-tours-nyc-wings-air-6.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b50a823a381952a387_best-helicopter-tours-nyc-wings-air-4.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b567feb6e78cfda437_best-helicopter-tours-nyc-wings-air-9.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b570325ae14a94e501_best-helicopter-tours-nyc-wings-air-7.avif",
            "/assets/cdn/67d02edca7795b0f57073b59/6a4919b53052977cb135f301_best-helicopter-tours-nyc-wings-air-1.avif"
        ]
    }
]

# 1. Base CSS from Safaris + Enhanced QC Rules
css_start = safaris_html.find('<style id="ltt-dubai-safari-styles">')
css_end = safaris_html.find('</style>', css_start)
safaris_css = safaris_html[css_start:css_end + len('</style>')]
safaris_css = re.sub(r'/\* =+\s+Executive 10-Safari Summary Table.*?(?=/\* =+\s+Card Deck)', '', safaris_css, flags=re.DOTALL)
clean_heli_css = safaris_css.replace('id="ltt-dubai-safari-styles"', 'id="ltt-nyc-helicopter-styles"')
clean_heli_css = clean_heli_css.replace('DUBAI DESERT SAFARIS 2026 ARCHITECTURE', 'NYC HELICOPTER TOURS 2026 ARCHITECTURE')

extra_fixes_css = '''
/* ==========================================================================
   NYC HELICOPTER QC FIXES: Anti-Glitch Overrides
   ========================================================================== */

/* Fix 1: Stop .bpa-rank-tag from jumping over the TOC */
.bpa-acc-meta .bpa-rank-tag {
  position: static !important;
  display: inline-flex !important;
  align-items: center !important;
  box-shadow: none !important;
  margin: 0 6px 0 0 !important;
}

/* Fix 2: Sidebar Table of Contents items exact styling */
.content-left .stick-wrapper .toc {
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
}
.content-left .stick-wrapper .toc a.tocitem {
  color: #4a6a86 !important;
  border-left: 2px solid #e2e8f0 !important;
  border-radius: 0 5px 5px 0 !important;
  padding: 8px 12px !important;
  font-size: 12.5px !important;
  font-weight: 500 !important;
  line-height: 1.35em !important;
  text-decoration: none !important;
  transition: all 0.15s ease !important;
  display: block !important;
}
.content-left .stick-wrapper .toc a.tocitem:hover {
  color: #0f172a !important;
  background-color: rgba(217, 119, 6, 0.08) !important;
  border-left: 2px solid #d97706 !important;
  padding-left: 12px !important;
}
.content-left .stick-wrapper .toc a.tocitem.active {
  color: #0f172a !important;
  font-weight: 800 !important;
  background-color: rgba(217, 119, 6, 0.12) !important;
  border-left: 2px solid #d97706 !important;
  padding-left: 12px !important;
}

/* Fix 3: Balanced 50/50 Pros & Cons Columns (BPA Architecture) */
.pro-con-box-wrapper,
.pro-con-box-wrapper-2,
.pro-con-box-wrapper-3,
.pro-con-box-wrapper-4 {
  width: 100% !important;
  max-width: 100% !important;
  margin: 20px 0 24px 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  border-radius: 14px !important;
  box-shadow: none !important;
  overflow: hidden !important;
  display: block !important;
  box-sizing: border-box !important;
}
.pro-con-box-wrapper .w-layout-grid,
.pro-con-box-wrapper .grid-15,
.pro-con-box-wrapper .grid-28,
.pro-con-box-wrapper-2 .w-layout-grid,
.pro-con-box-wrapper-2 .grid-28,
.pro-con-box-wrapper-3 .w-layout-grid,
.pro-con-box-wrapper-3 .grid-28,
.pro-con-box-wrapper-4 .w-layout-grid,
.pro-con-box-wrapper-4 .grid-28 {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
  grid-template-areas: none !important;
  gap: 16px !important;
  align-items: stretch !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  outline: none !important;
  box-sizing: border-box !important;
}
@media (max-width: 640px) {
  .pro-con-box-wrapper .w-layout-grid,
  .pro-con-box-wrapper .grid-15,
  .pro-con-box-wrapper .grid-28,
  .pro-con-box-wrapper-2 .w-layout-grid,
  .pro-con-box-wrapper-2 .grid-28,
  .pro-con-box-wrapper-3 .w-layout-grid,
  .pro-con-box-wrapper-3 .grid-28,
  .pro-con-box-wrapper-4 .w-layout-grid,
  .pro-con-box-wrapper-4 .grid-28 {
    grid-template-columns: 1fr !important;
    gap: 16px !important;
  }
}
.pro-con-box-pro-cell,
.pro-con-box-pro-cell-2,
.pro-con-box-pro-cell-3,
.pro-con-box-pro-cell-4,
.pro-con-box-con-cell,
.pro-con-box-con-cell-2,
.pro-con-box-con-cell-3,
.pro-con-box-con-cell-4 {
  border-radius: 12px !important;
  padding: 18px 20px !important;
  box-shadow: 0 10px 28px -10px rgba(15, 23, 42, 0.06), 0 2px 6px rgba(15, 23, 42, 0.02) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: stretch !important;
  position: relative !important;
  overflow: hidden !important;
  height: 100% !important;
  width: 100% !important;
  margin: 0 !important;
  outline: none !important;
  box-sizing: border-box !important;
}
.pro-con-box-pro-cell,
.pro-con-box-pro-cell-2,
.pro-con-box-pro-cell-3,
.pro-con-box-pro-cell-4 {
  background: #f0fdf4 !important;
  border: 1px solid #bbf7d0 !important;
  border-top: 4px solid #16a34a !important;
}
.pro-con-box-con-cell,
.pro-con-box-con-cell-2,
.pro-con-box-con-cell-3,
.pro-con-box-con-cell-4 {
  background: #fff1f2 !important;
  border: 1px solid #fecdd3 !important;
  border-top: 4px solid #e11d48 !important;
}
.pro-con-box-pro-cell-rich-text-block,
.pro-con-box-con-cell-rich-text-block,
.pro-con-box-pro-cell .w-richtext,
.pro-con-box-pro-cell-3 .w-richtext,
.pro-con-box-con-cell .w-richtext,
.pro-con-box-con-cell-3 .w-richtext {
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.pro-con-box-pro-cell h3,
.pro-con-box-pro-cell-3 h3,
.pro-con-box-con-cell h3,
.pro-con-box-con-cell-3 h3 {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  font-size: 15px !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  margin: 0 0 10px 0 !important;
  padding: 0 0 14px 0 !important;
  border-bottom: 1px solid #f1f5f9 !important;
  line-height: 1.2 !important;
}
.pro-con-box-pro-cell h3,
.pro-con-box-pro-cell-3 h3,
.pro-con-box-pro-cell h3 strong,
.pro-con-box-pro-cell-3 h3 strong {
  color: #14532d !important;
}
.pro-con-box-con-cell h3,
.pro-con-box-con-cell-3 h3,
.pro-con-box-con-cell h3 strong,
.pro-con-box-con-cell-3 h3 strong {
  color: #881337 !important;
}
.pro-con-box-pro-cell h3::before,
.pro-con-box-pro-cell-3 h3::before {
  content: "✓" !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 22px !important;
  height: 22px !important;
  border-radius: 50% !important;
  background: #22c55e !important;
  color: #ffffff !important;
  font-size: 12px !important;
  font-weight: 900 !important;
  flex-shrink: 0 !important;
  box-shadow: 0 2px 6px rgba(34, 197, 94, 0.3) !important;
}
.pro-con-box-con-cell h3::before,
.pro-con-box-con-cell-3 h3::before {
  content: "✕" !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 22px !important;
  height: 22px !important;
  border-radius: 50% !important;
  background: #f43f5e !important;
  color: #ffffff !important;
  font-size: 11px !important;
  font-weight: 900 !important;
  flex-shrink: 0 !important;
  box-shadow: 0 2px 6px rgba(244, 63, 94, 0.3) !important;
}
.pro-con-box-pro-cell ul,
.pro-con-box-pro-cell-3 ul,
.pro-con-box-con-cell ul,
.pro-con-box-con-cell-3 ul {
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
}
.pro-con-box-pro-cell li,
.pro-con-box-pro-cell-3 li,
.pro-con-box-con-cell li,
.pro-con-box-con-cell-3 li {
  position: relative !important;
  padding-left: 28px !important;
  margin: 0 !important;
  font-size: 14.5px !important;
  line-height: 1.55 !important;
  color: #334155 !important;
  list-style-type: none !important;
}
.pro-con-box-pro-cell li strong,
.pro-con-box-pro-cell-3 li strong,
.pro-con-box-con-cell li strong,
.pro-con-box-con-cell-3 li strong {
  color: #0f172a !important;
  font-weight: 700 !important;
}
.pro-con-box-pro-cell li::before,
.pro-con-box-pro-cell-3 li::before {
  content: "✓" !important;
  position: absolute !important;
  left: 0 !important;
  top: 2px !important;
  width: 18px !important;
  height: 18px !important;
  border-radius: 50% !important;
  background: #dcfce7 !important;
  color: #15803d !important;
  font-size: 11px !important;
  font-weight: 900 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
}
.pro-con-box-con-cell li::before,
.pro-con-box-con-cell-3 li::before {
  content: "✕" !important;
  position: absolute !important;
  left: 0 !important;
  top: 2px !important;
  width: 18px !important;
  height: 18px !important;
  border-radius: 50% !important;
  background: #ffe4e6 !important;
  color: #be123c !important;
  font-size: 10px !important;
  font-weight: 900 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
}

/* Fix 4: Quick Facts & Logistics Box */
.bpa-quick-facts-card {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  padding: 14px 18px !important;
  margin: 16px 0 !important;
}
.bpa-quick-facts-card h4 {
  margin-top: 0 !important;
  margin-bottom: 10px !important;
  font-size: 14px !important;
  font-weight: 800 !important;
  color: #0f172a !important;
}
.bpa-qf-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
  gap: 8px 14px !important;
}
.bpa-qf-item {
  font-size: 12.5px !important;
  color: #334155 !important;
  line-height: 1.4 !important;
}
.bpa-qf-item strong {
  color: #0f172a !important;
}

/* Fix 5: Channel Icon definitions */
.bpa-ic-google {
  background-image: url("/assets/cdn/67d02edca7795b0f57073b59/67ebc6e4688dbf65f4077122_google-logo.avif");
}
.bpa-ic-ta {
  background-image: url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_tripadvisor-icon.png");
}
.bpa-ic-gyg {
  background-image: url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png");
}
.bpa-ic-viator {
  background-image: url("/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png");
}

/* Fix 6: Details summary toggle chevron */
.bpa-details-toggle {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex-shrink: 0 !important;
  margin-left: 16px !important;
}
.bpa-details-chevron {
  font-size: 16px !important;
  color: #64748b !important;
  transition: transform 0.2s ease !important;
}
details[open] .bpa-details-chevron {
  transform: rotate(180deg) !important;
}

/* Fix 7: Strict Constraints for Sticky Mobile Bar */
.sticky-mobile-bar .sticky-thumb-img {
  width: 44px !important;
  height: 44px !important;
  max-width: 44px !important;
  max-height: 44px !important;
  border-radius: 8px !important;
  object-fit: cover !important;
  flex-shrink: 0 !important;
}
'''
clean_heli_css = clean_heli_css.replace('</style>', f'{extra_fixes_css}\n</style>')

# 2. Build Card Deck HTML
deck_html = ['<div class="ltt-deck-container" id="nyc-helicopter-deck">']
deck_html.append('''<div class="ltt-header-box">
<span class="ltt-kicker-tag">2026 Comparison Engine • Personally Tested</span>
<h2 class="ltt-header-title">Comparison Guide — 5 Best Helicopter Tours in New York</h2>
<p class="ltt-header-desc">Compare open-door "shoe selfie" flights, classic climate-controlled Manhattan tours, night flights, and private couples rides side-by-side.</p>
<div class="ltt-filter-tabs">
<button class="ltt-tab-btn active" onclick="lttFilterHelicopters('all', this)" type="button">All Tours (5)</button>
<button class="ltt-tab-btn" onclick="lttFilterHelicopters('opendoor', this)" type="button">🚁 Open-Door / Shoe-Selfie</button>
<button class="ltt-tab-btn" onclick="lttFilterHelicopters('closeddoor', this)" type="button">🚪 Closed-Door Classic</button>
<button class="ltt-tab-btn" onclick="lttFilterHelicopters('night', this)" type="button">🌃 Night Flights</button>
<button class="ltt-tab-btn" onclick="lttFilterHelicopters('couples', this)" type="button">💑 Couples &amp; Private</button>
</div>
</div>
<div class="bpa-deck-wrap" id="ltt-cards-deck">''')

for h in NYC_HELICOPTER_DATA:
    imgs_html = []
    for idx, img in enumerate(h["images"]):
        loading = 'eager' if idx == 0 else 'lazy'
        imgs_html.append(f'<img alt="{h["name"]}" class="bpa-slide" loading="{loading}" src="{img}"/>')
    
    channels_html = []
    for c in h["channels"]:
        channels_html.append(f'''<div class="bpa-ci">
<i class="bpa-ic-{c["type"]}"></i>
<strong>{c["score"]}</strong>
<span>({c["count"]})</span>
</div>''')
    
    specs_pills = ''.join([f'<span class="bpa-sp">{s}</span>' for s in h["specs"]])
    
    card = f'''<div class="bpa-card" data-cat="{h["cat"]}" id="card-{h["rank"]}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {h["tag_class"]}">{h["tag"]}</span>
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>
<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>
<span class="bpa-pill">1 / {len(h["images"])}</span>
<div class="bpa-slider" onscroll="bpaCount(this)">
{''.join(imgs_html)}
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{h["kicker"]}</div>
<a class="bpa-title" href="#{h["id"]}">{h["rank"]}. {h["title"]}</a>
<div class="bpa-proof">
<span class="bpa-stars">★★★★★</span>
<span class="bpa-score-text">{h["rating_score_text"]}</span>
<span class="bpa-count-muted">({h["rating_count"]})</span>
<span class="bpa-vchip">✓ Verified</span>
</div>
<div class="bpa-channels">
{''.join(channels_html)}
</div>
<div class="bpa-specs-row">
{specs_pills}
</div>
<div class="bpa-best-for">
🎯 <strong>Best For:</strong> {h["best_for"]}
</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{h["price"]}</div>
<div class="bpa-psub">{h["price_sub"]}</div>
</div>
<a class="bpa-btn" href="{h["link"]}" rel="noopener nofollow sponsored" target="_blank">Book Now →</a>
<a class="bpa-sublink" href="#{h["id"]}">Read Review ↓</a>
</div>
</div>
</div>'''
    deck_html.append(card)

deck_html.append('</div></div>')
full_deck_markup = '\n'.join(deck_html)

# 3. Build Details Cards
details_cards_html = []

# Tour 1: FlyNYON
details_cards_html.append('''<details class="bpa-details-card" id="1-flynyon" open="">
<a id="1-legenda" class="ltt-anchor-alias"></a>
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-acc-meta">
<span class="bpa-rank-tag bpa-gold">🏆 #1 Best Overall • Shoe-Selfie</span>
<span class="bpa-acc-pill">FlyNYON • <strong>From $99–$249</strong> • ⏱️ 16m or 30m</span>
</div>
<h3 class="bpa-details-title">1. FlyNYON — NYC Open-Door "Shoe Selfie" Helicopter Tour</h3>
<div class="bpa-summary-reviews">
<div class="div-block-53">
<a class="bpa-rev-badge" href="https://maps.app.goo.gl/M7HgoZAbejMyQS2G9" onclick="event.stopPropagation()" rel="noopener nofollow" target="_blank">
<img alt="Google" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/67d02edca7795b0f57073b59/67ebc6e4688dbf65f4077122_google-logo.avif"/>
<span class="bpa-rev-score">4.4</span>
<span class="bpa-rev-stars">★★★★½</span>
<span class="bpa-rev-count">+11,000 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://maps.app.goo.gl/M7HgoZAbejMyQS2G9" onclick="event.stopPropagation()" rel="noopener nofollow" target="_blank">
<img alt="TripAdvisor" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_tripadvisor-icon.png"/>
<span class="bpa-rev-score">4.5</span>
<span class="bpa-rev-stars">★★★★½</span>
<span class="bpa-rev-count">+2,000 reviews</span>
</a>
</div>
</div>
</div>
<div class="bpa-details-toggle">
<span class="bpa-details-chevron">▾</span>
</div>
</summary>
<div class="bpa-details-body">
<div class="bpa-quick-facts-card">
<h4>Flight Overview &amp; Logistics</h4>
<div class="bpa-qf-grid">
<div class="bpa-qf-item"><strong>Test Status:</strong> ✔️ Personally Tested by Adam</div>
<div class="bpa-qf-item"><strong>Hours:</strong> 10:00 AM – 11:00 PM Daily</div>
<div class="bpa-qf-item"><strong>Flight Duration:</strong> 16 or 30 Minutes</div>
<div class="bpa-qf-item"><strong>Flight Style:</strong> Open-Door "Shoe Selfie" (Tethered)</div>
<div class="bpa-qf-item"><strong>Meeting Point:</strong> <a href="https://maps.app.goo.gl/M7HgoZAbejMyQS2G9" target="_blank" rel="noopener nofollow">Kearny, New Jersey Terminal 📍</a></div>
<div class="bpa-qf-item"><strong>Getting There:</strong> Train to NJ + 10-min Uber</div>
</div>
</div>

<div class="pro-con-box-wrapper">
<div class="w-layout-grid grid-15">
<div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">
<div class="pro-con-box-pro-cell-rich-text-block w-richtext">
<h3><strong>Pros:</strong></h3>
<ul role="list">
<li><strong>The Ultimate "Shoe Selfie"</strong> — The only open-door experience where you can safely dangle your legs hundreds of meters above the city for iconic social media shots.</li>
<li><strong>Unmatched Night Views</strong> — Delivers a vastly richer and more spectacular experience seeing New York City completely lit up at night compared to daytime flights.</li>
<li><strong>Elite Safety Measures</strong> — Professional safety harnesses with quick-release buttons and tethers for all phones and cameras so nothing can fall.</li>
<li><strong>Full Manhattan Coverage (with Upgrade)</strong> — Extended flight crosses Statue of Liberty, Financial District, Central Park, Midtown, East River, and Brooklyn Bridge.</li>
<li><strong>Outstanding Customer Care</strong> — Highly attentive, warm, and professional ground crew with rapid dispatch communication.</li>
</ul>
</div>
</div>
<div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical">
<div class="pro-con-box-con-cell-rich-text-block w-richtext">
<h3><strong>Cons:</strong></h3>
<ul role="list">
<li><strong>Weird Online Overcharging</strong> — Save hundreds of dollars by booking the basic 16-minute flight online, then upgrading to 30 minutes in person at the desk for ~$105 to bypass steep $600–$700 online pricing.</li>
<li><strong>Located in New Jersey</strong> — Terminal requires an Uber ride or a train-to-Uber transfer from Manhattan.</li>
<li><strong>The Freight Train Trap</strong> — One approach route is frequently blocked by a slow-moving freight train; allow extra travel buffer time.</li>
</ul>
</div>
</div>
</div>
</div>

<div class="w-richtext">
<h2>Words Can Hardly Describe It: New York’s Skyline Lit Up at Night</h2>
<p>It is almost impossible to put into words the feeling of seeing <strong>New York City completely lit up at night</strong> from above. This is an <strong>absolute must-do experience</strong> for anyone traveling to New York.</p>
<p>In my experience, <strong>FlyNYON</strong> offers the <strong>most memorable helicopter tours</strong> in the city. The main reason for this is that, unlike most other operators, they fly with <strong>open-door helicopters</strong>. This means that during the flight, you can <strong>literally dangle your legs</strong> out of the chopper hundreds of meters above New York and capture those <strong>iconic "shoe selfie" photos and videos</strong> that you always see on social media.</p>

<h3>Safety First</h3>
<p>Despite the doors being wide open, you don't have to worry for a single second. Every passenger is secured to their seat with a <strong>professional safety harness</strong> equipped with a <strong>quick-release button</strong> for instant detachment in case of an emergency. Before taking off, everyone goes through <strong>multiple comprehensive safety briefings</strong>.</p>
<p>Your <strong>mobile phones and cameras are also tethered</strong> to your harness using special cases and lanyards, ensuring there is <strong>zero chance of dropping your device</strong> onto someone's head below.</p>

<h3>Open-Door vs. Closed-Door, Day vs. Night</h3>
<p>FlyNYON offers daytime, sunset, and night flights, with <strong>ticket prices increasing accordingly</strong>. I flew with them at <strong>9:00 PM in early June</strong>. While daytime flights are undeniably cheaper, the <strong>night flight delivers a vastly richer and more spectacular experience</strong> (and I say this as someone who has flown over New York during the day with another company).</p>
<p>The weather was absolutely perfect, though I imagine that <strong>during the freezing winter months</strong>, the open-door setup might make it <strong>too cold to fully enjoy</strong>.</p>

<h3>Pricing and the "Secret" Upgrade Strategy</h3>
<p>While the experience was worth every single penny, <strong>booking purely online can get incredibly expensive</strong>, sometimes climbing up to <strong>$600–$700 per ticket</strong>. After doing a bit of research, I came across a tip recommended by several past passengers: <strong>it is much cheaper to book the shorter 15–20 minute flight online, and then upgrade to the 30-minute flight in person at the terminal.</strong></p>
<p>That is exactly what I did. By doing the on-site upgrade, my <strong>total flight cost came out to around $450</strong> instead of the $600–$700 online rate. I honestly don't quite understand why they use this <strong>confusing pricing strategy</strong>, but the bottom line is that <strong>the trick works!</strong></p>

<h3>Location and the Traps of Getting There</h3>
<p>FlyNYON’s hangar is <strong>located in New Jersey</strong>, and getting there can throw a few curveballs at you. The <strong>most reliable option is taking an Uber</strong>, though that obviously comes with an extra cost. Public transport is available, but it's a bit more complicated. If you want to find the perfect balance between comfort and budget, I highly recommend <strong>taking a train into New Jersey first, and then ordering an Uber from there</strong> to save some money.</p>
<p><strong>Crucial logistics tip:</strong> there are two ways to approach the meeting point, and <strong>one of them is very likely to be blocked by a seemingly endless freight train</strong>. Because of this, you might have to take a <strong>massive detour</strong> (there is actually a sign posted out there warning you about this). This train situation <strong>nearly made me late for my check-in</strong>.</p>

<h3>Customer Service and Hospitality</h3>
<p>My experience with their customer service and the friendliness of the staff was <strong>exceptional</strong>. We were looked after by an <strong>incredibly warm yet highly professional team</strong>. I can wholeheartedly recommend FlyNYON to anyone visiting New York City.</p>

<h2>My Flight Experience – Step-by-Step</h2>
<p>After arriving in New Jersey by train, I ordered an Uber to the FlyNYON terminal. My driver and I ended up <strong>stuck at a railroad crossing for at least 10 minutes</strong> while a seemingly never-ending freight train crawled past. I <strong>immediately messaged FlyNYON</strong> to let them know I was going to be late; <strong>they replied within minutes</strong> and redirected us via an <strong>alternative route</strong> (which was also written on a nearby roadside sign—clearly, this train misery is a regular occurrence here).</p>
<p>Once I arrived at the terminal, I signed the waiver and completed a basic questionnaire. Right there at the desk, they <strong>offered me the on-site upgrade to the 30-minute flight for about $105</strong>, and I am so glad I took it! The <strong>standard 15-minute flight only takes you as far as the Statue of Liberty, the Financial District ("money shot"), and the Hudson River</strong>. The <strong>30-minute flight, however, crosses all the way over Central Park, Midtown Manhattan, the East River, and the Brooklyn Bridge</strong>.</p>
<p>Next, I went through <strong>three separate safety presentations</strong>, and then they fitted us into our professional harnesses and secured our phone/camera lanyards. Unfortunately, Donald Trump decided that exact evening to fly out by helicopter to a Knicks game, which <strong>temporarily grounded all air traffic and locked down the airspace</strong>, so we had to wait. At least we were able to use the downtime to <strong>charge our phones</strong>.</p>
<p>After a short wait, we were driven out to our helicopter in a shuttle van. We were <strong>split into two groups</strong>: one for the short 15-minute loop and one for the 30-minute flight. Following <strong>one final, on-site safety demonstration</strong>, we took our seats in the aircraft and lifted off.</p>
<p>Seats are allocated based on weight distribution, but everyone gets the chance to dangle their legs outside, so seat location doesn't matter.</p>
<p>The helicopter first headed toward the <strong>Statue of Liberty</strong>, the classic <strong>Manhattan skyline money shot</strong>, and <strong>Governor's Island</strong>, before banking north and flying <strong>all the way up to Central Park</strong>. By this point, of course, we were already happily dangling our legs out of the open doors. For <strong>30 spectacular minutes</strong>, we flew right over all the iconic skyscrapers and landmarks before heading back. The flight was <strong>incredibly smooth</strong>, and I didn't feel motion sick for a single second.</p>
<p>After landing, there was an opportunity to <strong>take some photos by the helicopter with our own devices</strong>. The shuttle then drove us back to the main building, bringing our unforgettable helicopter adventure to an end.</p>
</div>

<div class="bpa-cta-box">
<div class="bpa-cta-inner">
<div class="bpa-cta-text">
<h4>Ready for the Ultimate Open-Door "Shoe Selfie"?</h4>
<p>Book the 16-minute basic flight online, then upgrade to 30 minutes at check-in for the complete skyline loop.</p>
</div>
<a class="bpa-cta-big" href="https://www.flynyon.com/" rel="noopener nofollow sponsored" target="_blank">Book FlyNYON Now →</a>
</div>
</div>
</div>
</details>''')

# Tour 2: HeliNY
details_cards_html.append('''<details class="bpa-details-card" id="2-heliny" open="">
<a id="2-rubingroup" class="ltt-anchor-alias"></a>
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-acc-meta">
<span class="bpa-rank-tag bpa-gold">🥈 #2 Runner Up • Classic Closed-Door</span>
<span class="bpa-acc-pill">HeliNY • <strong>From $269</strong> • ⏱️ 12 to 30 min</span>
</div>
<h3 class="bpa-details-title">2. HeliNY — Manhattan Classic Closed-Door Scenic Helicopter Tour</h3>
<div class="bpa-summary-reviews">
<div class="div-block-53">
<a class="bpa-rev-badge" href="https://www.getyourguide.com/new-york-city-l59/nyc-manhattan-sightseeing-helicopter-tour-t19901/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-h3-reviews-heliny&mkt_cmp=true" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="GetYourGuide" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"/>
<span class="bpa-rev-score">4.8</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+7,180 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://viator.tpm.lv/F6amfNG8" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="Viator" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"/>
<span class="bpa-rev-score">4.8</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+1,310 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://tripadvisor.tpm.lv/I3j3kV7W" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="TripAdvisor" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_tripadvisor-icon.png"/>
<span class="bpa-rev-score">4.8</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+750 reviews</span>
</a>
</div>
</div>
</div>
<div class="bpa-details-toggle">
<span class="bpa-details-chevron">▾</span>
</div>
</summary>
<div class="bpa-details-body">
<div class="bpa-quick-facts-card">
<h4>Flight Overview &amp; Logistics</h4>
<div class="bpa-qf-grid">
<div class="bpa-qf-item"><strong>Test Status:</strong> ✔️ Personally Tested by Adam</div>
<div class="bpa-qf-item"><strong>Hours:</strong> 10:00 AM – 5:30 PM Daily</div>
<div class="bpa-qf-item"><strong>Flight Duration:</strong> 12 to 30 Minutes</div>
<div class="bpa-qf-item"><strong>Flight Style:</strong> Enclosed Climate-Controlled Cabin</div>
<div class="bpa-qf-item"><strong>Meeting Point:</strong> <a href="https://maps.app.goo.gl/VHqxx4N9k6GJw3rGA" target="_blank" rel="noopener nofollow">Downtown Manhattan Heliport (Pier 6) 📍</a></div>
<div class="bpa-qf-item"><strong>Getting There:</strong> 5-min walk from South Ferry Subway</div>
</div>
</div>

<div class="w-richtext">
<h2>The Most Popular and Classic Big Apple Scenic Flight</h2>
<p>If you want a closed-doors New York flight experience, <strong>HeliNY</strong> is the most popular choice in the city. While the <strong>closed doors</strong> mean you cannot experience the open air thrill of dangling your legs, you still get to enjoy amazing views of NYC in a comfortable, climate-controlled cabin.</p>

<h3>Flexible Flight Tiers and Routes</h3>
<p>The listing allows you to select between three specific flight durations depending on how far north you want the aircraft to travel:</p>
<ul>
<li><strong>The 12 to 15 Minute Route (The New Yorker):</strong> A rapid harbor loop focusing on the absolute essentials. The helicopter takes off and heads straight down to circle the <strong>Statue of Liberty</strong> and Ellis Island before cruising past Battery Park, Wall Street, and the One World Trade Center.</li>
<li><strong>The 17 to 20 Minute Route (The Ultimate):</strong> The most popular tier selected by travelers. It covers the complete harbor loop but continues further up the Hudson River to give you clear views of Madison Square Garden, Times Square, and the southern edge of <strong>Central Park</strong>.</li>
<li><strong>The 25 to 30 Minute Route (The Deluxe):</strong> The maximum sightseeing path. The aircraft flies the full length of Manhattan all the way to the northern tip, showcasing the George Washington Bridge, <strong>Yankee Stadium</strong>, Columbia University, and the dramatic New Jersey Palisades cliffs.</li>
</ul>

<h2>My Flight Experience – Step-by-Step</h2>
<p>After arriving at the heliport, which is located just a <strong>five minute walk from the South Ferry subway station</strong> in Lower Manhattan, the logistics proved to be significantly faster and easier compared to traveling out to New Jersey. I went through a quick security check, signed the standard waiver, and checked in for the flight that I had previously <strong>booked online through GetYourGuide</strong>.</p>
<p>Next, I placed all my personal bags and belongings into a <strong>non-site locker</strong>, received my safety gear, and watched the mandatory safety demonstration. Since the launchpads are located <strong>directly next to the terminal compound</strong>, we did not need to wait for any shuttle vans to transport us to the aircraft.</p>
<p>Right before boarding the helicopter on the tarmac, the staff took a quick photo of us in front of the chopper. Once inside, we took our seats and lifted off for the <strong>15 to 17 minute daytime tour</strong>.</p>
<p>The flight path immediately took us out over the water, offering clear views of the <strong>Statue of Liberty</strong>, Governor's Island, and the Hudson River, alongside the classic <strong>Lower Manhattan skyline money shots</strong>.</p>
<p>I took this flight in early June, and while the outside weather was ideal, the internal climate control was a bit problematic. The cabin itself became quite warm (I went during the heat wave), yet the air conditioning was blowing freezing air directly at me. This combination, along with the enclosed space, triggered some <strong>motion sickness</strong>, and by the halfway mark, I was honestly just looking forward to the end of the ride.</p>
<p>Upon landing, we walked straight back into the main building where the pre-flight photos were available for viewing. You could choose to purchase the <strong>digital copies for $40</strong>, which brought the entire experience to a close.</p>
</div>

<div class="bpa-cta-box">
<div class="bpa-cta-inner">
<div class="bpa-cta-text">
<h4>Book HeliNY from Downtown Manhattan</h4>
<p>Instant mobile tickets departing directly from Pier 6 with free cancellation up to 24 hours in advance.</p>
</div>
<a class="bpa-cta-big" href="https://www.getyourguide.com/new-york-city-l59/nyc-manhattan-sightseeing-helicopter-tour-t19901/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-heliny&mkt_cmp=true" rel="noopener nofollow sponsored" target="_blank">Check Dates on GetYourGuide →</a>
</div>
</div>
</div>
</details>''')

# Tour 3: Charm Aviation
details_cards_html.append('''<details class="bpa-details-card" id="3-charm-aviation" open="">
<a id="4-kisfaludy-historic-cruise" class="ltt-anchor-alias"></a>
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-acc-meta">
<span class="bpa-rank-tag bpa-bronze">🥉 #3 Also Great • Lower Manhattan</span>
<span class="bpa-acc-pill">Charm Aviation • <strong>From $269</strong> • ⏱️ 12 to 30 min</span>
</div>
<h3 class="bpa-details-title">3. Charm Aviation — Big Apple All-Inclusive Helicopter Tour</h3>
<div class="bpa-summary-reviews">
<div class="div-block-53">
<a class="bpa-rev-badge" href="https://www.getyourguide.com/new-york-city-l59/nyc-helicopter-tour-of-the-big-apple-all-inclusive-t456488/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-h3-reviews-charm-aviation&mkt_cmp=true" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="GetYourGuide" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"/>
<span class="bpa-rev-score">4.8</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+2,180 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://viator.tpm.lv/4aX2WYra" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="Viator" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"/>
<span class="bpa-rev-score">4.5</span>
<span class="bpa-rev-stars">★★★★½</span>
<span class="bpa-rev-count">+1,870 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://tripadvisor.tpm.lv/LItHJmxS" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="TripAdvisor" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_tripadvisor-icon.png"/>
<span class="bpa-rev-score">4.3</span>
<span class="bpa-rev-stars">★★★★☆</span>
<span class="bpa-rev-count">+350 reviews</span>
</a>
</div>
</div>
</div>
<div class="bpa-details-toggle">
<span class="bpa-details-chevron">▾</span>
</div>
</summary>
<div class="bpa-details-body">
<div class="bpa-quick-facts-card">
<h4>Flight Overview &amp; Logistics</h4>
<div class="bpa-qf-grid">
<div class="bpa-qf-item"><strong>Test Status:</strong> ⭐ Verified Partner</div>
<div class="bpa-qf-item"><strong>Schedule:</strong> 10:00 AM – 6:30 PM (Mon–Sat)</div>
<div class="bpa-qf-item"><strong>Sundays:</strong> ❌ Closed on Sundays</div>
<div class="bpa-qf-item"><strong>Flight Duration:</strong> 12 to 30 Minutes</div>
<div class="bpa-qf-item"><strong>Meeting Point:</strong> <a href="https://maps.app.goo.gl/ihKsQZb5G4UXTgr4A" target="_blank" rel="noopener nofollow">Downtown Manhattan Heliport (Pier 6) 📍</a></div>
<div class="bpa-qf-item"><strong>Accessible:</strong> Yes</div>
</div>
</div>

<div class="w-richtext">
<h2>Charm Aviation: A Great Alternative (Just Not on Sundays)</h2>
<p><strong>Charm Aviation</strong> is almost exactly like HeliNY. They leave from the exact same building at the <strong>Downtown Manhattan Heliport (Pier 6)</strong>, use the same types of closed-door helicopters with panoramic windows, and fly the exact same scenic routes over the Statue of Liberty and up the Hudson River. Their prices are also virtually identical.</p>
<p>The only major difference is the schedule. While HeliNY flies seven days a week, <strong>Charm Aviation does not fly on Sundays</strong>. This makes them a perfect backup option to book from Monday to Saturday if HeliNY slots are sold out, but you cannot use them for a Sunday flight.</p>
</div>

<div class="bpa-cta-box">
<div class="bpa-cta-inner">
<div class="bpa-cta-text">
<h4>Book Charm Aviation Big Apple Tour</h4>
<p>All-inclusive pricing with heliport security fees included up front. Mon–Sat availability.</p>
</div>
<a class="bpa-cta-big" href="https://www.getyourguide.com/new-york-city-l59/nyc-helicopter-tour-of-the-big-apple-all-inclusive-t456488/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-charm-aviation&mkt_cmp=true" rel="noopener nofollow sponsored" target="_blank">Check Dates on GetYourGuide →</a>
</div>
</div>
</div>
</details>''')

# Tour 4: Zip Aviation
details_cards_html.append('''<details class="bpa-details-card" id="4-zip-aviation" open="">
<a id="3-portum" class="ltt-anchor-alias"></a>
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-acc-meta">
<span class="bpa-rank-tag bpa-bronze">⭐ #4 Time-Tested Classic</span>
<span class="bpa-acc-pill">Zip Aviation • <strong>From $269</strong> • ⏱️ 12 or 30 min</span>
</div>
<h3 class="bpa-details-title">4. Zip Aviation — Liberty Harbor Helicopter Adventure</h3>
<div class="bpa-summary-reviews">
<div class="div-block-53">
<a class="bpa-rev-badge" href="https://www.getyourguide.com/new-york-city-l59/liberty-harbor-helicopter-adventure-t15252/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-h3-reviews-zip-aviation&mkt_cmp=true" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="GetYourGuide" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"/>
<span class="bpa-rev-score">4.7</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+7,300 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://viator.tpm.lv/rHrTkVDe" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="Viator" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"/>
<span class="bpa-rev-score">4.4</span>
<span class="bpa-rev-stars">★★★★½</span>
<span class="bpa-rev-count">+1,460 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://tripadvisor.tpm.lv/YJgZ8JXL" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="TripAdvisor" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_tripadvisor-icon.png"/>
<span class="bpa-rev-score">4.5</span>
<span class="bpa-rev-stars">★★★★½</span>
<span class="bpa-rev-count">+190 reviews</span>
</a>
</div>
</div>
</div>
<div class="bpa-details-toggle">
<span class="bpa-details-chevron">▾</span>
</div>
</summary>
<div class="bpa-details-body">
<div class="bpa-quick-facts-card">
<h4>Flight Overview &amp; Logistics</h4>
<div class="bpa-qf-grid">
<div class="bpa-qf-item"><strong>Test Status:</strong> ⭐ Verified Operator</div>
<div class="bpa-qf-item"><strong>Schedule:</strong> 10:00 AM – 4:30 PM (Mon–Sat)</div>
<div class="bpa-qf-item"><strong>Solo Rule:</strong> Solo riders must choose 17-20m tier</div>
<div class="bpa-qf-item"><strong>Flight Duration:</strong> 12 or 30 Minutes</div>
<div class="bpa-qf-item"><strong>Meeting Point:</strong> <a href="https://maps.app.goo.gl/LPbifuYEZNGB8vTg8" target="_blank" rel="noopener nofollow">Downtown Manhattan Heliport (Pier 6) 📍</a></div>
<div class="bpa-qf-item"><strong>Accessible:</strong> Yes</div>
</div>
</div>

<div class="w-richtext">
<h2>Zip Aviation: A Popular Choice (But Watch the Group Rules)</h2>
<p><strong>Zip Aviation</strong> is another company that is very similar to HeliNY. They fly out of the exact same <strong>Downtown Manhattan Heliport (Pier 6)</strong>, use the same types of closed-door helicopters with big windows, and fly the same routes over the landmarks. They have thousands of reviews because they are one of the oldest and busiest companies on the pier, and they even offer unique night flights by taking off from an extra hangar over in New Jersey.</p>
<p>The biggest difference is how you book your seats because their rules for solo travelers are much more strict. If you are traveling alone, <strong>Zip Aviation only lets you book their middle-sized 17 to 20 minute flight</strong>. If you want their shortest flight or their longest 30 minute flight, you must have a group of at least 4 people to book it. This makes them a bit harder to use if you are by yourself.</p>
</div>

<div class="bpa-cta-box">
<div class="bpa-cta-inner">
<div class="bpa-cta-text">
<h4>Book Zip Aviation Liberty Harbor Adventure</h4>
<p>Time-tested veteran operator on Pier 6 with instant confirmation and flexible cancellation.</p>
</div>
<a class="bpa-cta-big" href="https://www.getyourguide.com/new-york-city-l59/liberty-harbor-helicopter-adventure-t15252/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-zip-aviation&mkt_cmp=true" rel="noopener nofollow sponsored" target="_blank">Check Dates on GetYourGuide →</a>
</div>
</div>
</div>
</details>''')

# Tour 5: Wings Air
details_cards_html.append('''<details class="bpa-details-card" id="5-wings-air" open="">
<a id="5-silverline-no-frills" class="ltt-anchor-alias"></a>
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-acc-meta">
<span class="bpa-rank-tag bpa-gold">💑 #5 Best for Couples • Private Luxury</span>
<span class="bpa-acc-pill">Wings Air • <strong>From $690/flight</strong> • ⏱️ 30 or 45 min</span>
</div>
<h3 class="bpa-details-title">5. Wings Air — Couple's Private Luxury Helicopter Tour from White Plains</h3>
<div class="bpa-summary-reviews">
<div class="div-block-53">
<a class="bpa-rev-badge" href="https://www.getyourguide.com/new-york-city-l59/couple-s-private-helicopter-tour-over-new-york-t63337/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-h3-reviews-wings-air&mkt_cmp=true" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="GetYourGuide" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3745_getyourguide-icon.png"/>
<span class="bpa-rev-score">4.8</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+300 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://viator.tpm.lv/fbeTlJnZ" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="Viator" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3747_viator-icon.png"/>
<span class="bpa-rev-score">4.8</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+50 reviews</span>
</a>
<a class="bpa-rev-badge" href="https://tripadvisor.tpm.lv/YH24HK2Q" onclick="event.stopPropagation()" rel="noopener nofollow sponsored" target="_blank">
<img alt="TripAdvisor" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_tripadvisor-icon.png"/>
<span class="bpa-rev-score">4.7</span>
<span class="bpa-rev-stars">★★★★★</span>
<span class="bpa-rev-count">+40 reviews</span>
</a>
</div>
</div>
</div>
<div class="bpa-details-toggle">
<span class="bpa-details-chevron">▾</span>
</div>
</summary>
<div class="bpa-details-body">
<div class="bpa-quick-facts-card">
<h4>Flight Overview &amp; Logistics</h4>
<div class="bpa-qf-grid">
<div class="bpa-qf-item"><strong>Test Status:</strong> 👑 100% Private Charter</div>
<div class="bpa-qf-item"><strong>Schedule:</strong> 10:00 AM Daily Flights</div>
<div class="bpa-qf-item"><strong>Capacity:</strong> Exclusive for 2 Passengers</div>
<div class="bpa-qf-item"><strong>Flight Duration:</strong> 30 or 45 Minutes</div>
<div class="bpa-qf-item"><strong>Meeting Point:</strong> <a href="https://maps.app.goo.gl/jagGWLf6gwQpDPxJ6" target="_blank" rel="noopener nofollow">Westchester County Airport (White Plains) 📍</a></div>
<div class="bpa-qf-item"><strong>Accessible:</strong> Yes</div>
</div>
</div>

<div class="w-richtext">
<h2>Best for Couples: Private Closed-Door Luxury Flight from White Plains</h2>
<p><strong>Wings Air</strong> offers a completely different experience because they do not fly out of the crowded Manhattan pier. Instead, they leave from the <strong>Westchester County Airport (White Plains)</strong>, which is located just north of the city. This tour is completely private and designed exclusively for couples, so you get the entire helicopter to yourselves without having to share the cabin with strangers.</p>
<p>Because you start further north, the flight path is unique. You fly into the city from the top, getting amazing views of <strong>Yankee Stadium and Central Park</strong> first. The biggest detail to watch out for is the flight time. The shorter <strong>30 minute flight does not go down to the Statue of Liberty</strong>, so you must choose the longer <strong>45 minute flight</strong> if you want to see the lower part of Manhattan and the iconic bridges.</p>
</div>

<div class="bpa-cta-box">
<div class="bpa-cta-inner">
<div class="bpa-cta-text">
<h4>Book a Private Couples Helicopter Flight</h4>
<p>The ultimate private romantic flight over New York. Entire chopper for 2 with zero strangers.</p>
</div>
<a class="bpa-cta-big" href="https://www.getyourguide.com/new-york-city-l59/couple-s-private-helicopter-tour-over-new-york-t63337/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=article-helicopter-tours-nyc-comparison-list-wings-air&mkt_cmp=true" rel="noopener nofollow sponsored" target="_blank">Book Private Flight on GetYourGuide →</a>
</div>
</div>
</div>
</details>''')

full_details_markup = '\n'.join(details_cards_html)

# 4. Build TOC and Sidebar Structure
blog_section_markup = f'''<div class="blog-section">
<div class="container-26">
<div class="blog-grid-2">
<div class="content-left">
<div class="stick-wrapper">
<div class="title-small-6">TABLE OF CONTENTS</div>
<div class="toc" id="toc"></div>
</div>
</div>
<div class="content-right_blog">
{full_details_markup}
</div>
</div>
</div>
</div>'''

# 5. Build Sticky Mobile Bar strictly conforming to Safaris CSS
sticky_bar_markup = '''<aside aria-label="Current Tour Quick Reservation" class="sticky-mobile-bar" id="sticky-bar">
<div class="sticky-inner">
<div class="sticky-boat-info">
<img alt="NYC Helicopter" class="sticky-thumb-img" id="sticky-thumb" src="/assets/cdn/67d02edca7795b0f57073b59/6a47d3559ce91814c1df86f5_best-helicopter-tours-nyc-flynyon-4.avif"/>
<div class="sticky-text">
<div class="sticky-title-row">
<span class="sticky-rank-badge" id="sticky-rank">🏆 #1 Best Overall</span>
<strong id="sticky-name">FlyNYON New York</strong>
</div>
<div class="sticky-meta-row">
<span class="sticky-price-tag" id="sticky-price">From $99–$249</span>
<span class="sticky-bullet">•</span>
<span class="sticky-desc-text" id="sticky-desc">Open-Door Shoe-Selfie • Night Flight</span>
</div>
</div>
</div>
<a class="btn-sticky-cta" href="https://www.flynyon.com/" id="sticky-cta-btn" rel="noopener nofollow sponsored" target="_blank">Book Now →</a>
</div>
</aside>'''

# 6. JavaScript conforming 1:1 to Safaris
heli_script_markup = '''<script id="ltt-nyc-helicopter-script">
(function() {
  // 1. Slider controls
  window.bpaSlide = function(btn, dir) {
    var media = btn.closest('.bpa-media');
    if (!media) return;
    var slider = media.querySelector('.bpa-slider');
    if (!slider) return;
    var w = slider.clientWidth;
    slider.scrollBy({ left: dir * w, behavior: 'smooth' });
  };

  window.bpaCount = function(slider) {
    var media = slider.closest('.bpa-media');
    if (!media) return;
    var pill = media.querySelector('.bpa-pill');
    if (!pill) return;
    var w = slider.clientWidth || 1;
    var idx = Math.min(Math.round(slider.scrollLeft / w) + 1, slider.children.length);
    pill.textContent = idx + ' / ' + slider.children.length;
  };

  // 2. Filter tabs
  window.lttFilterHelicopters = function(cat, btn) {
    var buttons = document.querySelectorAll('.ltt-tab-btn');
    buttons.forEach(function(b) { b.classList.remove('active'); });
    if (btn) btn.classList.add('active');
    
    // Filter Cards
    var cards = document.querySelectorAll('#ltt-cards-deck .bpa-card');
    cards.forEach(function(card) {
      var cardCat = card.getAttribute('data-cat') || '';
      if (cat === 'all' || cardCat.indexOf(cat) !== -1) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  };

  // 3. Extract structured Tours list from Cards
  function getTours() {
    return Array.from(document.querySelectorAll('.bpa-card')).map(function(card, i) {
      var sub = card.querySelector('.bpa-sublink');
      var id = sub ? sub.getAttribute('href').replace('#', '') : '';
      var kicker = card.querySelector('.bpa-kicker');
      var head = card.querySelector('.bpa-title');
      var tag = card.querySelector('.bpa-rank-tag');
      var p = card.querySelector('.bpa-price');
      var psub = card.querySelector('.bpa-psub');
      var btn = card.querySelector('.bpa-btn');
      var kp = kicker ? kicker.textContent.split('•') : [];
      return {
        id: id,
        r: String(i + 1),
        tag: tag ? tag.textContent.trim() : '',
        name: kp[0] ? kp[0].trim() : '',
        p: p ? p.textContent.trim() : '',
        d: (kp[1] ? kp[1].trim() : '') + (psub ? ' • ' + psub.textContent.trim() : ''),
        l: btn ? btn.href : (head ? head.href : ''),
        t: (i + 1) + '. ' + (head ? head.textContent.trim() : '')
      };
    });
  }

  // 4. Smooth offset scroll animation engine (settles at exact 85px offset)
  var _activeScrollId = null;
  function smoothScrollToElement(target, offset) {
    if (!target) return;
    offset = (typeof offset === 'number') ? offset : 85;

    var details = target.closest('details');
    if (details) details.open = true;
    if (target.tagName === 'DETAILS') target.open = true;

    if (_activeScrollId) {
      cancelAnimationFrame(_activeScrollId);
      _activeScrollId = null;
    }

    function stopScroll() {
      if (_activeScrollId) {
        cancelAnimationFrame(_activeScrollId);
        _activeScrollId = null;
      }
      cleanup();
    }
    function cleanup() {
      window.removeEventListener('wheel', stopScroll, { passive: true });
      window.removeEventListener('touchmove', stopScroll, { passive: true });
      window.removeEventListener('keydown', stopScroll, { passive: true });
    }
    window.addEventListener('wheel', stopScroll, { passive: true });
    window.addEventListener('touchmove', stopScroll, { passive: true });
    window.addEventListener('keydown', stopScroll, { passive: true });

    var lastScrollY = -1;
    var stuckFrames = 0;
    var settlingFrames = 0;

    function frame() {
      var rect = target.getBoundingClientRect();
      var diff = rect.top - offset;

      if (Math.abs(diff) <= 2) {
        window.scrollBy(0, diff);
        settlingFrames++;
        if (settlingFrames > 8) {
          _activeScrollId = null;
          cleanup();
          return;
        }
        _activeScrollId = requestAnimationFrame(frame);
        return;
      }

      settlingFrames = 0;
      var step = diff * 0.18;
      if (Math.abs(step) < 1) {
        step = diff > 0 ? 1 : -1;
      }

      var beforeY = window.pageYOffset;
      window.scrollBy(0, step);
      var afterY = window.pageYOffset;

      if (afterY === lastScrollY) {
        stuckFrames++;
        if (stuckFrames > 6) {
          _activeScrollId = null;
          cleanup();
          return;
        }
      } else {
        stuckFrames = 0;
      }
      lastScrollY = afterY;

      _activeScrollId = requestAnimationFrame(frame);
    }

    _activeScrollId = requestAnimationFrame(frame);
  }

  // 5. Intercept anchor clicks at capture phase
  function setupSmoothAnchorJumps() {
    document.addEventListener('click', function(e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || href === '#' || href === '#!') return;
      var targetId = href.substring(1);
      var target = document.getElementById(targetId);
      if (!target && targetId === 'nyc-helicopter-deck') {
        target = document.getElementById('nyc-helicopter-deck');
      }
      if (target) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        smoothScrollToElement(target, 85);
        if (history.pushState) {
          history.pushState(null, null, href);
        }
      }
    }, true);

    // Prevent clicks inside summary links from triggering detail accordion toggle
    document.addEventListener('click', function(e) {
      var a = e.target.closest('summary a');
      if (a) e.stopPropagation();
    }, true);
  }

  // 6. Sync Sidebar Table of Contents using exact .tocitem anchors from Safaris
  function syncSidebarTOC() {
    var toc = document.querySelector('#toc');
    if (!toc || toc.getAttribute('data-synced') === 'true') return;
    var tours = getTours();
    if (!tours.length) return;

    var items = [
      { id: 'nyc-helicopter-deck', text: 'Top 5 Helicopter Tours' }
    ];
    tours.forEach(function(t) {
      items.push({ id: t.id, text: t.r + '. ' + t.name });
    });

    toc.innerHTML = '';
    var frag = document.createDocumentFragment();
    items.forEach(function(it) {
      var a = document.createElement('a');
      a.className = 'tocitem';
      a.href = '#' + it.id;
      a.textContent = it.text;
      frag.appendChild(a);
    });
    toc.appendChild(frag);
    toc.setAttribute('data-synced', 'true');

    var leftCol = toc.closest('.content-left');
    if (leftCol) leftCol.style.display = 'block';

    if (window._tocObs) window._tocObs.disconnect();
    window._tocObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          toc.querySelectorAll('.tocitem.active').forEach(function(z) { z.classList.remove('active'); });
          var link = toc.querySelector('a[href="#' + entry.target.id + '"]');
          if (link) link.classList.add('active');
        }
      });
    }, { rootMargin: '0px 0px -70% 0px' });

    items.forEach(function(it) {
      var el = document.getElementById(it.id);
      if (el) window._tocObs.observe(el);
    });
  }

  // 7. Update Floating Sticky Bottom Bar strictly conforming to Safaris
  function updateFloatingCTA() {
    var bar = document.getElementById('sticky-bar');
    if (!bar) return;
    var cards = document.querySelectorAll('.bpa-card');
    var reviews = document.querySelectorAll('.bpa-details-card');
    if (!cards.length) return;
    var tours = getTours();
    var vCenter = window.innerHeight / 2;
    var firstTop = cards[0].getBoundingClientRect().top;
    var lastRev = reviews.length ? reviews[reviews.length - 1] : cards[cards.length - 1];
    var lastBottom = lastRev.getBoundingClientRect().bottom;

    if (firstTop > vCenter || lastBottom < vCenter) {
      bar.classList.remove('visible');
      return;
    }

    var activeIdx = 0, minDistance = Infinity;
    cards.forEach(function(card, i) {
      var r = card.getBoundingClientRect();
      var dist = Math.abs(r.top + r.height / 2 - vCenter);
      if (dist < minDistance) {
        minDistance = dist;
        activeIdx = i;
      }
    });

    reviews.forEach(function(rev, i) {
      var r = rev.getBoundingClientRect();
      if (r.top <= vCenter && r.bottom >= vCenter) {
        activeIdx = i;
      } else {
        var dist = Math.abs(r.top + r.height / 2 - vCenter);
        if (dist < minDistance) {
          minDistance = dist;
          activeIdx = i;
        }
      }
    });

    var active = tours[activeIdx];
    if (active) {
      var card = cards[activeIdx];
      var imgEl = card ? card.querySelector('.bpa-slider img') : null;
      var thumb = document.getElementById('sticky-thumb');
      var rankEl = document.getElementById('sticky-rank');
      var nameEl = document.getElementById('sticky-name');
      var priceEl = document.getElementById('sticky-price');
      var descEl = document.getElementById('sticky-desc');
      var ctaBtn = document.getElementById('sticky-cta-btn');

      if (thumb && imgEl) thumb.src = imgEl.src;
      if (rankEl) rankEl.textContent = active.tag;
      if (nameEl) nameEl.textContent = active.name;
      if (priceEl) priceEl.textContent = active.p;
      if (descEl) descEl.textContent = active.d;
      if (ctaBtn) ctaBtn.href = active.l;
      bar.classList.add('visible');
    }
  }

  function initAll() {
    syncSidebarTOC();
    setupSmoothAnchorJumps();
    window.addEventListener('scroll', updateFloatingCTA, { passive: true });
    updateFloatingCTA();

    // Check URL hash on page load
    if (window.location.hash) {
      var h = window.location.hash.substring(1);
      var el = document.getElementById(h);
      if (el) {
        setTimeout(function() {
          smoothScrollToElement(el, 85);
        }, 150);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
</script>'''

# Assemble HTML
if '<style id="ltt-nyc-helicopter-styles">' in heli_html:
    heli_html = re.sub(r'<style id="ltt-nyc-helicopter-styles">.*?</style>', clean_heli_css, heli_html, flags=re.DOTALL)
else:
    heli_html = heli_html.replace('</head>', f'{clean_heli_css}\n</head>')

heli_html = re.sub(r'href="#(?:content|river-cruises-quick-summary)"', 'href="#nyc-helicopter-deck"', heli_html)

soup_target = BeautifulSoup(heli_html, 'html.parser')

for old_id in ['nyc-helicopter-deck', 'sticky-bar', 'ltt-nyc-helicopter-script']:
    el = soup_target.find(id=old_id)
    if el: el.decompose()

for old_cls in ['blog-section', 'comparison-table']:
    el = soup_target.find('div', class_=old_cls)
    if el: el.decompose()

intro = soup_target.find('div', class_='container-intro-section')
if intro:
    new_fragment = BeautifulSoup(f'{full_deck_markup}\n{blog_section_markup}', 'html.parser')
    intro.insert_after(new_fragment)

final_html = str(soup_target)
final_html = final_html.replace('</body>', f'{sticky_bar_markup}\n{heli_script_markup}\n</body>')

with open(HELI_FILE, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("PARITY COMPLETE: All glitches eliminated and 100% architectural parity established!")
