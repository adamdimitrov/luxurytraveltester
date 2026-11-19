"""Abu Dhabi tourism statistics. Figures: Department of Culture and Tourism Abu Dhabi (DCT),
Sheikh Zayed Grand Mosque Centre, via Abu Dhabi Media Office / WAM. Accessed 19 November 2026."""


def a(url, text):
    return f'<a href="{url}" rel="noopener" target="_blank">{text}</a>'


DCT25 = "https://www.mediaoffice.abudhabi/en/tourism/abu-dhabis-culture-and-tourism-sectors-delivered-strong-growth-in-2025-with-26m-visitors/"
DCT24 = "https://dct.gov.ae/DataFolder/reports/hotel-establishment/2019/2024%20Hotel%20Performance%20Report.pdf"
DCT24N = "https://en.aletihad.ae/news/business/4579524/abu-dhabi-hotel-sector-booms-with-5-8-million-guests-in-2024"
DCT23 = "https://dct.gov.ae/Pages/AnnualReport2024.aspx"
TARGET = "https://thenationalnews.com/business/aviation/2024/12/24/abu-dhabi-tourism-jobs"
SZGM = "https://gulfnews.com/uae/sheikh-zayed-grand-mosque-welcomes-nearly-7-million-guests-in-2025-2-1.500426996"

S25 = a(DCT25, "DCT Abu Dhabi, 2025 performance (Abu Dhabi Media Office, April 2026)")
S24 = a(DCT24, "DCT Abu Dhabi, 2024 Hotel Performance Report")

