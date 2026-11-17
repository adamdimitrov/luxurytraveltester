#!/usr/bin/env python3
import sys, re, os

"""
Ultra-simple Content Manager CLI:
Usage:
  python3 update_content.py replace "Old Text" "New Text"
  python3 update_content.py price "€49" "€59"
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def replace_across_site(old_text, new_text):
    count = 0
    file_count = 0
    for root, _, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fl:
                    content = fl.read()
                if old_text in content:
                    updated = content.replace(old_text, new_text)
                    with open(path, 'w', encoding='utf-8') as fl:
                        fl.write(updated)
                    file_count += 1
                    count += content.count(old_text)
    print(f"✓ Replaced '{old_text}' -> '{new_text}' across {file_count} files ({count} instances).")

if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[1] != 'replace':
        print("Usage: python3 update_content.py replace 'Exact Old Text' 'New Text'")
    else:
        replace_across_site(sys.argv[2], sys.argv[3])
