#!/usr/bin/env python3
"""
Fix accessibility landmarks, ARD schema, iframe titles, and slider focusability.
"""

import os
import glob
import json
from bs4 import BeautifulSoup

REPO_ROOT = '/Users/adamdimitrov/Development/luxurytraveltester'

# 1. Update .well-known/ard.json and .well-known/ai-catalog.json
clean_catalog = {
  "specVersion": "1.0",
  "entries": [
    {
      "identifier": "urn:air:luxurytraveltester.com:travel:safaris",
      "type": "text/markdown",
      "url": "https://luxurytraveltester.com/best-desert-safaris-dubai.md"
    },
    {
      "identifier": "urn:air:luxurytraveltester.com:travel:helicopters",
      "type": "text/markdown",
      "url": "https://luxurytraveltester.com/best-helicopter-tours-new-york.md"
    },
    {
      "identifier": "urn:air:luxurytraveltester.com:travel:hotels",
      "type": "text/markdown",
      "url": "https://luxurytraveltester.com/best-palm-jumeirah-hotels-dubai.md"
    },
    {
      "identifier": "urn:air:luxurytraveltester.com:travel:knowledge-base",
      "type": "text/markdown",
      "url": "https://luxurytraveltester.com/llms-full.txt"
    },
    {
      "identifier": "urn:air:luxurytraveltester.com:travel:guidelines",
      "type": "text/plain",
      "url": "https://luxurytraveltester.com/llms.txt"
    }
  ]
}

with open(os.path.join(REPO_ROOT, '.well-known', 'ard.json'), 'w', encoding='utf-8') as f:
    json.dump(clean_catalog, f, indent=2)

with open(os.path.join(REPO_ROOT, '.well-known', 'ai-catalog.json'), 'w', encoding='utf-8') as f:
    json.dump(clean_catalog, f, indent=2)

print("Updated ard.json and ai-catalog.json with canonical specVersion 1.0.")

# 2. Update HTML files for accessibility landmarks, iframe titles, slider tabindex, and link tags
all_html = sorted(glob.glob(os.path.join(REPO_ROOT, '**/*.html'), recursive=True))

for fpath in all_html:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    head = soup.head
    body = soup.body
    if not head or not body:
        continue

    # Ensure link rel="ai-catalog" and rel="ard" in head
    for l in head.find_all('link', rel=lambda r: r and ('ai-catalog' in r or 'ard' in r)):
        l.decompose()
    l_ard = soup.new_tag('link', rel='ard', href='/.well-known/ard.json')
    l_cat = soup.new_tag('link', rel='ai-catalog', href='/.well-known/ai-catalog.json')
    head.append(l_ard)
    head.append(l_cat)

    # Iframe accessible titles
    for iframe in body.find_all('iframe'):
        if not iframe.get('title'):
            iframe['title'] = 'Interactive Map Location'

    # Slider focusable for screen readers
    for slider in body.find_all(class_='bpa-slider'):
        if not slider.get('tabindex'):
            slider['tabindex'] = '0'
        if not slider.get('aria-label'):
            slider['aria-label'] = 'Photo Carousel'

    # Ensure main landmark wraps main content if not already present
    if not body.find('main'):
        header = body.find('header', class_='ltt-navbar') or body.find('header')
        footer = body.find('footer')
        
        main_tag = soup.new_tag('main', id='main', role='main')
        
        # Collect nodes between header and footer/scripts
        nodes_to_wrap = []
        started = False if header else True
        
        for child in list(body.children):
            if child == header:
                started = True
                continue
            if not started:
                continue
            if child == footer:
                break
            if child.name == 'script' and child.get('id') in ['ltt-schema-jsonld', 'bpa-slider-perf-runtime']:
                break
            nodes_to_wrap.append(child)
            
        if nodes_to_wrap:
            if header:
                header.insert_after(main_tag)
            else:
                body.insert(0, main_tag)
            for node in nodes_to_wrap:
                main_tag.append(node.extract())

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print(f"Updated {len(all_html)} HTML files with <main>, iframe titles, slider tabindex, and catalog links.")
