"""Dubai tourism statistics. Figures: Dubai Department of Economy and Tourism (DET), official
releases via Dubai Media Office. Accessed 19 November 2026."""


def a(url, text):
    return f'<a href="{url}" rel="noopener" target="_blank">{text}</a>'


DET25 = "https://www.mediaoffice.ae/en/news/2026/february/09-02/dubais-tourism-industry-achieves-third-successive-record-breaking-year"
DET24 = "https://www.mediaoffice.ae/en/news/2025/february/09-02/dubai-welcomes-1872-million-international-visitors-in-2024-and-up-9-percent-year-on-year"
DET23 = "https://www.wam.ae/a/b1jm812"
DET22 = "https://www.mediaoffice.ae/en/news/2023/february/05-02/dubai-receives-14-million-international-visitors-in-2022"
DET_H1 = "https://www.wam.ae/en/article/bl0df77-dubai-welcomes-988-million-international-visitors"
DET_M5 = "https://www.wam.ae/en/article/bkck33b-dubai-welcomes-868-million-international-visitors"
UK9 = "https://gulfnews.com/business/tourism/dubai-welcomed-104m-british-tourists-in-first-nine-months-of-2025-1.500345998"

S25 = a(DET25, "Dubai DET, 2025 tourism performance (Dubai Media Office, 9 Feb 2026)")
S24 = a(DET24, "Dubai DET, 2024 tourism performance")

