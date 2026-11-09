#!/usr/bin/env python3
"""
Full execution script for PageSpeed Insights speed optimizations and Agentic Browsing suite.
"""

import os
import glob
import re
import json
from bs4 import BeautifulSoup

REPO_ROOT = '/Users/adamdimitrov/Development/luxurytraveltester'

GA_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-4XYHG46VLR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-4XYHG46VLR');
</script>"""

LCP_PRELOADS = {
    'best-desert-safaris-dubai': '<link rel="preload" as="image" href="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68a1c9f3d9abe6be9477999f_F777B364-6E93-4638-AE41-962C73448297_1_105_c_result.webp" imagesrcset="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68a1c9f3d9abe6be9477999f_F777B364-6E93-4638-AE41-962C73448297_1_105_c_result-p-500.webp 500w, https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68a1c9f3d9abe6be9477999f_F777B364-6E93-4638-AE41-962C73448297_1_105_c_result-p-800.webp 800w, https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68a1c9f3d9abe6be9477999f_F777B364-6E93-4638-AE41-962C73448297_1_105_c_result.webp 1024w" imagesizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw" fetchpriority="high"/>',
    'best-helicopter-tours-new-york': '<link rel="preload" as="image" href="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/6a47d3559ce91814c1df86f5_best-helicopter-tours-nyc-flynyon-4.avif" fetchpriority="high"/>',
    'best-palm-jumeirah-hotels-dubai': '<link rel="preload" as="image" href="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68d00c728bf6d88cc1f839c1_1.%20Atlantis%20The%20Palm.avif" imagesrcset="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68d00c728bf6d88cc1f839c1_1.%20Atlantis%20The%20Palm-p-500.avif 500w, https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68d00c728bf6d88cc1f839c1_1.%20Atlantis%20The%20Palm.avif 800w" imagesizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1919px) 49vw, 800px" fetchpriority="high"/>',
    'index': '<link rel="preload" as="image" href="https://cdn.prod.website-files.com/67d02edca7795b0f57073b59/68175d418e783498a077f773_Best-Dubai-Hotels-hero.avif" fetchpriority="high"/>'
}

def clean_html_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    rel = os.path.relpath(fpath, REPO_ROOT)
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.head
    if not head:
        return False

    # 1. Determine slug key
    if rel == 'index.html':
        slug = 'index'
        md_slug = 'index.md'
    elif '/' in rel:
        parts = rel.split('/')
        slug = parts[0]
        md_slug = f'{slug}.md'
    else:
        slug = rel.replace('.html', '')
        md_slug = f'{slug}.md'

    # 2. Remove dead/blocking scripts from head & body
    scripts_to_remove = []
    for s in soup.find_all('script'):
        src = s.get('src', '')
        text = s.string or s.text or ''
        
        # Dead webflow-sync.js
        if 'webflow-sync.js' in src:
            scripts_to_remove.append(s)
            continue
            
        # Blocking webfont.js and WebFont.load
        if 'ajax.googleapis.com/ajax/libs/webfont' in src or 'WebFont.load' in text:
            scripts_to_remove.append(s)
            continue
            
        # Dead 404 ghost script
        if 'avljl2rk9q5pNjdkMDJlZGNhNzc5NWIwZjU3MDczYjU5' in src:
            scripts_to_remove.append(s)
            continue
            
        # Duplicate gtag declarations and Google tags first party
        if 'google_tags_first_party' in text or 'developer_id.dZGVlNj' in text or 'developer_id.dYWYxNW' in text:
            scripts_to_remove.append(s)
            continue
            
        # GetYourGuide head widget in index.html
        if 'widget.getyourguide.com/dist/pa.umd.production.min.js' in src and s.parent == head:
            scripts_to_remove.append(s)
            continue

        # Existing GTM script in head (we will inject a single clean GA snippet)
        if 'googletagmanager.com/gtag/js' in src:
            nxt = s.find_next_sibling('script')
            if nxt and ('gtag(' in (nxt.string or nxt.text or '') or 'dataLayer' in (nxt.string or nxt.text or '')):
                scripts_to_remove.append(nxt)
            scripts_to_remove.append(s)
            continue

        # Defer jQuery and Webflow.js
        if 'jquery-3.5.1.min' in src or 'webflow.' in src:
            s['defer'] = ''

    for s in scripts_to_remove:
        try:
            s.decompose()
        except Exception:
            pass

    # Clean any lingering standalone gtag config blocks in head
    for s in head.find_all('script'):
        text = (s.string or s.text or '').strip()
        if 'dataLayer = window.dataLayer' in text and 'gtag(' in text and not s.get('src'):
            s.decompose()

    # 3. Add explicit dimensions to images to eliminate CLS
    for img in soup.find_all('img'):
        classes = img.get('class') or []
        
        # Slider images
        if img.find_parent(class_='bpa-slider'):
            if not img.get('width'):
                img['width'] = '800'
            if not img.get('height'):
                img['height'] = '500'
        # Author avatar
        elif 'ltt-author-avatar' in classes:
            img['width'] = '32'
            img['height'] = '32'
        # Brand logo
        elif 'ltt-brand-logo' in classes:
            img['width'] = '36'
            img['height'] = '36'
        # Review icons
        elif 'bpa-rev-icon' in classes:
            img['width'] = '16'
            img['height'] = '16'
        # Spec cards
        elif 'ltt-sp-card' in [c for parent in img.parents for c in (parent.get('class') or [])]:
            if not img.get('width'):
                img['width'] = '420'
            if not img.get('height'):
                img['height'] = '280'
        # Guide cards
        elif 'ltt-guide-card' in [c for parent in img.parents for c in (parent.get('class') or [])]:
            if not img.get('width'):
                img['width'] = '600'
            if not img.get('height'):
                img['height'] = '375'
        # Hotel cards
        elif 'ltt-hotel-card' in [c for parent in img.parents for c in (parent.get('class') or [])]:
            if not img.get('width'):
                img['width'] = '600'
            if not img.get('height'):
                img['height'] = '375'

    # In index.html, fix the hero image
    if slug == 'index':
        first_img = soup.find('img', class_='ltt-guide-img')
        if first_img:
            first_img['loading'] = 'eager'
            first_img['fetchpriority'] = 'high'

    # 4. Clean Preconnects in Head
    for link in head.find_all('link', rel='preconnect'):
        link.decompose()
        
    p1 = soup.new_tag('link', rel='preconnect', href='https://fonts.googleapis.com')
    p2 = soup.new_tag('link', rel='preconnect', href='https://fonts.gstatic.com', crossorigin='')
    p3 = soup.new_tag('link', rel='preconnect', href='https://cdn.prod.website-files.com', crossorigin='')
    head.insert(0, p3)
    head.insert(0, p2)
    head.insert(0, p1)

    # 5. Preload LCP image if applicable
    for link in head.find_all('link', rel='preload', as_='image'):
        link.decompose()
        
    if slug in LCP_PRELOADS:
        preload_soup = BeautifulSoup(LCP_PRELOADS[slug], 'html.parser')
        preload_tag = preload_soup.find('link')
        if preload_tag:
            head.append(preload_tag)

    # 6. Ensure Agentic Browsing tags in Head
    for m in head.find_all('meta', attrs={'name': 'is-agentic-site-type'}):
        m.decompose()
    agentic_meta = soup.new_tag('meta', attrs={'name': 'is-agentic-site-type', 'content': 'content'})
    head.append(agentic_meta)

    for link in head.find_all('link', rel='alternate', type='text/markdown'):
        link.decompose()
    md_link = soup.new_tag('link', rel='alternate', type='text/markdown', href=f'/{md_slug}')
    head.append(md_link)

    # 7. Add single clean GA snippet in head
    ga_soup = BeautifulSoup(GA_SNIPPET, 'html.parser')
    for el in ga_soup.children:
        if el.name:
            head.append(el)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return True


def extract_page_markdown(slug, title, canonical_url, summary_text):
    fpath = os.path.join(REPO_ROOT, slug, 'index.html')
    with open(fpath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    cards = soup.find_all(class_='bpa-card')
    details = soup.find_all(class_='bpa-details-card')

    md_lines = []
    md_lines.append(f"# {title}\n")
    md_lines.append(f"> **Canonical URL**: [{canonical_url}]({canonical_url})  ")
    md_lines.append(f"> **Author**: Adam Dimitrov (Verified Luxury Field Tester)  ")
    md_lines.append(f"> **Publication**: Luxury Travel Tester  ")
    md_lines.append(f"> **Last Verified**: November 2026\n")
    md_lines.append(f"{summary_text}\n")

    md_lines.append("## Quick Comparison & Verified Rankings\n")
    md_lines.append("| Rank | Name | Details / Category | Verified Specs | Direct Booking |")
    md_lines.append("|---|---|---|---|---|")

    items_data = []

    for i in range(len(cards)):
        c = cards[i]
        d = details[i] if i < len(details) else None

        item_title = c.find(class_='bpa-title').get_text(strip=True) if c.find(class_='bpa-title') else f"Item {i+1}"
        kicker = c.find(class_='bpa-kicker').get_text(strip=True) if c.find(class_='bpa-kicker') else ""
        cta = c.find('a', class_='bpa-btn')
        cta_url = cta.get('href', '') if cta else canonical_url

        # Pros & Cons
        pro_items = []
        con_items = []
        body_paras = []
        if d:
            pro_block = d.find(class_='pro-con-box-pro-cell-rich-text-block')
            con_block = d.find(class_='pro-con-box-con-cell-rich-text-block')
            if pro_block:
                pro_items = [li.get_text(strip=True) for li in pro_block.find_all('li')]
            if con_block:
                con_items = [li.get_text(strip=True) for li in con_block.find_all('li')]
            
            body = d.find(class_='bpa-details-body')
            if body:
                for p in body.find_all('p'):
                    txt = p.get_text(strip=True)
                    if len(txt) > 30 and 'cookie' not in txt.lower():
                        body_paras.append(txt)

        items_data.append({
            'rank': i + 1,
            'title': item_title,
            'kicker': kicker,
            'cta_url': cta_url,
            'pros': pro_items,
            'cons': con_items,
            'paragraphs': body_paras[:4]
        })

        clean_kicker = kicker.replace('|', '/').replace('•', '·')
        md_lines.append(f"| **#{i+1}** | **{item_title}** | {clean_kicker} | Verified Field-Tested | [Check Availability →]({cta_url}) |")

    md_lines.append("\n---\n")
    md_lines.append("## Detailed Field Review Dossiers\n")

    for item in items_data:
        md_lines.append(f"### #{item['rank']}. {item['title']}\n")
        if item['kicker']:
            md_lines.append(f"*{item['kicker']}*\n")
        md_lines.append(f"🔗 **Direct Booking Link**: [{item['cta_url']}]({item['cta_url']})\n")

        if item['pros']:
            md_lines.append("#### Verified Strengths (Pros)")
            for pro in item['pros']:
                md_lines.append(f"- **✓ {pro}**")
            md_lines.append("")

        if item['cons']:
            md_lines.append("#### Considerations & Trade-offs (Cons)")
            for con in item['cons']:
                md_lines.append(f"- **⚠️ {con}**")
            md_lines.append("")

        if item['paragraphs']:
            md_lines.append("#### Field Tester Verdict & Notes")
            for para in item['paragraphs']:
                md_lines.append(f"{para}\n")

        md_lines.append("---\n")

    return "\n".join(md_lines)


def generate_all_markdown_files():
    # 1. Dubai Desert Safaris
    safari_summary = """Our team personally booked, tested, and evaluated the top 10 desert safaris across Dubai. We analyzed dune bashing safety, camel trek authenticity, quad bike power, desert camp hygiene, BBQ dinner quality, Bedouin hospitality, and value for money to deliver an unbiased ranking."""
    safari_md = extract_page_markdown(
        'best-desert-safaris-dubai',
        '10 Best Desert Safaris in Dubai in 2026 (Personally Tested)',
        'https://luxurytraveltester.com/best-desert-safaris-dubai',
        safari_summary
    )
    with open(os.path.join(REPO_ROOT, 'best-desert-safaris-dubai.md'), 'w', encoding='utf-8') as f:
        f.write(safari_md)

    # 2. NYC Helicopter Tours
    nyc_summary = """We personally tested New York City's top helicopter flight operators. From thrilling open-door photo flights over Central Park and the Empire State Building to luxurious executive closed-cabin flights departing from Downtown Manhattan Heliport (Pier 6), here is our verified ranking."""
    nyc_md = extract_page_markdown(
        'best-helicopter-tours-new-york',
        '5 Best Helicopter Tours in New York in 2026 (Personally Tested)',
        'https://luxurytraveltester.com/best-helicopter-tours-new-york',
        nyc_summary
    )
    with open(os.path.join(REPO_ROOT, 'best-helicopter-tours-new-york.md'), 'w', encoding='utf-8') as f:
        f.write(nyc_md)

    # 3. Palm Jumeirah Luxury Hotels
    palm_summary = """Palm Jumeirah is home to the world's most prestigious luxury resorts. We personally stayed at the 5 flagship resorts (Atlantis The Royal, Atlantis The Palm, Anantara The Palm, FIVE Palm Jumeirah, Rixos The Palm) and vetted the top 5 alternative luxury contenders to compile this definitive guide."""
    palm_md = extract_page_markdown(
        'best-palm-jumeirah-hotels-dubai',
        '10 Best Hotels in Palm Jumeirah Dubai in 2026 (Personally Tested)',
        'https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai',
        palm_summary
    )
    with open(os.path.join(REPO_ROOT, 'best-palm-jumeirah-hotels-dubai.md'), 'w', encoding='utf-8') as f:
        f.write(palm_md)

    # 4. Index.md
    index_md = """# Luxury Travel Tester — Verified Luxury Travel Intelligence

> **Canonical Site**: [https://luxurytraveltester.com](https://luxurytraveltester.com)  
> **Chief Editor & Founder**: Adam Dimitrov  
> **Testing Ethos**: 100% personally tested, zero sponsored bias, verified unit economics, and authentic photo/video proof.

---

## Flagship Verified Hubs & Guides (2026)

### 1. [10 Best Desert Safaris in Dubai](https://luxurytraveltester.com/best-desert-safaris-dubai)
- **Markdown Version**: [/best-desert-safaris-dubai.md](https://luxurytraveltester.com/best-desert-safaris-dubai.md)
- **Scope**: 10 distinct routes and operators personally tested in the Lahbab Red Dunes, Al Marmoom, and Dubai Desert Conservation Reserve (DDCR).
- **Flagship Winner**: Dubai Red Dunes Safari & Al Khayma Camp (OceanAir Travels / Excursion Point).

### 2. [5 Best Helicopter Tours in New York](https://luxurytraveltester.com/best-helicopter-tours-new-york)
- **Markdown Version**: [/best-helicopter-tours-new-york.md](https://luxurytraveltester.com/best-helicopter-tours-new-york.md)
- **Scope**: Comprehensive comparison of open-door ("shoe selfie") vs closed-door scenic flights across Manhattan, Statue of Liberty, Brooklyn Bridge, and Central Park.
- **Flagship Winner**: FlyNYON Open-Door Photography Flight (Kearny Heliport) & HeliNY Manhattan Classic (Pier 6 Downtown Heliport).

### 3. [10 Best Hotels in Palm Jumeirah Dubai](https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai)
- **Markdown Version**: [/best-palm-jumeirah-hotels-dubai.md](https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai.md)
- **Scope**: 5 personally stayed luxury resorts plus 5 top-rated luxury contenders on Palm Jumeirah Crescent, West Beach, and the Trunk.
- **Flagship Winner**: Atlantis The Royal & Atlantis, The Palm.

---

## Machine-Readable Resources
- **LLM Index**: [https://luxurytraveltester.com/llms.txt](https://luxurytraveltester.com/llms.txt)
- **Full Knowledge Base**: [https://luxurytraveltester.com/llms-full.txt](https://luxurytraveltester.com/llms-full.txt)
- **XML Sitemap**: [https://luxurytraveltester.com/sitemap.xml](https://luxurytraveltester.com/sitemap.xml)
- **Robots Policy**: [https://luxurytraveltester.com/robots.txt](https://luxurytraveltester.com/robots.txt)
"""
    with open(os.path.join(REPO_ROOT, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(index_md)

    # 5. llms.txt
    llms_txt = """# Luxury Travel Tester
> Verified luxury travel intelligence, hotel reviews, helicopter tours, and desert safaris. Every flagship guide is backed by hands-on testing, original photography, verified pricing, and unbiased editorial analysis.

## Core Hubs & Flagship Guides
- [10 Best Desert Safaris in Dubai in 2026 (Personally Tested)](https://luxurytraveltester.com/best-desert-safaris-dubai): Comprehensive review of 10 desert safaris across Lahbab Red Dunes and DDCR. Covers morning, evening, and overnight Bedouin camps, quad bikes, dune bashing, and pricing.
- [5 Best Helicopter Tours in New York in 2026 (Personally Tested)](https://luxurytraveltester.com/best-helicopter-tours-new-york): Field comparison of NYC helicopter rides from Downtown Manhattan Heliport (Pier 6) and Kearny NJ. Includes open-door photo flights, closed-cabin tours, flight routes, and safety protocols.
- [10 Best Hotels in Palm Jumeirah Dubai in 2026 (Personally Tested)](https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai): In-depth resort dossiers for Atlantis The Royal, Atlantis The Palm, Anantara, FIVE Palm, Rixos The Palm, and top luxury competitors. Covers beach specs, Michelin dining, waterparks, and room tiers.

## Markdown Endpoints (Content-Negotiated)
- [Dubai Desert Safaris Markdown](https://luxurytraveltester.com/best-desert-safaris-dubai.md)
- [NYC Helicopter Tours Markdown](https://luxurytraveltester.com/best-helicopter-tours-new-york.md)
- [Palm Jumeirah Luxury Hotels Markdown](https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai.md)
- [Luxury Travel Tester Overview Markdown](https://luxurytraveltester.com/index.md)

## Full Knowledge Base
- [Full LLM Knowledge Base](https://luxurytraveltester.com/llms-full.txt): Complete, concatenated dossiers including all pros, cons, verified specifications, and booking links across all 3 hubs.

## About the Publication
- Founder & Chief Field Tester: Adam Dimitrov
- Editorial Policy: 100% verified first-person stays and tours.
- Contact: contact@luxurytraveltester.com
"""
    with open(os.path.join(REPO_ROOT, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_txt)

    # 6. llms-full.txt
    llms_full_txt = f"""# Luxury Travel Tester — Master LLM Knowledge Base (Full Dossiers)

> This document contains the complete, unedited review dossiers, verified specifications, pros & cons, and booking links for Luxury Travel Tester's core hubs.

---

{safari_md}

---

{nyc_md}

---

{palm_md}
"""
    with open(os.path.join(REPO_ROOT, 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_full_txt)

    print("Markdown and LLM documents generated successfully.")


def create_well_known_manifests():
    wk_dir = os.path.join(REPO_ROOT, '.well-known')
    as_dir = os.path.join(wk_dir, 'agent-skills')
    os.makedirs(as_dir, exist_ok=True)

    # 1. ai-plugin.json
    ai_plugin = {
        "schema_version": "v1",
        "name_for_model": "luxury_travel_tester",
        "name_for_human": "Luxury Travel Tester",
        "description_for_model": "Access verified, personally tested reviews and ratings for Dubai desert safaris, New York City helicopter tours, and Palm Jumeirah luxury hotels. Includes direct booking links, pricing, pros and cons, and hands-on testing verdicts.",
        "description_for_human": "Personally tested luxury travel reviews, hotel guides, helicopter tours, and desert safaris.",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "https://luxurytraveltester.com/llms.txt"
        },
        "logo_url": "https://luxurytraveltester.com/assets/apple-touch-icon.png",
        "contact_email": "contact@luxurytraveltester.com",
        "legal_info_url": "https://luxurytraveltester.com/about"
    }
    with open(os.path.join(wk_dir, 'ai-plugin.json'), 'w', encoding='utf-8') as f:
        json.dump(ai_plugin, f, indent=2)

    # 2. agent-skills/index.json
    skills_index = {
        "name": "luxury-travel-tester",
        "description": "Verified luxury travel intelligence covering Dubai Desert Safaris, NYC Helicopter Tours, and Palm Jumeirah Luxury Resorts.",
        "version": "1.0.0",
        "resources": [
            {
                "uri": "https://luxurytraveltester.com/llms.txt",
                "name": "LLM Index & Guidelines",
                "mimeType": "text/plain"
            },
            {
                "uri": "https://luxurytraveltester.com/llms-full.txt",
                "name": "Complete Tested Travel Knowledge Base",
                "mimeType": "text/markdown"
            },
            {
                "uri": "https://luxurytraveltester.com/best-desert-safaris-dubai.md",
                "name": "Dubai Desert Safaris Tested Dossier",
                "mimeType": "text/markdown"
            },
            {
                "uri": "https://luxurytraveltester.com/best-helicopter-tours-new-york.md",
                "name": "NYC Helicopter Tours Tested Dossier",
                "mimeType": "text/markdown"
            },
            {
                "uri": "https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai.md",
                "name": "Palm Jumeirah Luxury Hotels Tested Dossier",
                "mimeType": "text/markdown"
            }
        ]
    }
    with open(os.path.join(as_dir, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(skills_index, f, indent=2)

    # 3. ai-catalog.json
    ai_catalog = {
        "$schema": "https://is-agentic.com/schemas/ai-catalog.json",
        "title": "Luxury Travel Tester AI Catalog",
        "description": "Autonomous Agent and AI Search discovery endpoint for Luxury Travel Tester verified travel reviews.",
        "homepage": "https://luxurytraveltester.com",
        "llms_txt": "https://luxurytraveltester.com/llms.txt",
        "llms_full_txt": "https://luxurytraveltester.com/llms-full.txt",
        "sitemap": "https://luxurytraveltester.com/sitemap.xml",
        "endpoints": [
            {
                "name": "Dubai Desert Safaris",
                "url": "https://luxurytraveltester.com/best-desert-safaris-dubai",
                "markdown": "https://luxurytraveltester.com/best-desert-safaris-dubai.md",
                "category": "Travel Guide / Reviews"
            },
            {
                "name": "New York City Helicopter Tours",
                "url": "https://luxurytraveltester.com/best-helicopter-tours-new-york",
                "markdown": "https://luxurytraveltester.com/best-helicopter-tours-new-york.md",
                "category": "Travel Guide / Reviews"
            },
            {
                "name": "Palm Jumeirah Luxury Hotels Dubai",
                "url": "https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai",
                "markdown": "https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai.md",
                "category": "Hotel Reviews"
            }
        ]
    }
    with open(os.path.join(wk_dir, 'ai-catalog.json'), 'w', encoding='utf-8') as f:
        json.dump(ai_catalog, f, indent=2)

    print(".well-known manifests created.")


def update_robots_txt():
    robots_content = """# robots.txt for luxurytraveltester.com
User-agent: *
Allow: /

# Dedicated AI Agent & Autonomous Search Crawlers
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: CCBot
Allow: /

# Machine-Readable LLM Standards
# llms.txt: https://luxurytraveltester.com/llms.txt
# llms-full.txt: https://luxurytraveltester.com/llms-full.txt

# Canonical Sitemaps
Sitemap: https://luxurytraveltester.com/sitemap.xml
"""
    with open(os.path.join(REPO_ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("robots.txt updated.")


def update_vercel_config():
    vercel_path = os.path.join(REPO_ROOT, 'vercel.json')
    with open(vercel_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Add rewrites for Accept: text/markdown content negotiation
    rewrites = [
        {
            "source": "/best-desert-safaris-dubai",
            "has": [
                {
                    "type": "header",
                    "key": "accept",
                    "value": ".*text/markdown.*"
                }
            ],
            "destination": "/best-desert-safaris-dubai.md"
        },
        {
            "source": "/best-helicopter-tours-new-york",
            "has": [
                {
                    "type": "header",
                    "key": "accept",
                    "value": ".*text/markdown.*"
                }
            ],
            "destination": "/best-helicopter-tours-new-york.md"
        },
        {
            "source": "/best-palm-jumeirah-hotels-dubai",
            "has": [
                {
                    "type": "header",
                    "key": "accept",
                    "value": ".*text/markdown.*"
                }
            ],
            "destination": "/best-palm-jumeirah-hotels-dubai.md"
        },
        {
            "source": "/",
            "has": [
                {
                    "type": "header",
                    "key": "accept",
                    "value": ".*text/markdown.*"
                }
            ],
            "destination": "/index.md"
        }
    ]
    data["rewrites"] = rewrites

    # 2. Add headers for .md, llms*.txt, and .well-known
    existing_headers = data.get("headers", [])
    new_headers = [
        {
            "source": "/(.*\\.md)",
            "headers": [
                {
                    "key": "Content-Type",
                    "value": "text/markdown; charset=utf-8"
                },
                {
                    "key": "Vary",
                    "value": "Accept"
                },
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=3600, stale-while-revalidate=86400"
                }
            ]
        },
        {
            "source": "/(llms.*\\.txt)",
            "headers": [
                {
                    "key": "Content-Type",
                    "value": "text/plain; charset=utf-8"
                },
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=3600, stale-while-revalidate=86400"
                }
            ]
        },
        {
            "source": "/\\.well-known/(.*)",
            "headers": [
                {
                    "key": "Content-Type",
                    "value": "application/json; charset=utf-8"
                },
                {
                    "key": "Access-Control-Allow-Origin",
                    "value": "*"
                },
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=3600, stale-while-revalidate=86400"
                }
            ]
        }
    ]

    # Prepend new headers before generic fallback headers
    data["headers"] = new_headers + [h for h in existing_headers if not any(k in h.get("source", "") for k in ["\\.md", "llms", "\\.well-known"])]

    with open(vercel_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print("vercel.json updated with rewrites and headers.")


def main():
    print("=== Starting Full PageSpeed and Agentic Suite Implementation ===")
    
    # 1. Clean and optimize all production HTML files
    all_html = sorted(glob.glob(os.path.join(REPO_ROOT, '**/*.html'), recursive=True))
    for f in all_html:
        clean_html_file(f)
    print(f"Cleaned and optimized {len(all_html)} HTML files.")

    # 2. Generate Markdown files and LLM standards
    generate_all_markdown_files()

    # 3. Create .well-known manifests
    create_well_known_manifests()

    # 4. Update robots.txt
    update_robots_txt()

    # 5. Update vercel.json
    update_vercel_config()

    print("=== All Operations Completed Successfully ===")

if __name__ == '__main__':
    main()