SPEC = {
    "slug": "abu-dhabi-tourism-statistics",
    "short_name": "Abu Dhabi Tourism Statistics",
    "title_tag": "Abu Dhabi Tourism Statistics 2026: 26.6M Visitors & Hotel Data",
    "meta_description": "Abu Dhabi had 26.6 million visitors and 5.9 million hotel guests in 2025. Official DCT data on source markets, occupancy, hotel revenue and top attractions.",
    "headline": "Abu Dhabi Tourism Statistics 2026: Visitors, Hotels and Top Attractions",
    "breadcrumb": "Abu Dhabi Tourism Statistics (2026)",
    "kicker_badge": "Official DCT Data · 2025",
    "h1_main": "Abu Dhabi Tourism Statistics 2026",
    "h1_muted": "(Visitors, Hotels & Attractions)",
    "author_role": "Compiled from official DCT Abu Dhabi data",
    "image": "/assets/icons/icon-512.png",
    "lead": [
        "Abu Dhabi recorded <strong>26.6 million visitors</strong> in 2025 and its hotels welcomed <strong>5.9 million guests</strong>, filling 81% of rooms. Hotel revenue grew far faster than guest numbers: <strong>AED 9.1 billion, up 19.5%</strong>, because the average room rate rose 19%.",
        "This report covers how many people visit the UAE capital, which countries they come from, how long they stay, how the three regions compare and which attractions draw the crowds, all from the Department of Culture and Tourism (DCT). For the neighbouring emirate, see our <a href=\"/dubai-tourism-statistics\">Dubai tourism statistics</a>; for the national picture, <a href=\"/uae-tourism-statistics\">UAE tourism statistics</a>.",
    ],
    "citations": [DCT25, DCT24, DCT24N, DCT23, TARGET, SZGM],
    "sections": [
        {"h2": "Key Abu Dhabi tourism statistics (2025)", "toc": "Key Abu Dhabi tourism statistics", "blocks": [
            {"tiles": [("26.6M", "visitors to Abu Dhabi in 2025"), ("5.9M", "hotel guests (+2.2%)"),
                       ("81%", "average hotel occupancy"), ("AED 9.1bn", "hotel revenue (+19.5%)")]},
            "<ul role=\"list\">"
            "<li>Abu Dhabi recorded <strong>26.6 million visitors</strong> in 2025, a record, up from 24 million in 2023.</li>"
            "<li>Hotels welcomed <strong>5.9 million guests</strong> (+2.2%), and holiday homes and glamping sites another 338,000. International guests grew 10%.</li>"
            "<li><strong>India</strong> is the largest market with 436,124 hotel guests (13% of the total, +22%), ahead of Russia, the UK, China and Saudi Arabia.</li>"
            "<li>Occupancy reached <strong>81%</strong>, the average daily rate rose <strong>19%</strong> and revenue per available room <strong>23%</strong>.</li>"
            "<li>Guests stayed <strong>2.9 nights</strong> on average; visitors from Russia (4.3 nights), the UK (4.2) and Germany (4.1) stay longest.</li>"
            "<li>The <strong>Sheikh Zayed Grand Mosque</strong> received 6.85 million guests and Louvre Abu Dhabi 1.4 million visitors.</li></ul>",
        ]},
        {"h2": "How many tourists visit Abu Dhabi each year?", "blocks": [
            "<p>Abu Dhabi recorded <strong>26.6 million visitors in 2025</strong>, up from 24 million in 2023, about 11% more in two years. The emirate's target is <strong>39.3 million visitors a year by 2030</strong> under the Abu Dhabi Tourism Strategy 2030.</p>",
            "<p>The visitor total is a broad measure: it includes day visitors from Dubai and the other emirates, who make up a large share because the two cities are 90 minutes apart by road. The tighter measure is <strong>hotel guests</strong>, which grew from 5.50 million in 2023 to 5.82 million in 2024 and 5.9 million in 2025.</p>",
            {"chart": {"id": "chart-auh-guests", "title": "Hotel guests in Abu Dhabi", "sub": "Millions of guests in hotel establishments per year",
                       "label_w": 70,
                       "rows": [("2023", 5.504, "5.50M"), ("2024", 5.819, "5.82M"), ("2025", 5.9, "5.9M")], "highlight": [2],
                       "src": S25 + "; " + S24,
                       "table": {"caption": "Abu Dhabi hotel guests and occupancy. 2025 occupancy as published by DCT in April 2026",
                                 "head": ["Year", "Hotel guests", "Change", "Occupancy"],
                                 "rows": [["2023", "5,504,000", "", ""], ["2024", "5,819,000", "+5.7%", "79%"],
                                          ["2025", "5,900,000", "+2.2%", "81%"]]}}},
            "<p>Guest numbers grew only 2.2% in 2025, but the guest mix shifted abroad: <strong>international guests rose 10%</strong> while domestic stays (UAE residents on staycations) fell back. International guests spend more per night, which is why revenue grew nine times faster than guest numbers. In 2024, 3 million of the 5.8 million hotel guests came from abroad.</p>",
        ]},
        {"h2": "Where do Abu Dhabi's tourists come from?", "blocks": [
            "<p><strong>India</strong> sent 436,124 hotel guests to Abu Dhabi in 2025, 22% more than in 2024 and 13% of all hotel guests. <strong>Russia</strong> (257,200), the <strong>United Kingdom</strong> (250,906), <strong>China</strong> (248,494) and <strong>Saudi Arabia</strong> (200,652) complete the top five.</p>",
            {"chart": {"id": "chart-auh-markets", "title": "Top source markets for Abu Dhabi hotels, 2025", "sub": "Hotel guests by nationality",
                       "label_w": 120,
                       "rows": [("India", 436124, "436,124"), ("Russia", 257200, "257,200"), ("United Kingdom", 250906, "250,906"),
                                ("China", 248494, "248,494"), ("Saudi Arabia", 200652, "200,652")], "highlight": [0],
                       "src": S25,
                       "table": {"caption": "Hotel guests in Abu Dhabi by top source market, 2025",
                                 "head": ["Market", "Hotel guests", "Average stay"],
                                 "rows": [["India", "436,124", ""], ["Russia", "257,200", "4.3 nights"], ["United Kingdom", "250,906", "4.2 nights"],
                                          ["China", "248,494", ""], ["Saudi Arabia", "200,652", ""], ["Germany", "", "4.1 nights"],
                                          ["Italy", "", "3.4 nights"]]}}},
            "<p>India is far ahead: it sends 70% more hotel guests than the next market. Behind it, Russia, the UK and China are almost level at about 250,000 guests each. Chinese guests also stayed 13% longer than a year earlier, the fastest increase of any key market.</p>",
        ]},
        {"h2": "How long do visitors stay in Abu Dhabi?", "blocks": [
            "<p>Guests stayed <strong>2.9 nights</strong> on average across all accommodation in 2025, 3% longer than in 2024 and almost a night shorter than in Dubai (3.7 nights). Long-haul European markets stay the longest.</p>",
            {"chart": {"id": "chart-auh-stay", "title": "Average length of stay in Abu Dhabi by market, 2025", "sub": "Nights per guest",
                       "label_w": 120,
                       "rows": [("Russia", 4.3, "4.3"), ("United Kingdom", 4.2, "4.2"), ("Germany", 4.1, "4.1"),
                                ("Italy", 3.4, "3.4"), ("All guests", 2.9, "2.9")], "highlight": [4],
                       "src": S25,
                       "table": {"caption": "Average length of stay, nights. All guests = all accommodation types",
                                 "head": ["Market", "Nights"],
                                 "rows": [["Russia", "4.3"], ["United Kingdom", "4.2"], ["Germany", "4.1"], ["Italy", "3.4"], ["All guests", "2.9"]]}}},
            "<p>The short average reflects how many guests combine Abu Dhabi with Dubai: two or three nights for the Grand Mosque, Louvre and Yas Island theme parks, then the rest of the trip in Dubai. If you are splitting a trip that way, our <a href=\"/dubai-tourism-statistics\">Dubai statistics</a> show when each city is busiest.</p>",
        ]},
        {"h2": "How are Abu Dhabi's hotels performing?", "blocks": [
            "<p>Hotel revenue reached <strong>AED 9.1 billion in 2025, up 19.5%</strong>. Occupancy averaged <strong>81%</strong>, the average daily rate rose <strong>19%</strong> and revenue per available room <strong>23%</strong>, while airlines added 11% more inbound seats and flew them 89% full.</p>",
            {"chart": {"id": "chart-auh-growth", "title": "Abu Dhabi hotel growth in 2025", "sub": "Change on 2024, %",
                       "label_w": 150,
                       "rows": [("RevPAR", 23, "+23%"), ("Hotel revenue", 19.5, "+19.5%"), ("Average daily rate", 19, "+19%"),
                                ("Inbound air seats", 11, "+11%"), ("International guests", 10, "+10%"), ("Hotel guests", 2.2, "+2.2%")],
                       "highlight": [0], "src": S25,
                       "table": {"caption": "Year-on-year change, 2025 vs 2024. 2024 revenue is derived from the published growth rate",
                                 "head": ["Indicator", "2025", "Change"],
                                 "rows": [["Hotel revenue", "AED 9.1 billion", "+19.5% (2024: about AED 7.6 billion)"],
                                          ["Occupancy", "81%", "2024: 79%"], ["Average daily rate", "", "+19%"], ["RevPAR", "", "+23%"],
                                          ["Hotel guests", "5.9 million", "+2.2%"], ["International guests", "", "+10%"],
                                          ["Inbound seat capacity", "", "+11%"], ["Load factor", "89%", "+2 points"]]}}},
            "<p>The story of 2025 is price, not volume: guest numbers grew 2.2%, but each room earned almost a quarter more. At the end of 2024 the emirate had <strong>171 hotel establishments with more than 34,000 rooms</strong>, about a fifth of Dubai's room count, which keeps occupancy high when big events (Formula 1, concerts, exhibitions) fill the city.</p>",
        ]},
        {"h2": "Which parts of Abu Dhabi get the most visitors?", "toc": "Abu Dhabi city, Al Ain and Al Dhafra", "blocks": [
            "<p>The emirate has three regions. The <strong>Abu Dhabi region</strong> (the city, Yas and Saadiyat islands) takes about nine in ten hotel guests. <strong>Al Ain</strong>, the garden city on the Omani border, had 473,100 guests (+9%), and <strong>Al Dhafra</strong>, the desert region with Liwa and the Empty Quarter, 147,900 (+3%).</p>",
            {"chart": {"id": "chart-auh-regions", "title": "Hotel guests by region of Abu Dhabi, 2025", "sub": "Millions of guests",
                       "label_w": 140,
                       "rows": [("Abu Dhabi region", 5.279, "≈5.28M"), ("Al Ain", 0.4731, "0.47M"), ("Al Dhafra", 0.1479, "0.15M")],
                       "highlight": [0], "src": S25,
                       "table": {"caption": "Abu Dhabi region is derived: emirate total (5.9 million) minus Al Ain and Al Dhafra",
                                 "head": ["Region", "Hotel guests", "Change", "Occupancy change"],
                                 "rows": [["Abu Dhabi region (derived)", "about 5,279,000", "", ""], ["Al Ain", "473,100", "+9%", "+9%"],
                                          ["Al Dhafra", "147,900", "+3%", "+19%"]]}}},
            "<p>Al Dhafra is small but growing in value: its hotel occupancy rose 19% in 2025, helped by desert events such as the Liwa festival village, which drew more than 159,000 visitors.</p>",
        ]},
        {"h2": "What are the most visited attractions in Abu Dhabi?", "toc": "Most visited attractions", "blocks": [
            "<p>The <strong>Sheikh Zayed Grand Mosque</strong> is by far the most visited landmark: 6,846,723 guests in 2025, its highest total on record and 4% more than in 2024. That figure includes 4,331,046 visitors, 1,531,192 worshippers and 898,767 iftar guests during Ramadan. Cultural sites and libraries across the emirate recorded more than 8.6 million visits.</p>",
            {"chart": {"id": "chart-auh-attractions", "title": "Visits to major Abu Dhabi cultural sites, 2025", "sub": "Millions of visits",
                       "label_w": 170, "short": {"Sheikh Zayed Grand Mosque (visitors)": "Grand Mosque (visitors)"},
                       "rows": [("Sheikh Zayed Grand Mosque (visitors)", 4.331, "4.33M"), ("Louvre Abu Dhabi", 1.4, "1.4M"),
                                ("Qasr Al Hosn", 0.843, "0.84M")],
                       "highlight": [0], "src": a(SZGM, "Sheikh Zayed Grand Mosque Centre (via Gulf News, Jan 2026)") + "; " + S25,
                       "table": {"caption": "Grand Mosque: tourist visitors only, excluding worshippers, iftar guests and promenade users",
                                 "head": ["Site", "Visits 2025", "Note"],
                                 "rows": [["Sheikh Zayed Grand Mosque, all guests", "6,846,723", "+4% on 2024"],
                                          ["of which visitors", "4,331,046", ""], ["of which worshippers", "1,531,192", ""],
                                          ["of which iftar guests", "898,767", ""], ["of which promenade users", "85,718", ""],
                                          ["Louvre Abu Dhabi", "1,400,000", ""], ["Qasr Al Hosn", "843,000", "+22%"]]}}},
            "<p>82% of the mosque's guests came from outside the UAE. By nationality, <strong>India (20%)</strong>, <strong>China (9%)</strong>, <strong>Russia (8%)</strong> and the <strong>United States (8%)</strong> lead, followed by Germany, the UK, France and Italy at 3% each.</p>",
            {"chart": {"id": "chart-auh-mosque", "title": "Sheikh Zayed Grand Mosque visitors by nationality, 2025", "sub": "Share of visitors, %",
                       "label_w": 120,
                       "rows": [("India", 20, "20%"), ("China", 9, "9%"), ("Russia", 8, "8%"), ("United States", 8, "8%"),
                                ("Germany", 3, "3%"), ("United Kingdom", 3, "3%"), ("France", 3, "3%"), ("Italy", 3, "3%"),
                                ("Philippines", 2, "2%"), ("Pakistan", 2, "2%")],
                       "highlight": [0], "src": a(SZGM, "Sheikh Zayed Grand Mosque Centre (via Gulf News, Jan 2026)"),
                       "table": {"caption": "Top 10 nationalities among Sheikh Zayed Grand Mosque visitors, 2025",
                                 "head": ["Nationality", "Share"],
                                 "rows": [["India", "20%"], ["China", "9%"], ["Russia", "8%"], ["United States", "8%"], ["Germany", "3%"],
                                          ["United Kingdom", "3%"], ["France", "3%"], ["Italy", "3%"], ["Philippines", "2%"], ["Pakistan", "2%"]]}}},
            "<p>Events are the other big draw: 252 culture and leisure events attracted 4.2 million attendees (+20%), and 6,600 business events (MICE) brought 2.2 million delegates (+40%). Coldplay's four concerts alone drew 193,470 people.</p>",
            "<div class=\"bpa-plan\"><strong>Visiting from Dubai?</strong> Most Abu Dhabi day trips start in Dubai. Our Dubai comparisons help plan the rest of the trip:<ul>"
            "<li><a href=\"/best-dubai-city-tours\">Best Dubai city tours</a></li>"
            "<li><a href=\"/best-desert-safaris-dubai\">Best desert safaris in Dubai</a></li>"
            "<li><a href=\"/best-palm-jumeirah-hotels-dubai\">Best hotels on Palm Jumeirah</a></li>"
            "<li><a href=\"/best-water-parks-dubai\">Best water parks in Dubai</a></li></ul></div>",
        ]},
        {"h2": "Frequently asked questions", "id": "faq", "toc": "FAQ", "blocks": [
            "<p><strong>How many tourists visited Abu Dhabi in 2025?</strong> 26.6 million visitors, including 5.9 million hotel guests, according to the Department of Culture and Tourism Abu Dhabi.</p>",
            "<p><strong>Which country sends the most tourists to Abu Dhabi?</strong> India, with 436,124 hotel guests in 2025 (13% of the total), followed by Russia, the UK, China and Saudi Arabia.</p>",
            "<p><strong>What is the most visited attraction in Abu Dhabi?</strong> The Sheikh Zayed Grand Mosque, with 6.85 million guests in 2025 (4.33 million of them tourist visitors).</p>",
            "<p><strong>How full are Abu Dhabi's hotels?</strong> 81% average occupancy in 2025, up from 79% in 2024.</p>",
            "<p><strong>How many visitors does Abu Dhabi want to attract?</strong> 39.3 million a year by 2030.</p>",
        ]},
        {"h2": "Sources and methodology", "blocks": [
            "<ul role=\"list\">"
            f"<li><strong>2025 visitors, hotel guests, revenue, markets, regions, events and cultural sites</strong>: Department of Culture and Tourism Abu Dhabi (DCT), {a(DCT25, 'Abu Dhabi’s culture and tourism sectors delivered strong growth in 2025')}, Abu Dhabi Media Office, April 2026.</li>"
            f"<li><strong>2024 and 2023 hotel guests, 2024 occupancy and supply</strong>: DCT, {a(DCT24, '2024 Hotel Performance Report')} (summary in {a(DCT24N, 'Aletihad')}).</li>"
            f"<li><strong>2023 visitors and 2030 target</strong>: DCT annual reporting, as cited by {a(TARGET, 'The National, December 2024')}.</li>"
            f"<li><strong>Sheikh Zayed Grand Mosque</strong>: Sheikh Zayed Grand Mosque Centre, 2025 annual figures ({a(SZGM, 'Gulf News / WAM, 31 January 2026')}).</li>"
            "<li><strong>Definitions</strong>: \"visitors\" is DCT's total visitor count, which includes day visitors; \"hotel guests\" counts guests checking in to hotel establishments, so one person on two separate trips is counted twice. The Abu Dhabi region figure and 2024 revenue are derived from published totals and growth rates. The 2025 occupancy increase is described by DCT as 3 points; the 2024 report published 79%.</li>"
            "<li>Data accessed 19 November 2026.</li></ul>",
        ]},
    ],
}
