from bs4 import BeautifulSoup
import glob, os

base = "/Users/adamdimitrov/Development/luxurytraveltester"
for p in sorted(glob.glob(base + "/**/*.html", recursive=True)):
    if "test-" in p: continue
    soup = BeautifulSoup(open(p).read(), "html.parser")
    
    dead_elements = soup.select(".hide---but-don-t-delete, [class*=\"hide---\"], .content-left .featured-articles")
    placeholders = soup.select("img[src*=\"placeholder.svg\"]")
    
    if dead_elements or placeholders:
        for el in dead_elements:
            el.decompose()
        for img in placeholders:
            img.decompose()
            
        with open(p, "w", encoding="utf-8") as f:
            f.write(str(soup))
            
        rel = os.path.relpath(p, base)
        print(f"Cleaned {rel}: removed {len(dead_elements)} dead elements, {len(placeholders)} placeholder svgs")
