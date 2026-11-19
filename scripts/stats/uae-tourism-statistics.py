"""UAE tourism statistics. Figures: UAE Ministry of Economy and Tourism (via Gulf News / WAM),
World Travel and Tourism Council (WTTC) Economic Impact Research, Dubai DET, DCT Abu Dhabi.
Accessed 19 November 2026."""


def a(url, text):
    return f'<a href="{url}" rel="noopener" target="_blank">{text}</a>'


MOE25 = "https://gulfnews.com/business/tourism/uae-hotel-revenue-hits-dh492-billion-in-2025-guest-numbers-reach-323-million-1.500507957"
MOE24 = "https://www.wam.ae/en/article/bj249l1-uae-tourism-generates-aed45-billion-hotel-revenues"
MOE24B = "https://www.arabianbusiness.com/industries/travel-hospitality/uae-tourism-revenues-reach-12-2bn-in-2024-as-hotel-guest-numbers-grow-9-5"
WTTC = "https://wttc.org/news/international-traveller-spend-uae-to-reach-a-record-aed-228bn"
WTTC2 = "https://www.thenationalnews.com/business/aviation/2025/09/29/uae-expected-to-host-276-million-international-visitors-this-year-wttc-says"
STRAT = "https://www.wam.ae/en/article/hszrfv25-mohammed-bin-rashid-launches-uae-tourism-strategy"
STRAT23 = "https://www.moet.gov.ae/en/-/emirates-tourism-council-reviews-progress-made-in-the-achievement-of-uae-tourism-strategy-2031"
DET25 = "https://www.mediaoffice.ae/en/news/2026/february/09-02/dubais-tourism-industry-achieves-third-successive-record-breaking-year"
DCT24 = "https://en.aletihad.ae/news/business/4579524/abu-dhabi-hotel-sector-booms-with-5-8-million-guests-in-2024"

S_MOE = a(MOE25, "UAE Ministry of Economy and Tourism, 2025 hotel results (Gulf News, 15 Apr 2026)")
S_MOE24 = a(MOE24, "Ministry of Economy and Tourism, 2024 (WAM)")
S_WTTC = a(WTTC, "WTTC, UAE Economic Impact Research 2025")

