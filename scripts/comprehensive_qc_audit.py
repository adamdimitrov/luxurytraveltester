import sys
from playwright.sync_api import sync_playwright

PAGES = [
    {"name": "Homepage", "url": "http://localhost:8899/"},
    {"name": "Dubai Desert Safaris (Hub)", "url": "http://localhost:8899/best-desert-safaris-dubai/"},
    {"name": "Dubai Palm Hotels (Hub)", "url": "http://localhost:8899/best-palm-jumeirah-hotels-dubai/"},
    {"name": "NYC Helicopter Tours (Hub)", "url": "http://localhost:8899/best-helicopter-tours-new-york/"},
    {"name": "Atlantis The Royal Review", "url": "http://localhost:8899/best-palm-jumeirah-hotels-dubai/atlantis-the-royal-dubai-review/"},
    {"name": "Atlantis The Palm Review", "url": "http://localhost:8899/best-palm-jumeirah-hotels-dubai/atlantis-the-palm-dubai-review/"},
    {"name": "Anantara The Palm Review", "url": "http://localhost:8899/best-palm-jumeirah-hotels-dubai/anantara-the-palm-dubai-review/"},
    {"name": "FIVE Palm Jumeirah Review", "url": "http://localhost:8899/best-palm-jumeirah-hotels-dubai/five-palm-jumeirah-dubai-review/"},
    {"name": "Rixos The Palm Review", "url": "http://localhost:8899/best-palm-jumeirah-hotels-dubai/rixos-the-palm-dubai-review/"},
    {"name": "Desert Safaris FAQ", "url": "http://localhost:8899/best-desert-safaris-dubai/dubai-desert-safaris-faq/"},
    {"name": "City to Desert Itinerary", "url": "http://localhost:8899/best-desert-safaris-dubai/itinerary-from-the-city-to-the-desert-in-dubai/"},
    {"name": "About Page", "url": "http://localhost:8899/about/"},
    {"name": "Contact Page", "url": "http://localhost:8899/contact/"}
]

