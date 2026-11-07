import re
import os
import glob
from bs4 import BeautifulSoup

# 1. Read canonical Cruise Detective nav CSS
nav_css_path = "/Users/adamdimitrov/.gemini/config/skills/luxury-editorial-system/resources/ltt-nav-styles.css"
with open(nav_css_path, "r", encoding="utf-8") as f:
    nav_css = f.read()

# Customize colors for LTT (gold/amber accents instead of yellow-gold where applicable)
# Note: LTT brand emblem has #dfa732 / #785208, matching Cruise Detective style perfectly!

nav_script_content = """/* ==========================================================================
   LUXURY EDITORIAL SYSTEM — MODERN VANILLA NAVIGATION CONTROLLER
   Zero-dependency, semantic, responsive, WCAG-compliant (Desktop & Mobile)
   ========================================================================== */
(function() {
  function initNav() {
    var toggle = document.getElementById('lttNavToggle');
    var drawer = document.getElementById('lttMobileDrawer');
    var dropdown = document.getElementById('lttDestinationsDropdown') || document.getElementById('lttExploreDropdown');
    var dropBtn = dropdown ? dropdown.querySelector('.ltt-dropdown-btn') : null;

    if (toggle && drawer && !toggle._bound) {
      toggle._bound = true;
      toggle.addEventListener('click', function(e) {
        e.stopPropagation();
        var isOpen = drawer.classList.contains('is-open');
        if (isOpen) {
          drawer.classList.remove('is-open');
          toggle.classList.remove('is-active');
          toggle.setAttribute('aria-expanded', 'false');
          drawer.setAttribute('aria-hidden', 'true');
        } else {
          drawer.classList.add('is-open');
          toggle.classList.add('is-active');
          toggle.setAttribute('aria-expanded', 'true');
          drawer.setAttribute('aria-hidden', 'false');
        }
      });

      drawer.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
          drawer.classList.remove('is-open');
          toggle.classList.remove('is-active');
          toggle.setAttribute('aria-expanded', 'false');
          drawer.setAttribute('aria-hidden', 'true');
        });
      });
    }

    if (dropdown && !dropdown._bound) {
      dropdown._bound = true;
      var closeTimeout = null;

      function openMenu() {
        if (closeTimeout) {
          clearTimeout(closeTimeout);
          closeTimeout = null;
        }
        dropdown.classList.add('is-open');
        if (dropBtn) dropBtn.setAttribute('aria-expanded', 'true');
      }

      function closeMenuWithGrace(delay) {
        if (closeTimeout) clearTimeout(closeTimeout);
        closeTimeout = setTimeout(function() {
          dropdown.classList.remove('is-open');
          if (dropBtn) dropBtn.setAttribute('aria-expanded', 'false');
        }, delay !== undefined ? delay : 350);
      }

      dropdown.addEventListener('mouseenter', openMenu);
      dropdown.addEventListener('mouseleave', function() {
        closeMenuWithGrace(350);
      });

      if (dropBtn) {
        dropBtn.addEventListener('click', function(e) {
          e.stopPropagation();
          if (dropdown.classList.contains('is-open')) {
            closeMenuWithGrace(0);
          } else {
            openMenu();
          }
        });
      }

      document.addEventListener('click', function(e) {
        if (dropdown.classList.contains('is-open') && !dropdown.contains(e.target)) {
          closeMenuWithGrace(0);
        }
        if (drawer && drawer.classList.contains('is-open') && !drawer.contains(e.target) && (!toggle || !toggle.contains(e.target))) {
          drawer.classList.remove('is-open');
          if (toggle) {
            toggle.classList.remove('is-active');
            toggle.setAttribute('aria-expanded', 'false');
          }
          drawer.setAttribute('aria-hidden', 'true');
        }
      });

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          if (drawer && drawer.classList.contains('is-open')) {
            drawer.classList.remove('is-open');
            if (toggle) {
              toggle.classList.remove('is-active');
              toggle.setAttribute('aria-expanded', 'false');
            }
            drawer.setAttribute('aria-hidden', 'true');
          }
          if (dropdown && dropdown.classList.contains('is-open')) {
            dropdown.classList.remove('is-open');
            if (dropBtn) dropBtn.setAttribute('aria-expanded', 'false');
          }
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNav);
  } else {
    initNav();
  }
  window.addEventListener('load', initNav);
})();"""

