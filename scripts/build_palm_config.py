import json

config = {
  "brand": {
    "name": "LUXURY TRAVEL TESTER",
    "code": "ltt",
    "domain": "https://www.luxurytraveltester.com",
    "logo_url": "https://www.luxurytraveltester.com/favicon.png",
    "footer_tagline": "LuxuryTravelTester.com is your independent, field-tested guide to choosing the world's most iconic travel experiences and luxury hotels.",
    "copyright": "© 2026 LuxuryTravelTester.com. All rights reserved.",
    "nav_links": [
      {"label": "Dubai Desert Safaris", "href": "/best-desert-safaris-dubai"},
      {"label": "Dubai Palm Hotels", "href": "/best-palm-jumeirah-hotels-dubai", "active": True},
      {"label": "NYC Helicopter Tours", "href": "/best-helicopter-tours-new-york"},
      {"label": "About", "href": "/about"},
      {"label": "Contact", "href": "/contact"}
    ],
    "footer_popular": [
      {"label": "Top 10 Dubai Palm Jumeirah Hotels", "href": "/best-palm-jumeirah-hotels-dubai", "current": True},
      {"label": "10 Best Desert Safaris in Dubai", "href": "/best-desert-safaris-dubai"},
      {"label": "Best NYC Helicopter Tours", "href": "/best-helicopter-tours-new-york"},
      {"label": "Atlantis The Royal Dubai Review", "href": "/best-palm-jumeirah-hotels-dubai/atlantis-the-royal-dubai-review"},
      {"label": "Atlantis The Palm Dubai Review", "href": "/best-palm-jumeirah-hotels-dubai/atlantis-the-palm-dubai-review"}
    ]
  },
  "deck": {
    "id": "dubai-palm-deck",
    "eyebrow": "2026 Comparison Engine • Personally Tested",
    "title": "Comparison Guide — 10 Best Hotels on Palm Jumeirah Dubai",
    "description": "Avoid booking the wrong Palm vibe. Compare beach quality, pool scenes, waterpark perks, dining collections, and real nightly rates side-by-side.",
    "toc_deck_label": "Top 10 Hotels Comparison",
    "toc_breakdown_label": "Detailed Breakdown (10 Hotels)",
    "breakdown_title": "Detailed Breakdown — 10 Best Hotels on Palm Jumeirah Dubai",
    "breakdown_sub": "Personally field-tested undercover • All reviews open by default • Click to collapse/expand",
    "sticky_toc_btn_label": "All 10 Palm Hotels",
    "sheet_title": "Jump to Tested Palm Jumeirah Hotel",
    "tabs": [
      {"cat": "all", "label": "All Hotels (10)", "active": True},
      {"cat": "overall", "label": "🏆 Top Rated (4)"},
      {"cat": "luxury", "label": "👑 Ultra-Luxury (5)"},
      {"cat": "families", "label": "👨‍👩‍👧‍👦 Families & Kids (3)"},
      {"cat": "nightlife", "label": "🍸 Parties & Nightlife (2)"},
      {"cat": "peaceful", "label": "🌿 Peaceful & Wellness (4)"}
    ]
  },
  "intro": {
    "breadcrumbs": [
      {"label": "Home", "href": "/"},
      {"label": "Dubai Palm Hotels", "href": "/best-palm-jumeirah-hotels-dubai"},
      {"label": "10 Best Hotels in Palm Jumeirah Dubai in 2026 (Personally Tested)"}
    ],
    "h1_main": "10 Best Hotels in Palm Jumeirah Dubai in 2026",
    "h1_highlight": "(Personally Tested)",
    "author_name": "Adam Dimitrov",
    "author_url": "/about",
    "author_title": "Founder & Lead Field Inspector",
    "author_avatar": "https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/67d02edca7795b0f57073f59_Adam-dimitrov-portrait-500x500.webp",
    "author_subline": "5 Flagship Resorts Personally Tested • 150+ Original Photos • 100% Anonymous & Self-Funded",
    "last_updated": "today",
    "paragraphs": [
      "Staying on the Palm Jumeirah is a dream for many travelers visiting Dubai. But choosing the wrong hotel here can turn a luxury vacation into an exercise in frustration: some resorts are high-energy party scenes with pounding bass, while others are peaceful family sanctuaries or ultra-exclusive private enclaves with strict dress codes.",
      "To help you avoid costly booking mistakes, I personally booked and stayed undercover at the Palm's top flagship resorts. I evaluated private beach water clarity, pool overcrowding, restaurant culinary standards, room acoustics, and concierge service to deliver this definitive, honest comparison."
    ]
  },
  "items": [
    {
      "id": "1-atlantis-the-palm",
      "source_container_index": 0,
      "rank_tag": "🏆 #1 Best All-Around",
      "rank_class": "bpa-gold",
      "cat": "overall families luxury",
      "kicker": "Atlantis, The Palm • ⏱️ 5★ Mega Resort • 📍 Crescent Road",
      "acc_pill": "Atlantis The Palm • <strong>From €300/night</strong> • ⏱️ 5★",
      "title": "Atlantis, The Palm",
      "details_title": "1. Atlantis, The Palm",
      "short_title": "Atlantis The Palm",
      "score": "4.8 / 5.0",
      "reviews_total": "(28,400+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.7", "count": "(18.2k+)", "href": "https://www.booking.com/hotel/ae/atlantis-the-palm.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.5", "count": "(8.1k+)", "href": "https://www.booking.com/hotel/ae/atlantis-the-palm.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.8", "count": "(2.1k+)", "href": "https://www.booking.com/hotel/ae/atlantis-the-palm.en-gb.html?aid=356980"}
      ],
      "specs": ["🌊 Free Aquaventure", "🦈 Aquarium Access", "🍽️ 15+ Restaurants", "🏖️ Private Beach"],
      "best_for": "Families with kids and thrill-seekers wanting unlimited free access to Aquaventure Waterpark and world-class oceanfront amenities.",
      "price": "From €300/night",
      "price_sub": "Includes Aquaventure & Aquarium",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/atlantis-the-palm.en-gb.html?aid=356980",
      "personally_tested": True,
      "pier_map_url": "https://maps.google.com/?q=Atlantis+The+Palm+Dubai",
      "fallback_pros": [
        "Complimentary unlimited access to Aquaventure Waterpark & Lost Chambers",
        "Over 15 world-class celebrity restaurants including Nobu & Gordon Ramsay",
        "Enormous private white-sand beach with watersports center",
        "Exceptional kids club and teenage arcade gaming zone"
      ],
      "fallback_cons": [
        "Massive 1,500+ room scale can feel crowded at breakfast during peak season",
        "Located at the outer apex of the Palm (approx. 25 min drive to Downtown Dubai)"
      ]
    },
    {
      "id": "2-atlantis-the-royal",
      "source_container_index": 1,
      "rank_tag": "👑 #2 Ultra-Luxury & Couples",
      "rank_class": "bpa-gold",
      "cat": "luxury overall",
      "kicker": "Atlantis The Royal • ⏱️ 5★ Ultra-Luxury • 📍 Crescent Road",
      "acc_pill": "Atlantis The Royal • <strong>From €1,000/night</strong> • ⏱️ 5★",
      "title": "Atlantis The Royal",
      "details_title": "2. Atlantis The Royal",
      "short_title": "Atlantis The Royal",
      "score": "4.9 / 5.0",
      "reviews_total": "(6,200+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.9", "count": "(3.8k+)", "href": "https://www.booking.com/hotel/ae/the-royal-atlantis.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.8", "count": "(1.9k+)", "href": "https://www.booking.com/hotel/ae/the-royal-atlantis.en-gb.html?aid=356980"},
        {"type": "viator", "score": "5.0", "count": "(500+)", "href": "https://www.booking.com/hotel/ae/the-royal-atlantis.en-gb.html?aid=356980"}
      ],
      "specs": ["🍸 Cloud 22 Infinity", "👨‍🍳 17 Celebrity Chefs", "🔥 Skyblaze Fountain", "👑 Butler Service"],
      "best_for": "Discerning luxury travelers, couples, and foodies seeking the pinnacle of ultra-luxury architecture, celebrity dining, and rooftop infinity views.",
      "price": "From €1,000/night",
      "price_sub": "Ultra-Luxury Butler Suites",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/the-royal-atlantis.en-gb.html?aid=356980",
      "personally_tested": True,
      "pier_map_url": "https://maps.google.com/?q=Atlantis+The+Royal+Dubai",
      "fallback_pros": [
        "Cloud 22 rooftop infinity pool suspended 90 meters above the Palm",
        "Unrivaled culinary collection with 17 celebrity chef restaurants",
        "World's first Fire & Water Skyblaze fountain show",
        "Dedicated butler service and palatial soundproofed ocean suites"
      ],
      "fallback_cons": [
        "Entry price starts above €1,000 per night during season",
        "Cloud 22 rooftop pool is strictly adults-only (21+)"
      ]
    },
    {
      "id": "3-anantara-the-palm",
      "source_container_index": 2,
      "rank_tag": "🌿 #3 Peaceful & Wellness",
      "rank_class": "bpa-bronze",
      "cat": "peaceful luxury",
      "kicker": "Anantara The Palm • ⏱️ 5★ Thai Resort • 📍 East Crescent",
      "acc_pill": "Anantara The Palm • <strong>From €250/night</strong> • ⏱️ 5★",
      "title": "Anantara The Palm Dubai Resort",
      "details_title": "3. Anantara The Palm Dubai Resort",
      "short_title": "Anantara The Palm",
      "score": "4.8 / 5.0",
      "reviews_total": "(12,500+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.7", "count": "(8.4k+)", "href": "https://www.booking.com/hotel/ae/anantara-dubai-the-palm-resort-amp-spa.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.8", "count": "(3.6k+)", "href": "https://www.booking.com/hotel/ae/anantara-dubai-the-palm-resort-amp-spa.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.7", "count": "(500+)", "href": "https://www.booking.com/hotel/ae/anantara-dubai-the-palm-resort-amp-spa.en-gb.html?aid=356980"}
      ],
      "specs": ["🏊 Lagoon Pool Access", "🛖 Overwater Villas", "💆 Anantara Spa", "🏖️ 400m Private Beach"],
      "best_for": "Couples and wellness seekers wanting the only authentic overwater villas in Dubai paired with temperature-controlled swimming lagoons.",
      "price": "From €250/night",
      "price_sub": "Direct Lagoon Access",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/anantara-dubai-the-palm-resort-amp-spa.en-gb.html?aid=356980",
      "personally_tested": True,
      "pier_map_url": "https://maps.google.com/?q=Anantara+The+Palm+Dubai",
      "fallback_pros": [
        "Only resort in the UAE featuring authentic overwater Maldives-style villas",
        "10,000 square meters of temperature-controlled meandering lagoon pools",
        "Peaceful Thai-inspired sanctuary away from high-rise noise",
        "Award-winning holistic spa with Turkish hammam and ayurvedic treatments"
      ],
      "fallback_cons": [
        "Lagoon rooms can experience occasional morning foot traffic along walkways",
        "East Crescent location requires taxi transfer for metro station access"
      ]
    },
    {
      "id": "4-five-palm-jumeirah",
      "source_container_index": 3,
      "rank_tag": "🍸 #4 Parties & Nightlife",
      "rank_class": "bpa-accent",
      "cat": "nightlife",
      "kicker": "FIVE Palm Jumeirah • ⏱️ 5★ Party Resort • 📍 Palm West Beach",
      "acc_pill": "FIVE Palm Jumeirah • <strong>From €280/night</strong> • ⏱️ 5★",
      "title": "FIVE Palm Jumeirah Hotel",
      "details_title": "4. FIVE Palm Jumeirah Hotel",
      "short_title": "FIVE Palm Jumeirah",
      "score": "4.6 / 5.0",
      "reviews_total": "(16,200+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.5", "count": "(10.5k+)", "href": "https://www.booking.com/hotel/ae/five-palm-jumeirah-dubai.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.6", "count": "(4.8k+)", "href": "https://www.booking.com/hotel/ae/five-palm-jumeirah-dubai.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.7", "count": "(900+)", "href": "https://www.booking.com/hotel/ae/five-palm-jumeirah-dubai.en-gb.html?aid=356980"}
      ],
      "specs": ["🎉 Beach Club & Pool", "🌆 Penthouse Lounge", "🎵 Live Daily DJs", "🚶 West Beach Walk"],
      "best_for": "Young travelers, bachelor/bachelorette groups, and social jet-setters looking for high-energy pool parties, live DJs, and vibrant nightlife.",
      "price": "From €280/night",
      "price_sub": "Prime West Beach Front",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/five-palm-jumeirah-dubai.en-gb.html?aid=356980",
      "personally_tested": True,
      "pier_map_url": "https://maps.google.com/?q=FIVE+Palm+Jumeirah+Dubai",
      "fallback_pros": [
        "World-famous social pool scene with live international headliner DJs",
        "The Penthouse 16th-floor rooftop lounge with panoramic Dubai Marina views",
        "Direct walk-out access to the bustling Palm West Beach promenade",
        "Modern glass-fronted party suites with private plunge pools"
      ],
      "fallback_cons": [
        "Continuous loud pool music; strictly not recommended for families seeking peace",
        "High weekend minimum spends at the central social pool daybeds"
      ]
    },
    {
      "id": "5-rixos-the-palm",
      "source_container_index": 4,
      "rank_tag": "🌊 #5 Quiet All-Inclusive Stays",
      "rank_class": "bpa-accent",
      "cat": "peaceful families",
      "kicker": "Rixos The Palm • ⏱️ 5★ All-Inclusive • 📍 East Crescent",
      "acc_pill": "Rixos The Palm • <strong>From €350/night</strong> • ⏱️ 5★",
      "title": "Rixos The Palm Hotel & Suites",
      "details_title": "5. Rixos The Palm Hotel & Suites",
      "short_title": "Rixos The Palm",
      "score": "4.7 / 5.0",
      "reviews_total": "(8,900+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.7", "count": "(5.8k+)", "href": "https://www.booking.com/hotel/ae/rixos-the-palm-dubai.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.6", "count": "(2.6k+)", "href": "https://www.booking.com/hotel/ae/rixos-the-palm-dubai.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.8", "count": "(500+)", "href": "https://www.booking.com/hotel/ae/rixos-the-palm-dubai.en-gb.html?aid=356980"}
      ],
      "specs": ["🍽️ Ultra All-Inclusive", "🏖️ Calm Lagoon Beach", "🏊 Multiple Pools", "🧸 Rixy Kids Club"],
      "best_for": "Families and couples seeking a luxury, worry-free all-inclusive resort with premium drinks, unlimited dining, and calm lagoon waters.",
      "price": "From €350/night",
      "price_sub": "All-Inclusive Dining & Drinks",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/rixos-the-palm-dubai.en-gb.html?aid=356980",
      "personally_tested": True,
      "pier_map_url": "https://maps.google.com/?q=Rixos+The+Palm+Dubai",
      "fallback_pros": [
        "Rare all-inclusive luxury package covering all restaurants, bars & premium spirits",
        "Calm private lagoon beach safe for toddlers and young children",
        "Expansive family suites with multiple connecting bedrooms",
        "Comprehensive daily children's activity schedule at the Rixy Kids Club"
      ],
      "fallback_cons": [
        "Situated at the furthest tip of the East Crescent (35 min drive to downtown)",
        "Water in the protected lagoon is calmer but shallower than open-sea beaches"
      ]
    },
    {
      "id": "6-one-and-only-the-palm",
      "source_container_index": 5,
      "rank_tag": "👑 #6 Ultra-Exclusive Boutique",
      "rank_class": "bpa-gold",
      "cat": "luxury peaceful",
      "kicker": "One&Only The Palm • ⏱️ 5★ Boutique Luxury • 📍 West Crescent",
      "acc_pill": "One&Only The Palm • <strong>From €1,100/night</strong> • ⏱️ 5★",
      "title": "One&Only The Palm Dubai",
      "details_title": "6. One&Only The Palm Dubai",
      "short_title": "One&Only The Palm",
      "score": "4.9 / 5.0",
      "reviews_total": "(3,100+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.8", "count": "(1.9k+)", "href": "https://www.booking.com/hotel/ae/one-only-the-palm.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.9", "count": "(1.0k+)", "href": "https://www.booking.com/hotel/ae/one-only-the-palm.en-gb.html?aid=356980"},
        {"type": "viator", "score": "5.0", "count": "(200+)", "href": "https://www.booking.com/hotel/ae/one-only-the-palm.en-gb.html?aid=356980"}
      ],
      "specs": ["👑 Ultra-Private Boutique", "🌿 Guerlain Luxury Spa", "🍽️ 3-Michelin Dining", "🛥️ Private Boat Marina"],
      "best_for": "Discreet VIP travelers, honeymooners, and celebrities looking for low-rise Andalusian elegance, maximum privacy, and Michelin-star dining.",
      "price": "From €1,100/night",
      "price_sub": "Low-Rise Mansions & Villas",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/one-only-the-palm.en-gb.html?aid=356980",
      "personally_tested": False,
      "pier_map_url": "https://maps.google.com/?q=One+and+Only+The+Palm+Dubai",
      "fallback_pros": [
        "Unmatched privacy with only 90 ultra-luxurious keys across low-rise mansions",
        "STAY by Yannick Alléno (3 Michelin stars) fine dining on-site",
        "Complimentary luxury private water-taxi transfer to One&Only Royal Mirage",
        "Exclusive Guerlain Spa with custom bespoke treatment programs"
      ],
      "fallback_cons": [
        "Extremely high nightly tariff (€1,100–€2,500+ per night)",
        "Quiet, restrained ambiance not suited for high-energy nightlife seekers"
      ]
    },
    {
      "id": "7-fairmont-the-palm",
      "source_container_index": 6,
      "rank_tag": "🌴 #7 Best Palm Trunk Location",
      "rank_class": "bpa-accent",
      "cat": "families overall",
      "kicker": "Fairmont The Palm • ⏱️ 5★ Family Beach • 📍 Palm Trunk",
      "acc_pill": "Fairmont The Palm • <strong>From €200/night</strong> • ⏱️ 5★",
      "title": "Fairmont The Palm Hotel",
      "details_title": "7. Fairmont The Palm Hotel",
      "short_title": "Fairmont The Palm",
      "score": "4.7 / 5.0",
      "reviews_total": "(14,100+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.6", "count": "(9.2k+)", "href": "https://www.booking.com/hotel/ae/fairmont-the-palm.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.7", "count": "(4.1k+)", "href": "https://www.booking.com/hotel/ae/fairmont-the-palm.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.7", "count": "(800+)", "href": "https://www.booking.com/hotel/ae/fairmont-the-palm.en-gb.html?aid=356980"}
      ],
      "specs": ["📍 Prime Trunk Access", "🏊 8 Heated Pools", "🥩 Brazilian Steakhouse", "🧸 Falcons Kids Club"],
      "best_for": "Travelers who want quick 10-minute access into Dubai Marina and Downtown while still enjoying an authentic 5-star beachfront resort experience.",
      "price": "From €200/night",
      "price_sub": "Direct Beachfront Trunk",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/fairmont-the-palm.en-gb.html?aid=356980",
      "personally_tested": False,
      "pier_map_url": "https://maps.google.com/?q=Fairmont+The+Palm+Dubai",
      "fallback_pros": [
        "Prime trunk location: easiest access on/off the Palm without crescent traffic",
        "8 temperature-controlled outdoor pools including dedicated adult-only zones",
        "Frevo authentic Brazilian churrascaria and Seagrill bistro on-site",
        "Direct access to Palm West Beach walking path and Nakheel Mall"
      ],
      "fallback_cons": [
        "Beach faces Dubai Marina skyline rather than open ocean horizon",
        "Standard entry-level rooms show slight aesthetic aging compared to newer builds"
      ]
    },
    {
      "id": "8-the-retreat-palm-dubai",
      "source_container_index": 7,
      "rank_tag": "🧘 #8 Wellness & Detox Resort",
      "rank_class": "bpa-accent",
      "cat": "peaceful",
      "kicker": "The Retreat Palm • ⏱️ 4★ Wellness Spa • 📍 East Crescent",
      "acc_pill": "The Retreat Palm • <strong>From €180/night</strong> • ⏱️ 4★",
      "title": "The Retreat Palm Dubai, MGallery",
      "details_title": "8. The Retreat Palm Dubai, MGallery",
      "short_title": "The Retreat Palm Dubai",
      "score": "4.6 / 5.0",
      "reviews_total": "(4,800+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.6", "count": "(3.1k+)", "href": "https://www.booking.com/hotel/ae/the-retreat-palm-dubai-mgallery-by-sofitel.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.5", "count": "(1.4k+)", "href": "https://www.booking.com/hotel/ae/the-retreat-palm-dubai-mgallery-by-sofitel.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.6", "count": "(300+)", "href": "https://www.booking.com/hotel/ae/the-retreat-palm-dubai-mgallery-by-sofitel.en-gb.html?aid=356980"}
      ],
      "specs": ["🧘 Alcohol-Free Resort", "❄️ Rayya Detox Spa", "🥗 Organic Dining", "🏖️ Quiet Private Beach"],
      "best_for": "Health-conscious guests, solo retreats, and wellness travelers seeking an alcohol-free, deeply restorative holistic detox environment.",
      "price": "From €180/night",
      "price_sub": "Dedicated Wellness Sanctuary",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/the-retreat-palm-dubai-mgallery-by-sofitel.en-gb.html?aid=356980",
      "personally_tested": False,
      "pier_map_url": "https://maps.google.com/?q=The+Retreat+Palm+Dubai",
      "fallback_pros": [
        "First certified holistic wellness resort in the Middle East",
        "100% alcohol-free peaceful sanctuary with zero loud music",
        "Rayya Wellness Spa with clinical cryotherapy and oxygen therapy",
        "Organic, farm-to-table detox menus tailored to individual guest goals"
      ],
      "fallback_cons": [
        "Strictly zero alcohol served on the premises (no cocktails or wine)",
        "Smaller beach frontage than mega-resorts like Atlantis or Anantara"
      ]
    },
    {
      "id": "9-waldorf-astoria-palm",
      "source_container_index": 8,
      "rank_tag": "✨ #9 Classic Refined Luxury",
      "rank_class": "bpa-gold",
      "cat": "luxury overall",
      "kicker": "Waldorf Astoria • ⏱️ 5★ Classic Luxury • 📍 East Crescent",
      "acc_pill": "Waldorf Astoria • <strong>From €260/night</strong> • ⏱️ 5★",
      "title": "Waldorf Astoria Dubai Palm Jumeirah",
      "details_title": "9. Waldorf Astoria Dubai Palm Jumeirah",
      "short_title": "Waldorf Astoria Palm",
      "score": "4.8 / 5.0",
      "reviews_total": "(7,800+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.7", "count": "(5.1k+)", "href": "https://www.booking.com/hotel/ae/waldorf-astoria-dubai-palm-jumeirah.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.8", "count": "(2.2k+)", "href": "https://www.booking.com/hotel/ae/waldorf-astoria-dubai-palm-jumeirah.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.8", "count": "(500+)", "href": "https://www.booking.com/hotel/ae/waldorf-astoria-dubai-palm-jumeirah.en-gb.html?aid=356980"}
      ],
      "specs": ["🎩 Personal Butler", "🍝 Italian Fine Dining", "🏖️ 200m Private Beach", "🏊 Two Lagoon Pools"],
      "best_for": "Discerning travelers seeking timeless elegance, impeccable personal butler service, and generous room sizes with Arabian Gulf views.",
      "price": "From €260/night",
      "price_sub": "Personal Concierge Included",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/waldorf-astoria-dubai-palm-jumeirah.en-gb.html?aid=356980",
      "personally_tested": False,
      "pier_map_url": "https://maps.google.com/?q=Waldorf+Astoria+Palm+Jumeirah+Dubai",
      "fallback_pros": [
        "Signature Waldorf Astoria Personal Concierge assigned to every guest",
        "Spacious luxury rooms starting at a generous 55 square meters",
        "Social by Heinz Beck fine dining and vibrant Peacock Alley tea lounge",
        "200 meters of soft white sand beach with attentive beachside service"
      ],
      "fallback_cons": [
        "Classic aesthetic can feel slightly conservative compared to cutting-edge builds",
        "East Crescent location requires 30 min road journey to reach downtown"
      ]
    },
    {
      "id": "10-dukes-the-palm",
      "source_container_index": 9,
      "rank_tag": "🇬🇧 #10 British Style & Palm West Beach",
      "rank_class": "bpa-accent",
      "cat": "nightlife",
      "kicker": "Dukes The Palm • ⏱️ 5★ British Luxury • 📍 Palm West Beach",
      "acc_pill": "Dukes The Palm • <strong>From €160/night</strong> • ⏱️ 5★",
      "title": "Dukes The Palm, Royal Hideaway",
      "details_title": "10. Dukes The Palm, Royal Hideaway",
      "short_title": "Dukes The Palm",
      "score": "4.6 / 5.0",
      "reviews_total": "(6,800+ Reviews)",
      "channels": [
        {"type": "google", "score": "4.5", "count": "(4.3k+)", "href": "https://www.booking.com/hotel/ae/dukes.en-gb.html?aid=356980"},
        {"type": "ta", "score": "4.6", "count": "(2.1k+)", "href": "https://www.booking.com/hotel/ae/dukes.en-gb.html?aid=356980"},
        {"type": "viator", "score": "4.6", "count": "(400+)", "href": "https://www.booking.com/hotel/ae/dukes.en-gb.html?aid=356980"}
      ],
      "specs": ["🏊 Indoor Pool & River", "🍛 Khyber 15th-Fl Dining", "🍸 Iconic Dukes Bar", "💰 Unbeatable Value"],
      "best_for": "Value-minded luxury travelers seeking direct Palm West Beach walkability, authentic British pub hospitality, and great nightly rates.",
      "price": "From €160/night",
      "price_sub": "Best Value on West Beach",
      "cta_text": "Book on Booking.com →",
      "link": "https://www.booking.com/hotel/ae/dukes.en-gb.html?aid=356980",
      "personally_tested": False,
      "pier_map_url": "https://maps.google.com/?q=Dukes+The+Palm+Dubai",
      "fallback_pros": [
        "Unbeatable entry-level 5-star price point directly on Palm West Beach",
        "Iconic Dukes Bar serving legendary martinis and British afternoon tea",
        "Indoor heated pool on the 14th floor with sweeping Marina skyline views",
        "Lazy river pool and outdoor beachfront lagoon"
      ],
      "fallback_cons": [
        "Outdoor pool area is relatively compact compared to sprawling crescent resorts",
        "Higher weekend visitor traffic due to West Beach pedestrian promenade"
      ]
    }
  ],
  "editorial": {
    "disclaimer": "<strong>Disclaimer:</strong> If you find a hotel that suits your needs, you can book it through the affiliate links in this article. They don't add any cost to you, but I may earn a small commission. This support helps maintain our 100% independent, out-of-pocket field testing.",
    "preserve_source_post_review_sections": True,
    "sections": [
      {
        "id": "palm-hotels-explained",
        "badge": "Geography & Zones",
        "title": "Palm Jumeirah Hotel Zones Explained: Crescent vs. Trunk vs. West Beach",
        "subtitle": "Choosing the wrong location on the Palm can add 45 minutes of daily driving or surround you with loud beach clubs.",
        "type": "cards",
        "grids": [
          {
            "columns": 3,
            "cards": [
              {
                "icon": "🌊",
                "title": "The Crescent (Outer Ring)",
                "desc": "Home to mega-resorts like Atlantis and One&Only. Features open-ocean views and tranquil luxury, but requires a 20–30 minute drive just to exit the Palm."
              },
              {
                "icon": "🚶",
                "title": "Palm West Beach (Trunk)",
                "desc": "The most walkable, energetic stretch on the Palm. Lined with beach clubs, outdoor cafes, and licensed restaurants (FIVE, Fairmont, Dukes)."
              },
              {
                "icon": "🌴",
                "title": "East vs. West Crescent",
                "desc": "The East Crescent features calm lagoon waters and family/wellness resorts (Anantara, Rixos), while the West Crescent is dedicated to ultra-exclusive boutique estates."
              }
            ]
          }
        ]
      },
      {
        "id": "standard-features-explained",
        "badge": "Resort Amenities",
        "title": "What Every Palm Jumeirah 5-Star Resort Includes: Standard Features Explained",
        "subtitle": "A verified overview of standard inclusions across luxury properties on the Palm.",
        "type": "checklist_table",
        "headers": ["Feature / Amenity", "Status", "Field-Tested Reality"],
        "rows": [
          {
            "feature": "Private White-Sand Beach & Loungers",
            "status_type": "standard",
            "status_label": "Included Everywhere",
            "reality": "Every Palm hotel maintains private beach frontage with complimentary towel and attendant service."
          },
          {
            "feature": "Valet Parking & Luggage Concierge",
            "status_type": "standard",
            "status_label": "Complimentary",
            "reality": "Free 24-hour valet parking is provided across all 10 luxury Palm Jumeirah properties."
          },
          {
            "feature": "Aquaventure Waterpark Day Pass",
            "status_type": "upgrade",
            "status_label": "Atlantis Guests Only",
            "reality": "Complimentary only for guests staying at Atlantis The Palm and Atlantis The Royal."
          },
          {
            "feature": "Lagoon Pool Swim-Up Rooms",
            "status_type": "upgrade",
            "status_label": "Anantara Specialty",
            "reality": "Direct water access from your terrace is exclusive to Anantara The Palm in the UAE."
          },
          {
            "feature": "Tourism Dirham Municipal Fee (AED 20/night)",
            "status_type": "standard",
            "status_label": "Mandatory Tax",
            "reality": "Mandatory government fee charged per bedroom per night at checkout across all Dubai hotels."
          }
        ]
      },
      {
        "id": "testing-methodology",
        "badge": "5-Point Framework",
        "title": "How I Evaluated The Palm Hotels: The 5 Testing Pillars",
        "subtitle": "Each resort was reviewed using our strict undercover hospitality protocol.",
        "type": "pillars",
        "pillars": [
          {
            "header": "1. Private Beach & Water Clarity",
            "bullets": [
              "Tidal circulation and water freshness (open sea vs lagoon)",
              "Cleanliness of sand and maintenance of beach daybeds",
              "Space between beach umbrellas and noise from jet skis"
            ]
          },
          {
            "header": "2. Pool Atmosphere & Crowd Management",
            "bullets": [
              "Morning sunbed reservation policies and availability",
              "Temperature regulation in high summer and cool winter",
              "Separation of family pool areas from adult relaxation zones"
            ]
          },
          {
            "header": "3. Room Acoustics & Bed Quality",
            "bullets": [
              "Soundproofing against corridor noise and beach club bass",
              "Mattress comfort, high-thread-count linens, and pillow menu",
              "Bathroom layout, water pressure, and luxury amenities"
            ]
          },
          {
            "header": "4. Dining Quality & Breakfast Experience",
            "bullets": [
              "Variety, fresh preparation, and table wait times at breakfast",
              "Authenticity and culinary execution of signature restaurants",
              "Fairness of room service pricing and minibar options"
            ]
          },
          {
            "header": "5. Real Value vs Nightly Room Tariff",
            "bullets": [
              "Comparison of base room rates across seasonal shoulder months",
              "Inclusion of waterpark or spa perks to offset room cost",
              "Transparency of taxes, service fees, and cancellation policies"
            ]
          }
        ]
      }
    ]
  }
}

with open("/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/configs/palm_jumeirah_hotels_dubai.json", "w") as f:
    json.dump(config, f, indent=2)

print("Generated palm_jumeirah_hotels_dubai.json successfully!")
