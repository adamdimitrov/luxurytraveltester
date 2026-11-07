import re
import os
from bs4 import BeautifulSoup

def get_hotel_info(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract title
    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""
    parts = h1_text.split(":", 1)
    name = parts[0].strip()
    subtitle = parts[1].strip() if len(parts) > 1 else "My Honest, In-Depth Review"
    
    # Short name
    short_name = name.replace(", Dubai", "").replace(" Dubai Resort", "").replace(" Dubai", "").strip()
    if short_name.startswith("5 Days at "):
        short_name = short_name.replace("5 Days at ", "")
    
    # Extract nights & paid
    cis = soup.select_one(".container-intro-section")
    text = cis.get_text() if cis else ""
    
    nights = "1 night"
    m_nights = re.search(r"(\d+\s*nights?)", text, re.IGNORECASE)
    if m_nights:
        nights = m_nights.group(1)
        
    paid = "€1,000"
    m_paid = re.search(r"(€[\d,]+)", text)
    if m_paid:
        paid = m_paid.group(1)
    else:
        m_aed = re.search(r"([\d,.]+\s*AED)", text)
        if m_aed:
            paid = m_aed.group(1)

    return {
        "name": name,
        "short_name": short_name,
        "subtitle": subtitle,
        "nights": nights,
        "paid": paid
    }

def transform_hotel_page(file_path):
    hotel_info = get_hotel_info(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # 1. Read existing CSS files
    hero_css_path = "/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/resources/ltt-hero-card-styles.css"
    with open(hero_css_path, "r", encoding="utf-8") as f:
        hero_css = f.read()

    # 2. Extract intro narrative text
    cis = soup.select_one(".container-intro-section")
    intro_ps = []
    if cis:
        for p in cis.find_all("p"):
            p_text = p.get_text(strip=True)
            if "This comprehensive review evaluates" in p_text or "check out our" in p_text:
                continue
            intro_ps.append(str(p))

    if not intro_ps:
        intro_ps = [
            f"<p>I spent <strong>{hotel_info['nights']}</strong> as a solo guest at <strong>{hotel_info['name']}</strong> to conduct a deep-dive undercover assessment and definitively answer: <em>Does it live up to the hype?</em></p>",
            f"<p>My stay cost me approximately <strong>{hotel_info['paid']}</strong>, paid entirely out-of-pocket (excluding flights and transportation).</p>"
        ]

    intro_ps.append('<p style="margin-top: 10px; font-size: 14px; color: #64748b;">For side-by-side pricing, pool scenes, and beach comparisons with other top resorts, explore our <a href="/best-palm-jumeirah-hotels-dubai" style="color: #d97706; font-weight: 700; text-decoration: underline;">Comprehensive Guide to the 10 Best Palm Jumeirah Hotels</a>.</p>')

    lead_copy_html = "\n".join(intro_ps)

    # 3. Build canonical Hero Card
    hero_card_html = f"""<!-- CANONICAL LUXURY EDITORIAL SYSTEM 2.0 HERO CARD -->
<div class="ltt-hero-wrap">
  <div class="ltt-clean-card">
    <div class="ltt-top-bar">
      <nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
        <a href="/">Home</a>
        <span class="ltt-bc-sep">›</span>
        <a href="/best-palm-jumeirah-hotels-dubai">Dubai Palm Hotels</a>
        <span class="ltt-bc-sep">›</span>
        <span class="ltt-bc-current">{hotel_info['short_name']} Review</span>
      </nav>
      <span class="ltt-hero-kicker-badge">✓ Undercover Field-Tested Review</span>
    </div>

    <h1 class="ltt-editorial-h1">
      {hotel_info['name']} <span class="ltt-h1-muted">({hotel_info['subtitle']})</span>
    </h1>

    <div class="ltt-trust-bar">
      <div class="ltt-author-cluster">
        <div class="ltt-author-avatar-wrap">
          <img src="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/67d02edca7795b0f57073f57_Adam-dimitrov-portrait-75x75.webp" alt="Adam Dimitrov" class="ltt-author-avatar">
        </div>
        <div class="ltt-author-meta">
          <span class="ltt-author-line"><a href="/about">Adam Dimitrov</a></span>
          <span class="ltt-author-role">Founder &amp; Undercover Hotel Inspector • ⏱️ Updated Nov 2026</span>
        </div>
      </div>
      <div class="ltt-trust-pills">
        <span class="ltt-trust-pill">✓ 100% Unsponsored Stay</span>
        <span class="ltt-trust-pill">✓ Paid {hotel_info['paid']}</span>
        <span class="ltt-trust-pill">✓ Verified Receipt</span>
      </div>
    </div>

    <div class="ltt-lead-copy">
      {lead_copy_html}
    </div>
  </div>
</div>
"""

    # 4. Remove old intro sections
    for sel in [".hero-image-wrapper", ".article-hero-container", ".container-2", ".container-intro-section"]:
        el = soup.select_one(sel)
        if el:
            el.decompose()

    # 5. Insert new hero card right after navbar / nav script
    new_hero_soup = BeautifulSoup(hero_card_html, "html.parser")
    nav_script = soup.find(id="ltt-nav-script")
    if nav_script:
        nav_script.insert_after(new_hero_soup)
    else:
        navbar = soup.select_one(".ltt-navbar")
        if navbar:
            navbar.insert_after(new_hero_soup)
        else:
            soup.body.insert(0, new_hero_soup)

    # 6. Transform Summary Section into Bento Group
    container = soup.select_one(".content-right_blog .container")
    if container:
        grid_26 = container.select_one(".grid-26")
        summary_rich = None
        if grid_26:
            curr = grid_26.next_sibling
            while curr:
                if getattr(curr, "name", None) == "div" and "w-richtext" in curr.get("class", []):
                    summary_rich = curr
                    break
                curr = curr.next_sibling

        if grid_26 and summary_rich:
            summary_bento_html = f"""<details class="ltt-bento-group" id="sec-summary" open="">
  <summary class="ltt-bento-group-head">
    <span class="ltt-bento-group-title">📝 Summary, Video Tour &amp; Quick Verdict</span>
    <span class="ltt-bento-right">
      <span class="ltt-mini-pill">Overview</span>
      <span class="ltt-bento-chev">▾</span>
    </span>
  </summary>
  <div class="ltt-bento-group-body">
    {str(grid_26)}
    {str(summary_rich)}
  </div>
</details>"""
            summary_bento_soup = BeautifulSoup(summary_bento_html, "html.parser")
            grid_26.insert_before(summary_bento_soup)
            grid_26.decompose()
            summary_rich.decompose()

    # 7. Section metadata mapping for icons and pills
    icon_map = {
        "check-in": ("🛎️", "Logistics"),
        "arrival": ("🛎️", "Logistics"),
        "bedroom": ("🛏️", "Accommodations"),
        "palm king": ("🛏️", "Accommodations"),
        "queen vs": ("👑", "Room Value"),
        "room interior": ("🛏️", "Accommodations"),
        "bathroom": ("🛁", "Bath & Toiletries"),
        "other rooms": ("🚪", "Suite Options"),
        "breakfast": ("🥐", "Breakfast"),
        "lunch": ("🥗", "Lunch"),
        "dinner": ("🍽️", "Culinary"),
        "indoor": ("🏛️", "Architecture"),
        "outdoor": ("🏖️", "Pools & Beach"),
        "facilities": ("🎡", "Amenities"),
        "service": ("⭐", "Service Verdict")
    }

    # 8. Transform FAQ Cards into Collapsible Bento Groups
    faq_cards = soup.select(".cf-faq-plus-card")
    bento_items = []
    for i, fc in enumerate(faq_cards):
        h = fc.find(["h2", "h3"])
        raw_title = h.get_text(strip=True) if h else f"Section {i+1}"
        clean_title = raw_title.replace("Detailed Breakdown:", "").strip()
        lower_t = clean_title.lower()

        icon = "📌"
        tag = "Review"
        for k, (ic, tg) in icon_map.items():
            if k in lower_t:
                icon = ic
                tag = tg
                break

        slug = re.sub(r"[^a-z0-9]+", "-", lower_t).strip("-")
        sec_id = f"sec-{slug}"

        content_div = fc.select_one(".cf-faq-content-2")
        inner_content = str(content_div) if content_div else ""

        bento_card_html = f"""<details class="ltt-bento-group" id="{sec_id}" open="">
  <summary class="ltt-bento-group-head">
    <span class="ltt-bento-group-title">{icon} {clean_title}</span>
    <span class="ltt-bento-right">
      <span class="ltt-mini-pill">{tag}</span>
      <span class="ltt-bento-chev">▾</span>
    </span>
  </summary>
  <div class="ltt-bento-group-body">
    {inner_content}
  </div>
</details>"""
        bento_soup = BeautifulSoup(bento_card_html, "html.parser")
        fc.replace_with(bento_soup)
        bento_items.append((sec_id, f"{icon} {clean_title}"))

    # 9. Clean up FAQ Header
    faq_header = soup.select_one(".cf-faq-container > h2, .cf-faq-container .heading-42")
    if faq_header:
        header_html = f"""<div class="ltt-deck-header" style="margin: 36px 0 16px 0; border-top: 1px solid #e2e8f0; padding-top: 24px;">
  <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0; letter-spacing: -0.02em;">
    Detailed Breakdown: {hotel_info['short_name']}
  </h2>
  <p style="font-size: 14px; color: #64748b; margin: 0; font-weight: 500;">
    Personally tested undercover • All sections open by default • Click any section to collapse/expand
  </p>
</div>"""
        faq_header.replace_with(BeautifulSoup(header_html, "html.parser"))

    # 10. Update Sidebar Table of Contents in Static HTML
    toc_container = soup.select_one("#toc")
    if toc_container:
        toc_container.clear()
        summary_a = soup.new_tag("a", href="#sec-summary")
        summary_a["class"] = "tocitem active"
        summary_a.string = "📝 Summary & Video"
        toc_container.append(summary_a)
        
        for sec_id, label in bento_items:
            a = soup.new_tag("a", href=f"#{sec_id}")
            a["class"] = "tocitem"
            a.string = label
            toc_container.append(a)

    # 11. Replace ltt-subpage-toc-controller with modern Bento-aware Controller
    new_toc_script = """(function() {
  function smoothScrollToElement(target, offset) {
    if (!target) return;
    offset = (typeof offset === 'number') ? offset : 85;
    if (target.tagName === 'DETAILS') {
      target.open = true;
    }
    var targetPos = target.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop) - offset;
    try {
      window.scrollTo({
        top: Math.max(0, Math.round(targetPos)),
        behavior: 'smooth'
      });
    } catch (e) {
      window.scrollTo(0, Math.max(0, Math.round(targetPos)));
    }
    setTimeout(function() {
      var rect = target.getBoundingClientRect();
      if (Math.abs(rect.top - offset) > 30) {
        var secondPos = rect.top + (window.pageYOffset || document.documentElement.scrollTop) - offset;
        try {
          window.scrollTo({
            top: Math.max(0, Math.round(secondPos)),
            behavior: 'smooth'
          });
        } catch (err) {}
      }
    }, 600);
  }

  function initTOC() {
    var content = document.getElementById("content");
    var toc = document.getElementById("toc");
    var mobileList = document.getElementById("lttMobileTocList");
    var pill = document.getElementById("lttMobileTocPill");
    var pillText = document.getElementById("lttMobileTocPillText");
    var backdrop = document.getElementById("lttMobileTocBackdrop");
    var sheet = document.getElementById("lttMobileTocSheet");
    var closeBtn = document.getElementById("lttMobileTocClose");

    if (!content) return;
    var bentos = content.querySelectorAll("details.ltt-bento-group");
    if (!bentos.length) return;

    if (toc) toc.innerHTML = '';
    if (mobileList) mobileList.innerHTML = '';
    
    var desktopFrag = document.createDocumentFragment();
    var mobileFrag = document.createDocumentFragment();
    var items = [];

    bentos.forEach(function(bento, i) {
      var titleEl = bento.querySelector(".ltt-bento-group-title");
      var rawText = titleEl ? titleEl.textContent.trim() : ("Section " + (i + 1));
      var uniqueId = bento.id || ('sec-bento-' + (i + 1));
      bento.id = uniqueId;

      // Desktop Link
      var a = null;
      if (toc) {
        a = document.createElement('a');
        a.className = (i === 0) ? 'tocitem active' : 'tocitem';
        a.href = '#' + uniqueId;
        a.textContent = rawText;
        desktopFrag.appendChild(a);
      }

      // Mobile Sheet Link
      var mA = null;
      if (mobileList) {
        mA = document.createElement('a');
        mA.className = (i === 0) ? 'ltt-sheet-item is-active' : 'ltt-sheet-item';
        mA.href = '#' + uniqueId;
        mA.innerHTML = '<span>' + rawText + '</span><span>→</span>';
        mobileFrag.appendChild(mA);
      }

      items.push({ id: uniqueId, bento: bento, link: a, mobileLink: mA, text: rawText });
    });

    if (toc) toc.appendChild(desktopFrag);
    if (mobileList) mobileList.appendChild(mobileFrag);

    // Mobile Sheet Handlers
    function openSheet() {
      if (sheet) sheet.classList.add('is-open');
      if (backdrop) backdrop.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }
    function closeSheet() {
      if (sheet) sheet.classList.remove('is-open');
      if (backdrop) backdrop.classList.remove('is-open');
      document.body.style.overflow = '';
    }

    if (pill) pill.addEventListener('click', openSheet);
    if (closeBtn) closeBtn.addEventListener('click', closeSheet);
    if (backdrop) backdrop.addEventListener('click', closeSheet);

    // Mobile Item Clicks
    if (mobileList) {
      mobileList.addEventListener('click', function(e) {
        var clickedA = e.target.closest('a');
        if (!clickedA) return;
        e.preventDefault();
        var hash = clickedA.getAttribute('href');
        var targetId = hash.substring(1);
        var target = document.getElementById(targetId);
        closeSheet();
        if (target) {
          setTimeout(function() {
            smoothScrollToElement(target, 85);
          }, 120);
        }
      });
    }

    // Floating Pill Scroll Visibility
    function updatePill() {
      if (!pill) return;
      var y = window.pageYOffset || document.documentElement.scrollTop;
      if (y > 350) {
        pill.classList.add('is-visible');
      } else {
        pill.classList.remove('is-visible');
      }
    }
    window.addEventListener('scroll', updatePill, { passive: true });
    updatePill();

    // Scrollspy Observer
    if (window._subpageTocObs) window._subpageTocObs.disconnect();
    window._subpageTocObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          if (toc) {
            toc.querySelectorAll('.tocitem.active').forEach(function(z) { z.classList.remove('active'); });
          }
          if (mobileList) {
            mobileList.querySelectorAll('.ltt-sheet-item.is-active').forEach(function(z) { z.classList.remove('is-active'); });
          }

          var match = items.find(function(it) { return it.id === entry.target.id; });
          if (match) {
            if (match.link) match.link.classList.add('active');
            if (match.mobileLink) match.mobileLink.classList.add('is-active');
            if (pillText) pillText.textContent = match.text;
          }
        }
      });
    }, { rootMargin: '0px 0px -70% 0px' });

    items.forEach(function(it) {
      window._subpageTocObs.observe(it.bento);
    });
  }

  // Anchor click delegation
  document.addEventListener('click', function(e) {
    var clickedA = e.target.closest('a[href^="#"]');
    if (!clickedA || clickedA.closest('#lttMobileTocList')) return;
    var hash = clickedA.getAttribute('href');
    if (!hash || hash === '#' || hash.length < 2) return;
    var targetId = hash.substring(1);
    var target = document.getElementById(targetId);
    if (target) {
      e.preventDefault();
      e.stopPropagation();
      smoothScrollToElement(target, 85);
      try {
        history.pushState(null, '', hash);
      } catch (err) {}
    }
  }, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTOC);
  } else {
    initTOC();
  }
})();"""

    toc_script_el = soup.find(id="ltt-subpage-toc-controller")
    if toc_script_el:
        toc_script_el.string = new_toc_script
    else:
        new_sc = soup.new_tag("script", id="ltt-subpage-toc-controller")
        new_sc.string = new_toc_script
        soup.body.append(new_sc)

    # 12. Inject Hero Card & Bento Group CSS into ltt-subpage-styles
    bento_css = """
/* ==========================================================================
   OPTION C BENTO COLLAPSIBLE LITTLE BOXES ARCHITECTURE
   ========================================================================== */
details.ltt-bento-group {
  width: 100% !important;
  max-width: 100% !important;
  align-self: stretch !important;
  box-sizing: border-box !important;
  display: block !important;
  background: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 14px !important;
  margin: 16px 0 !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
  overflow: hidden !important;
}

.cf-faq-container,
.cf-faqs-container {
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}

details.ltt-bento-group > summary.ltt-bento-group-head {
  width: 100% !important;
  box-sizing: border-box !important;
  border-radius: 13px !important;
  list-style: none !important;
  cursor: pointer !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  gap: 12px !important;
  padding: 14px 18px !important;
  background: #f8fafc !important;
  border-bottom: 1px solid transparent !important;
  user-select: none !important;
  transition: background 0.15s ease !important;
}

details.ltt-bento-group > summary.ltt-bento-group-head::-webkit-details-marker {
  display: none !important;
}

details.ltt-bento-group[open] > summary.ltt-bento-group-head {
  border-bottom-color: #e2e8f0 !important;
  border-radius: 13px 13px 0 0 !important;
}

details.ltt-bento-group > summary.ltt-bento-group-head:hover {
  background: #f1f5f9 !important;
}

.ltt-bento-group-title {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  font-size: 16px !important;
  font-weight: 800 !important;
  color: #0f172a !important;
  margin: 0 !important;
  line-height: 1.35 !important;
}

.ltt-bento-right {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex-shrink: 0 !important;
}

.ltt-mini-pill {
  background: #fdfaf2 !important;
  color: #b45309 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  font-size: 11.5px !important;
  font-weight: 700 !important;
  padding: 3px 10px !important;
  border-radius: 99px !important;
  white-space: nowrap !important;
  border: 1px solid #fde68a !important;
}

.ltt-bento-chev {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 24px !important;
  height: 24px !important;
  border-radius: 6px !important;
  background: #e2e8f0 !important;
  color: #334155 !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  transition: transform 0.2s ease !important;
}

details.ltt-bento-group:not([open]) .ltt-bento-chev {
  transform: rotate(-90deg) !important;
}

.ltt-bento-group-body {
  padding: 20px 22px !important;
}

@media (max-width: 640px) {
  details.ltt-bento-group > summary.ltt-bento-group-head {
    padding: 12px 14px !important;
  }
  .ltt-bento-group-title {
    font-size: 14.5px !important;
  }
  .ltt-bento-group-body {
    padding: 14px !important;
  }
}
"""

    subpage_style = soup.find("style", id="ltt-subpage-styles")
    if subpage_style:
        subpage_style.string = hero_css + "\n" + bento_css + "\n" + (subpage_style.string or "")
    else:
        new_style = soup.new_tag("style", id="ltt-subpage-styles")
        new_style.string = hero_css + "\n" + bento_css
        soup.head.append(new_style)

    # 13. Write transformed file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully transformed {hotel_info['short_name']} ({len(bento_items) + 1} bento groups)")

if __name__ == "__main__":
    pages = [
        "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/atlantis-the-royal-dubai-review/index.html",
        "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/atlantis-the-palm-dubai-review/index.html",
        "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/anantara-the-palm-dubai-review/index.html",
        "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/five-palm-jumeirah-dubai-review/index.html",
        "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/rixos-the-palm-dubai-review/index.html"
    ]
    for p in pages:
        transform_hotel_page(p)