def build_navbar_html(current_page_slug):
    # Determine active classes
    is_safari = "best-desert-safaris-dubai" in current_page_slug
    is_palm = "best-palm-jumeirah-hotels-dubai" in current_page_slug
    is_nyc = "best-helicopter-tours-new-york" in current_page_slug
    is_about = "about" in current_page_slug
    is_contact = "contact" in current_page_slug

    safari_active = ' aria-current="page" class="ltt-nav-link active"' if is_safari and not ("review" in current_page_slug or "faq" in current_page_slug or "itinerary" in current_page_slug) else ' class="ltt-nav-link"'
    palm_active = ' aria-current="page" class="ltt-nav-link active"' if is_palm and not ("review" in current_page_slug) else ' class="ltt-nav-link"'
    nyc_active = ' aria-current="page" class="ltt-nav-link active"' if is_nyc else ' class="ltt-nav-link"'
    about_active = ' aria-current="page" class="ltt-nav-link active"' if is_about else ' class="ltt-nav-link"'
    contact_active = ' aria-current="page" class="ltt-nav-link active"' if is_contact else ' class="ltt-nav-link"'

    mega_safari_active = ' aria-current="page" class="ltt-mega-item active"' if is_safari else ' class="ltt-mega-item"'
    mega_palm_active = ' aria-current="page" class="ltt-mega-item active"' if is_palm else ' class="ltt-mega-item"'
    mega_nyc_active = ' aria-current="page" class="ltt-mega-item active"' if is_nyc else ' class="ltt-mega-item"'

    html = f"""<header class="ltt-navbar" role="banner">
  <div class="ltt-nav-inner">
    <a href="/" class="ltt-brand" aria-label="Luxury Travel Tester Homepage">
      <span class="ltt-brand-emblem">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
        </svg>
      </span>
      <span class="ltt-brand-text">LUXURY TRAVEL TESTER</span>
    </a>
    <nav class="ltt-nav-links" aria-label="Primary Navigation">
      <div class="ltt-nav-dropdown" id="lttDestinationsDropdown">
        <button type="button" class="ltt-nav-link ltt-dropdown-btn" aria-haspopup="true" aria-expanded="false">
          <span>Destinations</span>
          <svg class="ltt-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
        <div class="ltt-mega-menu" role="menu">
          <div class="ltt-mega-col">
            <div class="ltt-mega-head">DUBAI &amp; UAE</div>
            <a href="/best-desert-safaris-dubai"{mega_safari_active}>
              <span class="ltt-mega-icon">🏜️</span>
              <div>
                <strong>Dubai Desert Safaris</strong>
                <p>10 tested camps, dune bashing &amp; VIP suites</p>
              </div>
            </a>
            <a href="/best-palm-jumeirah-hotels-dubai"{mega_palm_active}>
              <span class="ltt-mega-icon">🏨</span>
              <div>
                <strong>Dubai Palm Hotels</strong>
                <p>10 luxury resorts &amp; private beach reviews</p>
              </div>
            </a>
          </div>
          <div class="ltt-mega-col">
            <div class="ltt-mega-head">UNITED STATES &amp; REVIEWS</div>
            <a href="/best-helicopter-tours-new-york"{mega_nyc_active}>
              <span class="ltt-mega-icon">🚁</span>
              <div>
                <strong>NYC Helicopter Tours</strong>
                <p>Doors-off shoe selfie &amp; skyline routes</p>
              </div>
            </a>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #f1f5f9;">
              <a href="/best-palm-jumeirah-hotels-dubai/atlantis-the-royal-dubai-review" class="ltt-mega-subitem">Atlantis The Royal Review</a>
              <a href="/best-palm-jumeirah-hotels-dubai/atlantis-the-palm-dubai-review" class="ltt-mega-subitem">Atlantis The Palm Review</a>
              <a href="/best-palm-jumeirah-hotels-dubai/anantara-the-palm-dubai-review" class="ltt-mega-subitem">Anantara The Palm Review</a>
            </div>
          </div>
        </div>
      </div>
      <a href="/best-desert-safaris-dubai"{safari_active}>Desert Safaris</a>
      <a href="/best-palm-jumeirah-hotels-dubai"{palm_active}>Palm Hotels</a>
      <a href="/best-helicopter-tours-new-york"{nyc_active}>NYC Helicopters</a>
      <a href="/about"{about_active}>About</a>
      <a href="/contact"{contact_active}>Contact</a>
    </nav>
    <div class="ltt-nav-right">
      <button type="button" class="ltt-hamburger" id="lttNavToggle" aria-label="Toggle Menu" aria-controls="lttMobileDrawer" aria-expanded="false">
        <span class="ltt-hamburger-bar"></span>
        <span class="ltt-hamburger-bar"></span>
        <span class="ltt-hamburger-bar"></span>
      </button>
    </div>
  </div>
  <div class="ltt-mobile-drawer" id="lttMobileDrawer" aria-hidden="true">
    <div class="ltt-drawer-content">
      <div class="ltt-mobile-section">
        <div class="ltt-mobile-label">Destinations &amp; Guides</div>
        <a href="/best-desert-safaris-dubai" class="ltt-mobile-link">
          <span>🏜️ Dubai Desert Safaris</span>
          <span style="font-size:10px; font-weight:800; background:#d97706; color:#fff; padding:2px 7px; border-radius:9999px;">TOP PICK</span>
        </a>
        <a href="/best-palm-jumeirah-hotels-dubai" class="ltt-mobile-link">
          <span>🏨 Dubai Palm Hotels</span>
        </a>
        <a href="/best-helicopter-tours-new-york" class="ltt-mobile-link">
          <span>🚁 NYC Helicopter Tours</span>
        </a>
      </div>
      <div class="ltt-mobile-section">
        <div class="ltt-mobile-label">Featured Hotel Reviews</div>
        <a href="/best-palm-jumeirah-hotels-dubai/atlantis-the-royal-dubai-review" class="ltt-mobile-link">
          <span>👑 Atlantis The Royal</span>
        </a>
        <a href="/best-palm-jumeirah-hotels-dubai/atlantis-the-palm-dubai-review" class="ltt-mobile-link">
          <span>🌊 Atlantis The Palm</span>
        </a>
        <a href="/best-palm-jumeirah-hotels-dubai/anantara-the-palm-dubai-review" class="ltt-mobile-link">
          <span>🌿 Anantara The Palm</span>
        </a>
        <a href="/best-palm-jumeirah-hotels-dubai/five-palm-jumeirah-dubai-review" class="ltt-mobile-link">
          <span>🍸 FIVE Palm Jumeirah</span>
        </a>
        <a href="/best-palm-jumeirah-hotels-dubai/rixos-the-palm-dubai-review" class="ltt-mobile-link">
          <span>🏖️ Rixos The Palm</span>
        </a>
      </div>
      <div class="ltt-mobile-section">
        <div class="ltt-mobile-label">Editorial</div>
        <a href="/about" class="ltt-mobile-link">
          <span>📖 About &amp; Testing Standards</span>
        </a>
        <a href="/contact" class="ltt-mobile-link">
          <span>✉️ Contact Editorial Desk</span>
        </a>
      </div>
    </div>
  </div>
</header>
"""
    return html

