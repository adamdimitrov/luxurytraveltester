#!/usr/bin/env python3
"""
Updates Pros & Cons bullet points across all articles:
Ensures ONLY the main feature title is bolded (<strong>Feature</strong>),
and the explanation/description after the delimiter (' — ') remains regular unbolded font weight.
"""

import os
import glob
import re

def transform_pro_con_li(inner: str) -> str:
    clean = inner.strip()
    
    # If already formatted as <strong>Feature</strong> — Description, preserve / normalize delimiter
    if re.match(r'^<strong>[^<]+</strong>\s*(?:—|–|-)\s*[^<]+$', clean):
        m = re.match(r'^<strong>([^<]+)</strong>\s*(?:—|–|-)\s*(.+)$', clean, flags=re.DOTALL)
        if m:
            return f'<strong>{m.group(1).strip()}</strong> — {m.group(2).strip()}'
        return clean
    
    clean_no_strong = re.sub(r'^<strong>(.*?)</strong>$', r'\1', clean, flags=re.DOTALL).strip()
    
    # 1. Em-dash ' — ' or '—'
    m_em = re.search(r'\s*—\s*', clean_no_strong)
    if m_em:
        feat = clean_no_strong[:m_em.start()].strip()
        desc = clean_no_strong[m_em.end():].strip()
        if feat and desc and feat.count('(') == feat.count(')'):
            feat = re.sub(r'</?strong>', '', feat).strip()
            desc = re.sub(r'</?strong>', '', desc).strip()
            return f'<strong>{feat}</strong> — {desc}'
            
    # 2. En-dash with spaces ' – '
    m_en = re.search(r'\s+–\s+', clean_no_strong)
    if m_en:
        feat = clean_no_strong[:m_en.start()].strip()
        desc = clean_no_strong[m_en.end():].strip()
        if feat and desc and feat.count('(') == feat.count(')'):
            feat = re.sub(r'</?strong>', '', feat).strip()
            desc = re.sub(r'</?strong>', '', desc).strip()
            return f'<strong>{feat}</strong> — {desc}'

    # 3. Spaced hyphen ' - ' (only if desc is > 10 chars and not a known proper noun place)
    m_hy = re.search(r'\s+-\s+', clean_no_strong)
    if m_hy:
        feat = clean_no_strong[:m_hy.start()].strip()
        desc = clean_no_strong[m_hy.end():].strip()
        if feat and desc and len(desc) > 10 and feat.count('(') == feat.count(')') and not any(p in desc for p in ['Marceau', 'Vigadó']):
            feat = re.sub(r'</?strong>', '', feat).strip()
            desc = re.sub(r'</?strong>', '', desc).strip()
            return f'<strong>{feat}</strong> — {desc}'

    # 4. Colon followed by space ': ' (only if feat is <= 40 chars)
    m_col = re.search(r':\s+', clean_no_strong)
    if m_col:
        feat = clean_no_strong[:m_col.start()].strip()
        desc = clean_no_strong[m_col.end():].strip()
        if feat and desc and len(feat) <= 40 and feat.count('(') == feat.count(')'):
            feat = re.sub(r'</?strong>', '', feat).strip()
            desc = re.sub(r'</?strong>', '', desc).strip()
            return f'<strong>{feat}</strong> — {desc}'

    # If no delimiter, keep clean
    if not clean.startswith('<strong>'):
        clean = f'<strong>{clean}</strong>'
    return clean


def process_html_file(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed_items = 0

    def replace_pro_con(box_match):
        nonlocal changed_items
        box_html = box_match.group(0)
        
        def replace_li(li_match):
            nonlocal changed_items
            inner = li_match.group(1)
            new_inner = transform_pro_con_li(inner)
            if new_inner != inner:
                changed_items += 1
            return f'<li>{new_inner}</li>'

        return re.sub(r'<li>(.*?)</li>', replace_li, box_html, flags=re.DOTALL)

    new_content = re.sub(
        r'<div class=\"pro-con-box-wrapper[^\"]*\".*?</div>\s*</div>\s*</div>\s*</div>',
        replace_pro_con,
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [UPDATED] {file_path} ({changed_items} items formatted)")
    return changed_items


def process_repo(repo_dir: str):
    print(f"\nProcessing repository: {repo_dir}")
    total_updated_files = 0
    total_items = 0
    for root, _, files in os.walk(repo_dir):
        if any(skip in root for skip in ['.git', 'node_modules', 'scripts']):
            continue
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                count = process_html_file(full_path)
                if count > 0:
                    total_updated_files += 1
                    total_items += count
    print(f"Done {repo_dir}: {total_updated_files} files updated, {total_items} total items formatted.")


if __name__ == '__main__':
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else '/Users/adamdimitrov/Development/luxurytraveltester'
    process_repo(target)