SPEC = {
    "slug": "uae-tourism-statistics",
    "short_name": "UAE Tourism Statistics",
    "title_tag": "UAE Tourism Statistics 2026: 32.3M Hotel Guests, Spending & GDP",
    "meta_description": "UAE hotels hosted a record 32.34 million guests in 2025 and earned AED 49.2 billion. Official data on occupancy, visitor spending, jobs and Dubai vs Abu Dhabi.",
    "headline": "UAE Tourism Statistics 2026: Hotel Guests, Spending and the Economy",
    "breadcrumb": "UAE Tourism Statistics (2026)",
    "kicker_badge": "Official Data · 2025",
    "h1_main": "UAE Tourism Statistics 2026",
    "h1_muted": "(Visitors, Hotels & Spending)",
    "author_role": "Compiled from Ministry of Economy and Tourism, WTTC, DET and DCT data",
    "image": "/assets/best-burj-khalifa-tickets/01-sky-148-01.avif",
    "lead": [
        "Hotels in the United Arab Emirates welcomed a record <strong>32.34 million guests</strong> in 2025 and earned <strong>AED 49.2 billion</strong> (about $13.4 billion), according to the Ministry of Economy and Tourism. Travel and tourism is worth almost <strong>13% of the UAE economy</strong> and supports about <strong>925,000 jobs</strong>.",
        "This report covers the whole country: how many guests the seven emirates host, how full the hotels are, how much visitors spend, what tourism adds to the economy and how Dubai and Abu Dhabi compare. For city-level detail, see our <a href=\"/dubai-tourism-statistics\">Dubai tourism statistics</a> and <a href=\"/abu-dhabi-tourism-statistics\">Abu Dhabi tourism statistics</a>. Every chart has a data table and a link to its source.",
    ],
    "citations": [MOE25, MOE24, MOE24B, WTTC, WTTC2, STRAT, STRAT23, DET25, DCT24],
    "sections": [
        {"h2": "Key UAE tourism statistics (2025)", "toc": "Key UAE tourism statistics", "blocks": [
            {"tiles": [("32.34M", "hotel guests across the seven emirates"), ("AED 49.2bn", "hotel revenue (+9.7%)"),
                       ("79.3%", "average hotel occupancy"), ("12.9%", "of GDP from travel and tourism (WTTC)")]},
            "<ul role=\"list\">"
            "<li>UAE hotels hosted <strong>32.34 million guests</strong> in 2025, up 5.2% from 30.75 million in 2024 and 15% more than in 2023 (28.08 million).</li>"
            "<li>Hotel revenue rose 9.7% to <strong>AED 49.21 billion</strong>, and guests stayed <strong>110.62 million nights</strong> (+5.9%).</li>"
            "<li>Occupancy averaged <strong>79.3%</strong> across about <strong>217,000 hotel rooms</strong>.</li>"
            "<li>International visitors were forecast to spend a record <strong>AED 228.5 billion</strong> in 2025, 37% more than in 2019 (WTTC).</li>"
            "<li>Travel and tourism contributes about <strong>AED 267.5 billion</strong> to the economy (12.9% of GDP) and supports more than 925,000 jobs.</li>"
            "<li><strong>Dubai</strong> holds about 71% of the country's hotel rooms; the national target is <strong>40 million hotel guests by 2031</strong>, and 2025 reached 81% of it.</li></ul>",
        ]},
        {"h2": "How many tourists visit the UAE each year?", "blocks": [
            "<p>UAE hotels welcomed <strong>32.34 million guests in 2025</strong>, a record, after 30.75 million in 2024 and 28.08 million in 2023. That is the official national measure, and it counts every check-in at a hotel establishment, from international tourists and business travellers to UAE residents on a staycation.</p>",
            {"chart": {"id": "chart-uae-guests", "title": "Hotel guests in the UAE", "sub": "Millions of guests in hotel establishments, all seven emirates",
                       "label_w": 110, "max": 40,
                       "rows": [("2023", 28.08, "28.08M"), ("2024", 30.75, "30.75M"), ("2025", 32.34, "32.34M"), ("2031 target", 40, "40M")],
                       "highlight": [2],
                       "src": S_MOE + "; " + a(MOE24B, "2024 and 2023 (Arabian Business, citing the Ministry)") + "; target: " + a(STRAT, "UAE Tourism Strategy 2031 (WAM)"),
                       "table": {"caption": "Hotel guests in UAE hotel establishments, Ministry of Economy and Tourism",
                                 "head": ["Year", "Hotel guests", "Change"],
                                 "rows": [["2023", "28,080,000", ""], ["2024", "30,750,000", "+9.5%"], ["2025", "32,340,000", "+5.2%"],
                                          ["2031 target", "40,000,000", "81% reached in 2025"]]}}},
            "<p>Counting <strong>international visitors</strong> only, the World Travel and Tourism Council expected <strong>27.6 million in 2025</strong>, up 4.6% on 2024. The two figures measure different things: a visitor who stays in Dubai and then Abu Dhabi checks in twice, while residents' staycations count as hotel guests but not as international visitors.</p>",
            "<p>To hit 40 million hotel guests by 2031, the UAE needs about 1.3 million more guests every year, slightly below the 1.6 million it added in 2025. On the current pace the target is within reach.</p>",
        ]},
        {"h2": "How much do UAE hotels earn?", "blocks": [
            "<p>UAE hotels earned <strong>AED 49.21 billion in 2025</strong> (about $13.4 billion), up 9.7% from about AED 45 billion in 2024. Revenue grew almost twice as fast as guest numbers, because rates went up as well as volumes.</p>",
            {"chart": {"id": "chart-uae-revenue", "title": "UAE hotel revenue", "sub": "AED billion, all hotel establishments",
                       "label_w": 70,
                       "rows": [("2024", 45.0, "AED 45bn"), ("2025", 49.21, "AED 49.2bn")], "highlight": [1],
                       "src": S_MOE + "; " + S_MOE24,
                       "table": {"caption": "Revenue per guest and per night are computed from the published totals. USD at AED 3.6725",
                                 "head": ["Indicator", "2024", "2025"],
                                 "rows": [["Hotel revenue (AED)", "about 45 billion", "49.21 billion"], ["Hotel revenue (USD)", "about $12.3 billion", "$13.4 billion"],
                                          ["Hotel guests", "30,750,000", "32,340,000"], ["Guest nights", "about 104,460,000", "110,620,000"],
                                          ["Nights per guest", "about 3.4", "3.4"], ["Revenue per guest night", "about AED 431", "AED 445"],
                                          ["Average occupancy", "78%", "79.3%"]]}}},
            "<p>Spread over 110.62 million guest nights, hotels took in about <strong>AED 445 per guest night</strong> (about $121), including food, drink and other hotel revenue, not just the room. The average guest stayed <strong>3.4 nights</strong>.</p>",
        ]},
        {"h2": "How much do tourists spend in the UAE?", "blocks": [
            "<p>International visitors were expected to spend a record <strong>AED 228.5 billion in 2025</strong> (about $62.2 billion), up from AED 217.3 billion in 2024 and 37% above the 2019 level, according to the WTTC. Residents travelling within the country add another <strong>AED 60 billion</strong>.</p>",
            {"chart": {"id": "chart-uae-spend", "title": "Visitor spending in the UAE", "sub": "AED billion; 2025 is a WTTC forecast",
                       "label_w": 90,
                       "legend": [("International visitors", "#1e3a5f"), ("Domestic visitors", "#b7791f")],
                       "rows": [("2024", [217.3, 57.6], "AED 274.9bn"), ("2025 (f)", [228.5, 60.0], "AED 288.5bn")],
                       "src": S_WTTC + "; " + a(WTTC2, "The National, September 2025"),
                       "table": {"caption": "WTTC Economic Impact Research. 2019 levels implied from WTTC's stated growth (+37% international, +47% domestic)",
                                 "head": ["Year", "International (AED bn)", "Domestic (AED bn)", "Total (AED bn)", "International share"],
                                 "rows": [["2019 (implied)", "about 166.8", "about 40.8", "about 207.6", "80%"],
                                          ["2024", "217.3", "57.6", "274.9", "79%"], ["2025 (forecast)", "228.5", "60.0", "288.5", "79%"]]}}},
            "<p>Almost <strong>four dirhams in five</strong> spent on travel in the UAE come from abroad, one of the highest international shares of any country. In most large tourism economies domestic travellers spend more than foreign ones; in the UAE it is the other way round, which makes the sector unusually sensitive to air connections and visa policy.</p>",
        ]},
        {"h2": "How much is tourism worth to the UAE economy?", "toc": "Tourism and the UAE economy", "blocks": [
            "<p>Travel and tourism contributed <strong>AED 257.3 billion</strong> to the UAE economy in 2024 and was forecast at <strong>AED 267.5 billion in 2025</strong>, about <strong>12.9% of GDP</strong>, according to the WTTC. The sector supported <strong>898,600 jobs</strong> in 2024, nearly one job in eight, and more than 925,000 in 2025.</p>",
            {"chart": {"id": "chart-uae-gdp", "title": "Travel and tourism contribution to UAE GDP", "sub": "AED billion, direct, indirect and induced (WTTC)",
                       "label_w": 110, "max": 450,
                       "rows": [("2024", 257.3, "AED 257.3bn"), ("2025 (f)", 267.5, "AED 267.5bn"), ("2031 target", 450, "AED 450bn")],
                       "highlight": [1], "src": S_WTTC + "; target: " + a(STRAT, "UAE Tourism Strategy 2031 (WAM)"),
                       "table": {"caption": "WTTC totals include indirect and induced effects. The 2031 target is the national strategy goal, not a WTTC forecast",
                                 "head": ["Indicator", "2024", "2025 (forecast)"],
                                 "rows": [["Contribution to GDP (AED)", "257.3 billion", "267.5 billion"], ["Share of GDP", "", "12.9%"],
                                          ["Jobs supported", "898,600", "over 925,000"], ["International visitor spending (AED)", "217.3 billion", "228.5 billion"],
                                          ["International visitor spending (USD)", "$59.2 billion", "$62.2 billion"], ["International visitors", "", "27.6 million"]]}}},
            f"<p>The national <strong>UAE Tourism Strategy 2031</strong>, launched in November 2022, aims to raise the sector's contribution to <strong>AED 450 billion</strong>, attract AED 100 billion of new investment and reach 40 million hotel guests. The ministry measures the contribution its own way: it put 2023 at AED 220 billion, 11.7% of GDP ({a(STRAT23, 'Emirates Tourism Council')}), so its figures are lower than WTTC's and the two should not be mixed.</p>",
        ]},
        {"h2": "How do Dubai, Abu Dhabi and the other emirates compare?", "toc": "Dubai vs Abu Dhabi vs other emirates", "blocks": [
            "<p><strong>Dubai</strong> dominates UAE tourism: it has about 154,264 of the country's 217,000 hotel rooms (71%) and received 19.59 million international overnight visitors in 2025. <strong>Abu Dhabi</strong> had more than 34,000 rooms and 5.9 million hotel guests. Sharjah, Ras Al Khaimah, Ajman, Fujairah and Umm Al Quwain share the remaining 29,000 or so rooms.</p>",
            {"chart": {"id": "chart-uae-rooms", "title": "Hotel rooms by emirate", "sub": "Thousands of rooms in hotel establishments",
                       "label_w": 140,
                       "rows": [("Dubai", 154.264, "154.3k"), ("Abu Dhabi", 34.0, "34k+"), ("Other five emirates", 28.7, "≈28.7k")],
                       "highlight": [0],
                       "src": a(DET25, "Dubai DET, end of 2025") + "; " + a(DCT24, "DCT Abu Dhabi, end of 2024") + "; UAE total: " + S_MOE,
                       "table": {"caption": "Other five emirates derived: UAE total (about 217,000) minus Dubai and Abu Dhabi; Abu Dhabi figure is end of 2024",
                                 "head": ["Emirate", "Hotel rooms", "Share", "Main 2025 demand figure"],
                                 "rows": [["Dubai", "154,264", "71%", "19.59 million international overnight visitors"],
                                          ["Abu Dhabi", "34,000+", "16%", "5.9 million hotel guests"],
                                          ["Sharjah, Ras Al Khaimah, Ajman, Fujairah, Umm Al Quwain (derived)", "about 28,700", "13%", ""],
                                          ["UAE total", "about 217,000", "100%", "32.34 million hotel guests"]]}}},
            "<p>Dubai and Abu Dhabi publish different headline numbers: Dubai counts international overnight visitors, Abu Dhabi counts total visitors (26.6 million, including day trips) and hotel guests. Use hotel guests and occupancy to compare them like for like: both ran at about 81% occupancy in 2025 (Dubai 80.7%, Abu Dhabi 81%), well above the national average of 79.3%, which means the smaller emirates' hotels are emptier.</p>",
            "<div class=\"bpa-plan\"><strong>Planning a UAE trip?</strong> Most visitors base themselves in Dubai. Our side-by-side comparisons:<ul>"
            "<li><a href=\"/best-desert-safaris-dubai\">10 best desert safaris in Dubai</a></li>"
            "<li><a href=\"/best-palm-jumeirah-hotels-dubai\">Best hotels on Palm Jumeirah</a></li>"
            "<li><a href=\"/best-burj-khalifa-tickets\">Best Burj Khalifa tickets</a></li>"
            "<li><a href=\"/best-dubai-city-tours\">Best Dubai city tours</a></li>"
            "<li><a href=\"/best-dinner-cruises-dubai\">Best dinner cruises in Dubai</a></li></ul></div>",
        ]},
        {"h2": "Frequently asked questions", "id": "faq", "toc": "FAQ", "blocks": [
            "<p><strong>How many tourists visit the UAE each year?</strong> UAE hotels hosted 32.34 million guests in 2025. Counting international visitors only, WTTC expected 27.6 million in 2025.</p>",
            "<p><strong>How much does tourism contribute to the UAE economy?</strong> About AED 267.5 billion in 2025, 12.9% of GDP, according to WTTC.</p>",
            "<p><strong>Which emirate gets the most tourists?</strong> Dubai, with 19.59 million international overnight visitors in 2025 and about 71% of the UAE's hotel rooms.</p>",
            "<p><strong>How full are UAE hotels?</strong> 79.3% average occupancy in 2025, among the highest of any country.</p>",
            "<p><strong>What is the UAE's tourism target?</strong> 40 million hotel guests and an AED 450 billion contribution to GDP by 2031.</p>",
        ]},
        {"h2": "Sources and methodology", "blocks": [
            "<ul role=\"list\">"
            f"<li><strong>Hotel guests, revenue, guest nights, occupancy and rooms, 2025</strong>: UAE Ministry of Economy and Tourism, results presented to the Emirates Tourism Council on 15 April 2026 ({a(MOE25, 'Gulf News')}).</li>"
            f"<li><strong>2024 and 2023 hotel figures</strong>: Ministry of Economy and Tourism ({a(MOE24, 'WAM, April 2025')}; {a(MOE24B, 'Arabian Business')}).</li>"
            f"<li><strong>Visitor spending, GDP contribution and jobs</strong>: World Travel and Tourism Council, {a(WTTC, 'UAE Economic Impact Research, May 2025')}, and the September 2025 update ({a(WTTC2, 'The National')}). 2025 values are WTTC forecasts and include indirect and induced effects.</li>"
            f"<li><strong>Targets</strong>: {a(STRAT, 'UAE Tourism Strategy 2031')}; ministry estimate of the 2023 contribution from the {a(STRAT23, 'Emirates Tourism Council')}.</li>"
            f"<li><strong>Emirate figures</strong>: {a(DET25, 'Dubai DET')} and {a(DCT24, 'DCT Abu Dhabi')}. The other five emirates' rooms are derived by subtraction. Revenue per guest night, nights per guest and 2024 guest nights are computed from published totals. USD at the fixed rate of AED 3.6725.</li>"
            "<li>Data accessed 19 November 2026.</li></ul>",
        ]},
    ],
}
