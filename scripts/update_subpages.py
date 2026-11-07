from bs4 import BeautifulSoup
import os

subpages = [
    "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/anantara-the-palm-dubai-review/index.html",
    "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/atlantis-the-palm-dubai-review/index.html",
    "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/atlantis-the-royal-dubai-review/index.html",
    "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/five-palm-jumeirah-dubai-review/index.html",
    "/Users/adamdimitrov/Development/luxurytraveltester/best-palm-jumeirah-hotels-dubai/rixos-the-palm-dubai-review/index.html",
    "/Users/adamdimitrov/Development/luxurytraveltester/best-desert-safaris-dubai/dubai-desert-safaris-faq/index.html",
    "/Users/adamdimitrov/Development/luxurytraveltester/best-desert-safaris-dubai/itinerary-from-the-city-to-the-desert-in-dubai/index.html"
]

cta_css = """
/* Canonical Pill CTA Standard & Clean UI Fixes */
.main-buy-button,
a.main-buy-button.w-button {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
  color: #ffffff !important;
  font-size: 15px !important;
  font-weight: 800 !important;
  border-radius: 9999px !important;
  padding: 14px 28px !important;
  box-shadow: 0 4px 14px rgba(217, 119, 6, 0.35) !important;
  text-decoration: none !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.main-buy-button:hover,
a.main-buy-button.w-button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(217, 119, 6, 0.45) !important;
}
.st_wrapper, .st_wrapper-2 {
  display: none !important;
}
"""

for path in subpages:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove st_wrapper
    removed = 0
    for el in soup.select(".st_wrapper, .st_wrapper-2"):
        el.decompose()
        removed += 1
        
    # Update style tag
    style_tag = soup.find("style", id="ltt-subpage-styles")
    if style_tag:
        if ".main-buy-button" not in style_tag.string:
            style_tag.string = style_tag.string + "\n" + cta_css
    else:
        new_style = soup.new_tag("style", id="ltt-subpage-styles")
        new_style.string = cta_css
        soup.head.append(new_style)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
        
    name = path.split("/")[-2]
    print(f"Updated {name}: removed {removed} st_wrapper elements")