SPEC = {
    "slug": "dubai-tourism-statistics",
    "short_name": "Dubai Tourism Statistics",
    "title_tag": "Dubai Tourism Statistics 2026: 19.6M Visitors, Hotels & Markets",
    "meta_description": "Dubai welcomed 19.59 million international overnight visitors in 2025. Official data on source markets, hotel occupancy, room rates and seasonality, charted.",
    "headline": "Dubai Tourism Statistics 2026: How Many Tourists Visit Dubai?",
    "breadcrumb": "Dubai Tourism Statistics (2026)",
    "kicker_badge": "Official DET Data · 2025",
    "h1_main": "Dubai Tourism Statistics 2026",
    "h1_muted": "(How Many Tourists Visit?)",
    "author_role": "Compiled from official Dubai DET data",
    "image": "/assets/best-burj-khalifa-tickets/01-sky-148-01.avif",
    "lead": [
        "Dubai welcomed <strong>19.59 million international overnight visitors</strong> in 2025, a third record year in a row and 17% more than before the pandemic. Its <strong>154,264 hotel rooms</strong> were 80.7% full on average, at an average rate of <strong>AED 579</strong> (about $158) a night.",
        "This report covers who visits Dubai, where they come from, when they come, how full the hotels are and what a room costs, all from the Department of Economy and Tourism (DET). For the whole country, see our <a href=\"/uae-tourism-statistics\">UAE tourism statistics</a>, and for the capital, <a href=\"/abu-dhabi-tourism-statistics\">Abu Dhabi tourism statistics</a>. Every chart has a data table and a link to its official source.",
    ],
    "citations": [DET25, DET24, DET23, DET22, DET_H1, DET_M5],
    "sections": [
        {"h2": "Key Dubai tourism statistics (2025)", "toc": "Key Dubai tourism statistics", "blocks": [
            {"tiles": [("19.59M", "international overnight visitors in 2025"), ("+5%", "growth on 2024 (18.72 million)"),
                       ("80.7%", "average hotel occupancy"), ("AED 579", "average daily room rate (about $158)")]},
            "<ul role=\"list\">"
            "<li>Dubai received <strong>19.59 million international overnight visitors</strong> in 2025, up 5% from 18.72 million in 2024 and 17.1% above the 16.73 million of 2019.</li>"
            "<li><strong>Western Europe</strong> is the largest source region with 4.10 million visitors (21%), followed by the <strong>GCC</strong> (2.99 million), <strong>South Asia</strong> and <strong>CIS and Eastern Europe</strong> (2.89 million each).</li>"
            "<li>Hotels sold <strong>44.85 million room nights</strong>, 4% more than in 2024, and guests stayed <strong>3.7 nights</strong> on average.</li>"
            "<li>The average daily rate rose 8% to <strong>AED 579</strong> and revenue per available room rose 11% to <strong>AED 467</strong>.</li>"
            "<li><strong>December 2025</strong> was the busiest month on record: 2.04 million visitors, the first month above 2 million.</li>"
            "<li>The city ended 2025 with <strong>154,264 hotel rooms in 827 establishments</strong>.</li></ul>",
        ]},
        {"h2": "How many tourists visit Dubai each year?", "blocks": [
            "<p>Dubai welcomed <strong>19.59 million international overnight visitors in 2025</strong>, about 870,000 more than in 2024. It was the third record year in a row: 2023 (17.15 million) was the first year above the 2019 peak of 16.73 million.</p>",
            {"chart": {"id": "chart-dxb-visitors", "title": "International overnight visitors to Dubai", "sub": "Millions of visitors per year",
                       "label_w": 70,
                       "rows": [("2019", 16.73, "16.73M"), ("2021", 7.28, "7.28M"), ("2022", 14.36, "14.36M"),
                                ("2023", 17.15, "17.15M"), ("2024", 18.72, "18.72M"), ("2025", 19.59, "19.59M")],
                       "highlight": [5],
                       "src": S25 + "; " + S24 + "; " + a(DET23, "DET 2023 (WAM)") + "; " + a(DET22, "DET 2022 (Dubai Media Office)"),
                       "table": {"caption": "International overnight visitors to Dubai, Department of Economy and Tourism",
                                 "head": ["Year", "Visitors", "Change on previous year shown"],
                                 "rows": [["2019", "16,730,000", ""], ["2021", "7,280,000", ""], ["2022", "14,360,000", "+97% on 2021"],
                                          ["2023", "17,150,000", "+19.4%"], ["2024", "18,720,000", "+9%"], ["2025", "19,590,000", "+5%"]]}}},
            "<p>Growth is slowing as the base gets bigger: +19.4% in 2023, +9% in 2024 and +5% in 2025. In absolute terms Dubai still adds close to a million visitors a year, roughly the population of a mid-sized European city arriving on top of last year's total.</p>",
            "<p>DET counts <strong>international overnight visitors</strong>: people from abroad who stay at least one night in a hotel or hotel apartment. Day trippers, transit passengers who never leave DXB and UAE residents visiting from other emirates are not included, which is why Dubai's figure is not directly comparable with Abu Dhabi's broader \"visitors\" total.</p>",
        ]},
        {"h2": "Where do Dubai's tourists come from?", "blocks": [
            "<p><strong>Western Europe</strong> sent 4.10 million visitors in 2025 (21% of the total), up from 3.74 million in 2024. The Gulf states (<strong>GCC</strong>, 2.99 million), <strong>South Asia</strong> and <strong>CIS and Eastern Europe</strong> (2.89 million each) each supply about 15%.</p>",
            {"chart": {"id": "chart-dxb-regions", "title": "Dubai visitors by source region, 2025", "sub": "Millions of international overnight visitors",
                       "label_w": 150,
                       "short": {"North East and South East Asia": "NE & SE Asia", "CIS and Eastern Europe": "CIS & E. Europe"},
                       "rows": [("Western Europe", 4.10, "4.10M"), ("GCC", 2.99, "2.99M"), ("CIS and Eastern Europe", 2.89, "2.89M"),
                                ("South Asia", 2.89, "2.89M"), ("MENA", 2.17, "2.17M"), ("North East and South East Asia", 1.85, "1.85M"),
                                ("Americas", 1.40, "1.40M"), ("Africa", 0.897, "0.90M"), ("Australasia", 0.401, "0.40M")],
                       "highlight": [0], "src": S25,
                       "table": {"caption": "International overnight visitors to Dubai by source region, 2025 (share computed from the regional totals)",
                                 "head": ["Region", "Visitors", "Share"],
                                 "rows": [["Western Europe", "4,100,000", "20.9%"], ["GCC", "2,990,000", "15.3%"],
                                          ["CIS and Eastern Europe", "2,890,000", "14.8%"], ["South Asia", "2,890,000", "14.8%"],
                                          ["MENA (excluding GCC)", "2,170,000", "11.1%"], ["North East and South East Asia", "1,850,000", "9.4%"],
                                          ["Americas", "1,400,000", "7.1%"], ["Africa", "897,000", "4.6%"], ["Australasia", "401,000", "2.0%"],
                                          ["Total", "19,588,000", "100%"]]}}},
            "<p>No single region dominates: the top four together account for two thirds of all visitors. Neighbouring Gulf and wider Middle East markets (GCC plus MENA) add up to 26%, more than Western Europe on its own.</p>",
            f"<p>By country, DET's headline releases do not publish a full-year 2025 ranking. India and the United Kingdom are consistently named as the two largest single markets; the UK alone sent about <strong>1.04 million visitors</strong> in the first nine months of 2025, 120,000 more than a year earlier ({a(UK9, 'Gulf News, citing DET')}).</p>",
        ]},
        {"h2": "When is Dubai busiest?", "blocks": [
            "<p>Dubai's high season runs from <strong>November to March</strong>, when daytime temperatures are in the mid-20s °C. <strong>December 2025 set the all-time monthly record</strong> with 2.04 million visitors, beating January 2025 (1.94 million). Summer is far quieter: June 2025 had about 1.2 million visitors.</p>",
            {"chart": {"id": "chart-dxb-season", "title": "Dubai visitors in selected months of 2025", "sub": "Millions of international overnight visitors",
                       "label_w": 100,
                       "rows": [("January", 1.94, "1.94M"), ("June", 1.20, "1.20M"), ("December", 2.04, "2.04M")],
                       "highlight": [2],
                       "src": S25 + "; " + a(DET_M5, "DET, January to May 2025") + "; " + a(DET_H1, "DET, first half of 2025"),
                       "table": {"caption": "June is derived: 9.88 million (January to June) minus 8.68 million (January to May)",
                                 "head": ["Period", "Visitors"],
                                 "rows": [["January 2025", "1,940,000"], ["January to May 2025", "8,680,000"],
                                          ["June 2025 (derived)", "1,200,000"], ["January to June 2025", "9,880,000"],
                                          ["July to December 2025 (derived)", "9,710,000"], ["December 2025", "2,040,000"],
                                          ["Full year 2025", "19,590,000"]]}}},
            "<p>December drew <strong>70% more visitors than June</strong>. That gap is the best argument for a shoulder-season trip: in late October, early November or April the weather is still good for the beach and the desert, and hotels are easier to book than over Christmas and New Year.</p>",
            "<p>Outdoor experiences follow the same calendar. Desert evenings, hot air balloon flights and open-deck dhow cruises are at their best (and busiest) between November and March, so that is when our <a href=\"/best-desert-safaris-dubai\">desert safari comparison</a>, <a href=\"/best-hot-air-balloon-dubai\">hot air balloon guide</a> and <a href=\"/best-dinner-cruises-dubai\">Dubai dinner cruise ranking</a> are worth reading early.</p>",
        ]},
        {"h2": "How full are Dubai's hotels?", "blocks": [
            "<p>Dubai's hotels were <strong>80.7% occupied</strong> on average in 2025, up from 78.2% in 2024 and 77.4% in 2023, even though the number of rooms kept growing. Hotels sold <strong>44.85 million room nights</strong> in 2025.</p>",
            {"chart": {"id": "chart-dxb-occupancy", "title": "Average hotel occupancy in Dubai", "sub": "Share of available rooms sold over the year",
                       "label_w": 70, "max": 100,
                       "rows": [("2023", 77.4, "77.4%"), ("2024", 78.2, "78.2%"), ("2025", 80.7, "80.7%")], "highlight": [2],
                       "src": S25 + "; " + S24,
                       "table": {"caption": "Dubai hotel supply and demand, end of year",
                                 "head": ["Year", "Rooms", "Establishments", "Occupancy", "Occupied room nights"],
                                 "rows": [["2023", "150,291", "821", "77.4%", "41,700,000"], ["2024", "154,016", "832", "78.2%", "43,030,000"],
                                          ["2025", "154,264", "827", "80.7%", "44,850,000"]]}}},
            "<p>Room supply barely moved in 2025 (+248 rooms) while demand rose 4%, which is why occupancy jumped 2.5 points. Dubai now has more hotel rooms than New York, Paris or Singapore and almost as many as London, and an occupancy above 80% across that stock is unusually high for a city of its size.</p>",
            "<p>Visitors stayed <strong>3.7 nights</strong> on average in 2025, the same as in 2024. That is short enough that most trips are city-break length, which is why the first-timer staples (the <a href=\"/best-burj-khalifa-tickets\">Burj Khalifa observation decks</a>, a <a href=\"/best-dubai-city-tours\">city tour</a> and one desert evening) sell out first.</p>",
        ]},
        {"h2": "How much does a hotel room in Dubai cost?", "blocks": [
            "<p>The <strong>average daily rate (ADR) was AED 579</strong> in 2025 (about $158 at the fixed rate of 3.6725 dirhams per dollar), up 8% from AED 538 in 2024. <strong>Revenue per available room (RevPAR) rose 11% to AED 467</strong>, the fastest growth of any headline hotel figure.</p>",
            {"chart": {"id": "chart-dxb-rates", "title": "Dubai hotel ADR and RevPAR", "sub": "Average for all hotel establishments, AED",
                       "label_w": 110,
                       "rows": [("ADR 2023", 536, "AED 536"), ("ADR 2024", 538, "AED 538"), ("ADR 2025", 579, "AED 579"),
                                ("RevPAR 2023", 415, "AED 415"), ("RevPAR 2024", 421, "AED 421"), ("RevPAR 2025", 467, "AED 467")],
                       "highlight": [2, 5], "src": S25 + "; " + S24,
                       "table": {"caption": "ADR = room revenue per occupied room night; RevPAR = room revenue per available room night. USD at AED 3.6725",
                                 "head": ["Year", "ADR (AED)", "ADR (USD)", "RevPAR (AED)", "RevPAR (USD)"],
                                 "rows": [["2023", "536", "$146", "415", "$113"], ["2024", "538", "$146", "421", "$115"],
                                          ["2025", "579", "$158", "467", "$127"]]}}},
            "<p>Rates were almost flat in 2024 (+AED 2) and then jumped AED 41 in 2025, when hotels could raise prices because they were fuller. The averages hide a wide range: they include budget hotels and hotel apartments as well as the Palm Jumeirah resorts, where peak-season nights cost several times the city average (see our <a href=\"/best-palm-jumeirah-hotels-dubai\">Palm Jumeirah hotel comparison</a>).</p>",
        ]},
        {"h2": "How does Dubai compare with Abu Dhabi and the UAE?", "toc": "Dubai vs Abu Dhabi and the UAE", "blocks": [
            "<p>Dubai holds about <strong>seven in ten UAE hotel rooms</strong> (154,264 of roughly 217,000) and dominates international arrivals. Abu Dhabi, the capital, had 5.9 million hotel guests in 2025 and 81% occupancy, with stronger growth in rates (ADR +19%) than Dubai. The full comparison is on our <a href=\"/uae-tourism-statistics\">UAE tourism statistics</a> page; the capital's own figures are on <a href=\"/abu-dhabi-tourism-statistics\">Abu Dhabi tourism statistics</a>.</p>",
            "<p>Dubai International Airport (DXB) handled <strong>92.3 million passengers in 2024</strong> and has been the world's busiest airport for international passengers for 11 years in a row, according to Airports Council International. Many of those passengers are in transit, which is one reason DET counts overnight hotel guests rather than arrivals.</p>",
            "<div class=\"bpa-plan\"><strong>Planning a Dubai trip?</strong> Our side-by-side comparisons of the city's most booked experiences:<ul>"
            "<li><a href=\"/best-desert-safaris-dubai\">10 best desert safaris in Dubai</a></li>"
            "<li><a href=\"/best-burj-khalifa-tickets\">Best Burj Khalifa tickets</a></li>"
            "<li><a href=\"/best-palm-jumeirah-hotels-dubai\">Best hotels on Palm Jumeirah</a></li>"
            "<li><a href=\"/best-dinner-cruises-dubai\">Best dinner cruises in Dubai</a></li>"
            "<li><a href=\"/best-helicopter-tours-dubai\">Best helicopter tours in Dubai</a></li>"
            "<li><a href=\"/best-water-parks-dubai\">Best water parks in Dubai</a></li></ul></div>",
        ]},
        {"h2": "Frequently asked questions", "id": "faq", "toc": "FAQ", "blocks": [
            "<p><strong>How many tourists visited Dubai in 2025?</strong> 19.59 million international overnight visitors, according to Dubai's Department of Economy and Tourism, up 5% on 2024.</p>",
            "<p><strong>Which country sends the most tourists to Dubai?</strong> By region, Western Europe (4.10 million in 2025). By single country, India and the United Kingdom are the largest markets; DET has not published a full-year 2025 country ranking.</p>",
            "<p><strong>What is the busiest month in Dubai?</strong> December. December 2025 was the first month with more than 2 million visitors (2.04 million).</p>",
            "<p><strong>How long do tourists stay in Dubai?</strong> 3.7 nights on average in hotels in 2025.</p>",
            "<p><strong>How many hotel rooms does Dubai have?</strong> 154,264 rooms in 827 hotels and hotel apartment buildings at the end of 2025.</p>",
        ]},
        {"h2": "Sources and methodology", "blocks": [
            "<ul role=\"list\">"
            f"<li><strong>2025 visitors, regions and hotel performance</strong>: Dubai Department of Economy and Tourism (DET), {a(DET25, 'Dubai’s tourism industry achieves third successive record-breaking year')}, Dubai Media Office, 9 February 2026.</li>"
            f"<li><strong>2024 and 2023 hotel figures</strong>: DET, {a(DET24, 'Dubai welcomes 18.72 million international visitors in 2024')}, Dubai Media Office, 9 February 2025.</li>"
            f"<li><strong>Earlier years</strong>: DET 2023 release ({a(DET23, 'WAM, February 2024')}) for 2023 and 2019, and the {a(DET22, '2022 release')} for 2022 and 2021.</li>"
            f"<li><strong>Monthly figures</strong>: DET releases for {a(DET_M5, 'January to May 2025')} and {a(DET_H1, 'the first half of 2025')}; June and the second half are derived by subtraction.</li>"
            "<li><strong>Definitions</strong>: visitors are international overnight visitors staying in hotel establishments (hotels and hotel apartments). Occupancy, ADR and RevPAR are averages for all hotel establishments in Dubai. Shares by region are computed from the regional totals and may differ by a fraction of a point from DET's rounded percentages. US dollar values use the fixed rate of AED 3.6725.</li>"
            "<li>Data accessed 19 November 2026. DET may revise figures in its annual visitor report.</li></ul>",
        ]},
    ],
}
