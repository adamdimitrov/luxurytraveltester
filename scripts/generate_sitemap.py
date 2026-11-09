#!/usr/bin/env python3
"""
Luxury Travel Tester — Automated XML Sitemap & robots.txt Generator
Generates a 100% Google-compliant sitemap with multi-lingual xhtml:link annotations.
"""
import os, sys, datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITEMAP_PATH = os.path.join(ROOT_DIR, 'sitemap.xml')
ROBOTS_PATH = os.path.join(ROOT_DIR, 'robots.txt')

def build_sitemap():
    canon_data = {}

    for root, dirs, files in os.walk(ROOT_DIR):
        if any(p.startswith('.') for p in root.split(os.sep)):
            continue
        for f in files:
            if f.endswith('.html') and f != 'sitemap.html' and not f.startswith('test-'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                    soup = BeautifulSoup(fp, 'html.parser')
                c = soup.find('link', rel='canonical')
                if c and c.get('href'):
                    canon = c['href'].strip()
                    mtime = os.path.getmtime(fpath)
                    mdate = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                    
                    alts = []
                    for a in soup.find_all('link', rel='alternate'):
                        lang = a.get('hreflang')
                        href = a.get('href')
                        if lang and href:
                            alts.append((lang.strip(), href.strip()))
                    
                    if canon in canon_data:
                        if mdate > canon_data[canon]['mdate']:
                            canon_data[canon]['mdate'] = mdate
                        existing_alts = set(canon_data[canon]['alts'])
                        existing_alts.update(alts)
                        canon_data[canon]['alts'] = list(existing_alts)
                    else:
                        canon_data[canon] = {
                            'mdate': mdate,
                            'alts': alts,
                            'fpath': os.path.relpath(fpath, ROOT_DIR)
                        }

    def get_priority_and_freq(url):
        path = urlparse(url).path.strip('/')
        parts = path.split('/')
        if not path or (len(parts) == 1 and len(parts[0]) == 2):
            return '1.0', 'daily'
        
        last_seg = parts[-1]
        if len(parts) == 1 or (len(parts) == 2 and len(parts[0]) == 2):
            if any(p in last_seg for p in ['desert', 'safari', 'helicopter', 'hotel', 'palm']) or 'wüstensafari' in last_seg or 'szafari' in last_seg:
                return '0.9', 'weekly'
            if any(u in last_seg for u in ['privacy', 'terms', 'adatvedelem']):
                return '0.3', 'yearly'
            if any(u in last_seg for u in ['about', 'contact', 'kontakt', 'o', 'hakkında']):
                return '0.5', 'monthly'
            return '0.8', 'weekly'
            
        if any(k in path for k in ['review', 'отзыв', 'recenz', 'inceleme', 'đánh-giá', 'บทวิจารณ์']):
            return '0.8', 'weekly'
        return '0.7', 'monthly'

    urlset = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xhtml': 'http://www.w3.org/1999/xhtml'
    })

    sorted_urls = sorted(canon_data.keys(), key=lambda u: (0 if '/en' in u or urlparse(u).path in ['', '/best-desert-safaris-dubai', '/best-helicopter-tours-new-york', '/best-palm-jumeirah-hotels-dubai'] else 1, u))

    for u in sorted_urls:
        d = canon_data[u]
        priority, freq = get_priority_and_freq(u)
        
        url_el = ET.SubElement(urlset, 'url')
        loc_el = ET.SubElement(url_el, 'loc')
        loc_el.text = u
        
        lastmod_el = ET.SubElement(url_el, 'lastmod')
        lastmod_el.text = d['mdate']
        
        changefreq_el = ET.SubElement(url_el, 'changefreq')
        changefreq_el.text = freq
        
        priority_el = ET.SubElement(url_el, 'priority')
        priority_el.text = priority
        
        for lang, alt_href in sorted(d['alts'], key=lambda x: x[0]):
            ET.SubElement(url_el, '{http://www.w3.org/1999/xhtml}link', {
                'rel': 'alternate',
                'hreflang': lang,
                'href': alt_href
            })

    xml_str = ET.tostring(urlset, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')

    with open(SITEMAP_PATH, 'wb') as f:
        f.write(pretty_xml)

    print(f'Wrote sitemap.xml to {SITEMAP_PATH} ({len(canon_data)} URLs)')

    robots_content = '''# robots.txt for luxurytraveltester.com
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

# Agentic Resource Discovery (discovered via /.well-known/ard.json & Link headers)
# ard.json: https://luxurytraveltester.com/.well-known/ard.json

# Canonical Sitemaps
Sitemap: https://luxurytraveltester.com/sitemap.xml
'''
    with open(ROBOTS_PATH, 'w', encoding='utf-8') as f:
        f.write(robots_content)

    print(f'Wrote robots.txt to {ROBOTS_PATH}')

if __name__ == '__main__':
    build_sitemap()