def apply_nav_to_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    # 1. Replace or insert style#ltt-nav-styles
    style_el = soup.find("style", id="ltt-nav-styles")
    if style_el:
        style_el.string = nav_css
    else:
        new_s = soup.new_tag("style", id="ltt-nav-styles")
        new_s.string = nav_css
        soup.head.append(new_s)

    # 2. Build new navbar
    new_nav_html = build_navbar_html(path)
    new_nav_soup = BeautifulSoup(new_nav_html, "html.parser")

    old_nav = soup.select_one(".ltt-navbar, header")
    if old_nav:
        old_nav.replace_with(new_nav_soup)
    else:
        soup.body.insert(0, new_nav_soup)

    # 3. Replace or insert script#ltt-nav-script
    old_script = soup.find("script", id="ltt-nav-script")
    if old_script:
        old_script.string = nav_script_content
    else:
        new_sc = soup.new_tag("script", id="ltt-nav-script")
        new_sc.string = nav_script_content
        # place right after header
        nav_in_doc = soup.select_one(".ltt-navbar")
        if nav_in_doc:
            nav_in_doc.insert_after(new_sc)
        else:
            soup.body.append(new_sc)

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    rel = os.path.relpath(path, "/Users/adamdimitrov/Development/luxurytraveltester")
    print(f"Updated navbar on {rel}")

if __name__ == "__main__":
    base = "/Users/adamdimitrov/Development/luxurytraveltester"
    pages = sorted(glob.glob(base + "/**/*.html", recursive=True))
    for p in pages:
        if "test-" in p: continue
        apply_nav_to_file(p)