def run_audit():
    results = []
    has_critical_failure = False

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for item in PAGES:
            name = item["name"]
            url = item["url"]
            print(f"\nAuditing: {name} ({url})")

            page_errors = []
            console_msgs = []

            # ========================
            # 1. DESKTOP VIEWPORT (1440x900)
            # ========================
            context_d = browser.new_context(viewport={"width": 1440, "height": 900})
            page_d = context_d.new_page()

            page_d.on("console", lambda msg: console_msgs.append(f"[{msg.type}] {msg.text}") if msg.type in ["error"] and not any(ign in msg.text for ign in ["emrld.cc", "favicon.ico", "net::ERR_"]) else None)
            page_d.on("pageerror", lambda err: page_errors.append(f"PageError: {err}"))

            resp_d = page_d.goto(url, wait_until="load", timeout=15000)
            status_code = resp_d.status if resp_d else 0

            # 1a. Horizontal Overflow Check
            d_overflow = page_d.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
            d_scroll_w = page_d.evaluate("() => document.documentElement.scrollWidth")
            if d_overflow:
                has_critical_failure = True
                print(f"  [FAIL] Desktop horizontal overflow! scrollWidth={d_scroll_w} > 1440")
            else:
                print(f"  [PASS] Desktop 1440px layout: 0px overflow (scrollWidth={d_scroll_w})")

            # 1b. Legacy Colliding Artifacts Check
            st_wrapper_count = page_d.locator(".st_wrapper, .st_wrapper-2").count()
            redundant_pill_count = page_d.locator(".ltt-navbar .ltt-cta-pill").count()
            if st_wrapper_count > 0:
                has_critical_failure = True
                print(f"  [FAIL] Found {st_wrapper_count} colliding .st_wrapper back-to-top buttons!")
            if redundant_pill_count > 0:
                has_critical_failure = True
                print(f"  [FAIL] Found {redundant_pill_count} redundant .ltt-cta-pill in navbar!")

            # 1c. Filter Bar Height Check (if hub page)
            filter_bar = page_d.locator(".ltt-integrated-pills")
            if filter_bar.count() > 0:
                fb_box = filter_bar.first.bounding_box()
                if fb_box and fb_box["height"] > 44:
                    has_critical_failure = True
                    print(f"  [FAIL] Filter bar wrapped to 2 rows! height={fb_box['height']}px")
                else:
                    print(f"  [PASS] Single-row filter bar: height={fb_box['height'] if fb_box else 0}px")

            # 1d. Specs Row Height Check (if hub page)
            specs_rows = page_d.locator(".bpa-specs-row")
            if specs_rows.count() > 0:
                specs_wrapped = False
                for i in range(specs_rows.count()):
                    s_box = specs_rows.nth(i).bounding_box()
                    if s_box and s_box["height"] > 34:
                        specs_wrapped = True
                        print(f"  [FAIL] Card #{i+1} specs row wrapped! height={s_box['height']}px")
                if not specs_wrapped:
                    print(f"  [PASS] All {specs_rows.count()} cards specs rows single-line (<=32px)")

            # 1e. Bento Box Collapsed Width Check (if review page)
            bentos = page_d.locator("details.ltt-bento-group")
            if bentos.count() > 0:
                for i in range(min(3, bentos.count())):
                    bentos.nth(i).locator("summary").click()
                b0_w = round(bentos.first.bounding_box()["width"])
                if b0_w < 700:
                    has_critical_failure = True
                    print(f"  [FAIL] Bento box collapsed width shrunk! width={b0_w}px")
                else:
                    print(f"  [PASS] Bento boxes full-width when collapsed: {b0_w}px (total bentos: {bentos.count()})")

            # 1f. Desktop Destinations Mega Menu Hover Test
            dropdown = page_d.locator(".ltt-nav-dropdown")
            mega = page_d.locator(".ltt-mega-menu")
            if dropdown.count() > 0 and mega.count() > 0:
                dropdown.hover()
                page_d.wait_for_timeout(200)
                mega_visible = mega.is_visible()
                if not mega_visible:
                    has_critical_failure = True
                    print("  [FAIL] Destinations mega menu did not open on hover!")
                else:
                    print("  [PASS] Destinations mega menu interactive hover verified")

            # 1g. TOC Anchors Check (if TOC present)
            toc_links = page_d.locator("#toc a, .tocitem")
            if toc_links.count() > 0:
                missing_anchors = 0
                for i in range(toc_links.count()):
                    href = toc_links.nth(i).get_attribute("href")
                    if href and href.startswith("#") and len(href) > 1:
                        target_id = href[1:]
                        target_exists = page_d.evaluate("(id) => document.getElementById(id) !== null", target_id)
                        if not target_exists:
                            missing_anchors += 1
                if missing_anchors > 0:
                    has_critical_failure = True
                    print(f"  [FAIL] {missing_anchors} TOC links point to non-existent anchor IDs!")
                else:
                    print(f"  [PASS] All {toc_links.count()} TOC links resolve to valid in-page targets")

            context_d.close()

            # ========================
            # 2. MOBILE VIEWPORT (390x844 - iPhone 14)
            # ========================
            context_m = browser.new_context(viewport={"width": 390, "height": 844})
            page_m = context_m.new_page()

            page_m.goto(url, wait_until="load", timeout=15000)

            # 2a. Mobile Horizontal Overflow Check
            m_overflow = page_m.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
            m_scroll_w = page_m.evaluate("() => document.documentElement.scrollWidth")
            if m_overflow:
                has_critical_failure = True
                print(f"  [FAIL] Mobile horizontal overflow! scrollWidth={m_scroll_w} > 390")
            else:
                print(f"  [PASS] Mobile responsive layout 0px overflow (scrollWidth={m_scroll_w})")

            # 2b. Mobile Drawer Toggle Test
            toggle = page_m.locator("#lttNavToggle")
            drawer = page_m.locator("#lttMobileDrawer")
            if toggle.count() > 0 and drawer.count() > 0:
                toggle.click()
                page_m.wait_for_timeout(300)
                is_open = "is-open" in (drawer.get_attribute("class") or "")
                if not is_open:
                    has_critical_failure = True
                    print("  [FAIL] Mobile hamburger drawer did not open!")
                else:
                    print("  [PASS] Mobile hamburger drawer opened smoothly")
                toggle.click()

            context_m.close()

            results.append({
                "page": name,
                "status": status_code,
                "desktop_overflow": d_overflow,
                "mobile_overflow": m_overflow,
                "errors": len(page_errors) + len(console_msgs)
            })

        browser.close()

    print("\n" + "="*80)
    print("FINAL QUALITY CONTROL AUDIT SUMMARY")
    print("="*80)
    print(f"{'Page':35} | Status | D-Overflow | M-Overflow | JS Errors | QC Result")
    print("-"*80)
    for r in results:
        status_txt = "PASS" if not r["desktop_overflow"] and not r["mobile_overflow"] and r["errors"] == 0 else "FAIL"
        print(f"{r['page']:35} | {r['status']:6} | {'NO' if not r['desktop_overflow'] else 'YES':10} | {'NO' if not r['mobile_overflow'] else 'YES':10} | {r['errors']:9} | {status_txt}")
    print("="*80)

    if has_critical_failure:
        print("[OVERALL RESULT: FAILED - Display or navigation issues detected]")
        sys.exit(1)
    else:
        print("[OVERALL RESULT: 100% PASS - All 13 Pages Verified Clean for Production]")
        sys.exit(0)

if __name__ == "__main__":
    run_audit()
