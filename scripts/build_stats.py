#!/usr/bin/env python3
"""Build the tourism statistics pages of luxurytraveltester.com from scripts/stats/<slug>.py.

    python3 scripts/build_stats.py            # all pages in scripts/stats/
    python3 scripts/build_stats.py dubai-tourism-statistics

Each page uses the shell of best-desert-safaris-dubai (head CSS, nav, footer), drops the
card deck and sticky booking bar, and fills the article column with question-style H2s,
key-figure tiles, CSS bar charts (each with a data table and an "Embed this chart" box),
sources and methodology. It also writes one standalone embed page per chart to
embed/<slug>/<chart id>.html (noindex, canonical = the statistics page).

Same format as the statistics pages on thecruisedetective.com. Run scripts/sync_layout.py
afterwards (menu, footer, search index) and scripts/generate_sitemap.py.
"""
import datetime as dt
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / "best-desert-safaris-dubai" / "index.html"
SPECS = ROOT / "scripts" / "stats"
SITE = "https://luxurytraveltester.com"
BRAND = "Luxury Travel Tester"
AUTHOR = {"name": "Adam Dimitrov", "url": "/about",
          "avatar": "/assets/cdn/67d02edca7795b0f57073b59/67d02edca7795b0f57073f59_Adam-dimitrov-portrait-500x500.webp"}
E = html.escape
NAVY, GOLD, SLATE = "#1e3a5f", "#b7791f", "#94a3b8"

STATS_CSS = """<style id="ltt-stats-css">
.ltt-stats{max-width:860px;margin:8px auto 0;font-size:16px;line-height:1.7;color:#1e293b}
.ltt-stats h2{font-family:'Playfair Display',Georgia,serif;font-size:28px;line-height:1.25;margin:40px 0 12px;color:#0f172a;scroll-margin-top:88px}
.ltt-stats p{margin:0 0 14px}
.ltt-stats ul{margin:0 0 18px 22px;padding:0}
.ltt-stats li{margin-bottom:8px}
.ltt-stats a{color:#855a00;font-weight:600;text-decoration:underline}
.ltt-stats a:hover,.ltt-stats a:focus{color:#5c3e00}
.bpa-tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0 24px}
.bpa-tile{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px 14px;box-sizing:border-box}
.bpa-tile-num{font-size:30px;font-weight:800;color:#0f172a;line-height:1.1;letter-spacing:-0.02em}
.bpa-tile-lab{font-size:13px;color:#64748b;margin-top:4px;line-height:1.35;font-weight:500}
@media (max-width:768px){.bpa-tiles{grid-template-columns:repeat(2,1fr)}}
@media (max-width:480px){.bpa-tiles{grid-template-columns:1fr}.bpa-tile-num{font-size:26px}}
.bpa-chart{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:20px 20px 14px;margin:20px 0 16px;box-sizing:border-box}
.bpa-chart-head{margin-bottom:8px}
.bpa-chart-title{font-weight:800;font-size:16px;color:#0f172a;line-height:1.3}
.bpa-chart-sub{font-size:13px;color:#64748b;margin-top:2px}
.bpa-legend{display:flex;flex-wrap:wrap;gap:14px;margin:12px 0 4px;font-size:13px;color:#334155}
.bpa-leg{display:inline-flex;align-items:center;gap:6px}
.bpa-leg i{display:inline-block;width:12px;height:12px;border-radius:3px}
.bpa-bars{margin-top:12px}
.bpa-row{display:grid;grid-template-columns:136px 1fr;align-items:center;gap:10px;margin:7px 0}
.bpa-lab{font-size:13px;color:#334155;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bpa-track{display:flex;align-items:center;gap:2px;min-width:0}
.bpa-seg{display:block;height:18px;min-width:2px}
.bpa-track .bpa-seg:last-of-type{border-radius:0 4px 4px 0}
.bpa-val{font-size:13px;font-weight:700;color:#0f172a;margin-left:8px;white-space:nowrap}
.bpa-src{font-size:12px;color:#64748b;margin-top:12px;line-height:1.5}
.ltt-stats .bpa-src a{color:#475569;font-weight:400}
.bpa-details{margin:4px 0 24px;width:100%;box-sizing:border-box}
.bpa-details summary{cursor:pointer;font-size:13.5px;font-weight:700;color:#0369a1;padding:4px 0;user-select:none}
.bpa-details summary:hover{color:#075985}
.bpa-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0 20px;border:1px solid #e2e8f0;border-radius:10px;width:100%;box-sizing:border-box}
.bpa-table{width:100%;min-width:480px;border-collapse:collapse;font-size:13.5px;font-variant-numeric:tabular-nums;background:#fff}
.bpa-table caption{caption-side:bottom;text-align:left;font-size:12px;color:#64748b;padding:8px 12px}
.bpa-table th{text-align:left;font-weight:700;color:#0f172a;border-bottom:2px solid #e2e8f0;padding:9px 12px;white-space:nowrap;background:#f8fafc}
.bpa-table td{border-bottom:1px solid #f1f5f9;padding:8px 12px;color:#334155;white-space:nowrap}
.bpa-table tr:last-child td{border-bottom:none}
.bpa-table td:not(:first-child),.bpa-table th:not(:first-child){text-align:right}
.bpa-cite{background:#fffbeb;border:1px solid #fde68a;border-radius:12px;padding:16px;font-size:14.5px;line-height:1.6;color:#334155;margin:20px 0}
.bpa-plan{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;margin:24px 0}
.bpa-plan ul{margin:8px 0 0 20px}
.bpa-embed{margin:-8px 0 20px}
.bpa-embed-btn{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #cbd5e1;border-radius:9999px;padding:6px 14px;font:700 12.5px/1.2 inherit;color:#1e3a5f;cursor:pointer}
.bpa-embed-btn:hover{background:#f1f5f9;color:#1e3a5f}
.bpa-embed-panel{margin-top:10px;padding:14px;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc}
.bpa-embed-panel[hidden]{display:none}
.bpa-embed-code{width:100%;box-sizing:border-box;min-height:118px;font:12px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;color:#0f172a;border:1px solid #cbd5e1;border-radius:8px;padding:10px;background:#fff;resize:vertical}
.bpa-embed-row{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:8px}
.bpa-embed-copy{background:#1e3a5f;color:#fff;border:0;border-radius:8px;padding:8px 14px;font:700 13px/1 inherit;cursor:pointer}
.bpa-embed-copy:hover{background:#16304f;color:#fff}
.bpa-embed-note{font-size:12.5px;color:#475569;line-height:1.4;flex:1;min-width:200px}
/* no red hover */
.ltt-author-role a{color:#855a00}
.ltt-breadcrumbs a:hover,.ltt-author-line a:hover,.ltt-author-role a:hover,.tocitem:hover,.hp-guide:hover{color:#0f172a}
@media (max-width:520px){.bpa-row{grid-template-columns:104px 1fr;gap:6px}.bpa-chart{padding:16px 12px 12px}.bpa-val{font-size:11.5px;margin-left:5px}.bpa-lab{font-size:12px}.ltt-stats h2{font-size:24px}}
</style>"""

EMBED_JS = """<script id="ltt-embed-js">(function(){
document.addEventListener('click',function(e){
  var b=e.target.closest('.bpa-embed-btn');
  if(b){var p=document.getElementById(b.getAttribute('aria-controls'));if(!p)return;var open=p.hasAttribute('hidden');
    if(open){p.removeAttribute('hidden');}else{p.setAttribute('hidden','');}
    b.setAttribute('aria-expanded',open?'true':'false');
    if(open&&window.gtag){gtag('event','embed_open',{chart_id:b.getAttribute('data-chart')});}
    return;}
  var c=e.target.closest('.bpa-embed-copy');
  if(c){var t=c.closest('.bpa-embed-panel').querySelector('textarea');t.select();
    var done=function(){var l=c.textContent;c.textContent=c.getAttribute('data-done');setTimeout(function(){c.textContent=l;},1800);};
    if(navigator.clipboard){navigator.clipboard.writeText(t.value).then(done,function(){document.execCommand('copy');done();});}
    else{document.execCommand('copy');done();}
    if(window.gtag){gtag('event','embed_copy',{chart_id:c.getAttribute('data-chart')});}}
});})();</script>"""


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ------------------------------------------------------------------ charts
def chart_html(c, spec):
    """c: id, title, sub, rows [(label, value or [values], display)], legend [(name,color)],
    colors, src (html), table {caption, head, rows}, label_w."""
    rows = c["rows"]
    tot = lambda v: sum(v) if isinstance(v, (list, tuple)) else v
    vmax = c.get("max") or max(tot(v) for _, v, _ in rows)
    colors = c.get("colors") or [NAVY, GOLD, SLATE]
    out = [f'<div class="bpa-chart" id="{c["id"]}" role="figure" aria-labelledby="{c["id"]}-t">',
           '<div class="bpa-chart-head">',
           f'<div class="bpa-chart-title" id="{c["id"]}-t">{E(c["title"])}</div>',
           f'<div class="bpa-chart-sub">{E(c["sub"])}</div>', '</div>']
    if c.get("legend"):
        out.append('<div class="bpa-legend">' + "".join(
            f'<span class="bpa-leg"><i style="background:{col}"></i>{E(n)}</span>' for n, col in c["legend"]) + "</div>")
    lw = c.get("label_w")
    if lw:
        out.append(f'<style>#{c["id"]} .bpa-row{{grid-template-columns:{lw}px 1fr}}'
                   f'@media (max-width:520px){{#{c["id"]} .bpa-row{{grid-template-columns:{min(lw, 112)}px 1fr}}}}</style>')
    out.append('<div class="bpa-bars">')
    for i, (lab, v, disp) in enumerate(rows):
        vals = v if isinstance(v, (list, tuple)) else [v]
        hl = c.get("highlight")
        segs = []
        for k, x in enumerate(vals):
            col = colors[k % len(colors)]
            if hl is not None and len(vals) == 1:
                col = GOLD if i in hl else NAVY
            w = 100.0 * x / vmax
            segs.append(f'<span class="bpa-seg" style="width:{w:.2f}%;background:{col}" title="{E(lab)}: {E(disp)}"></span>')
        short = c.get("short", {}).get(lab, lab)
        out.append(f'<div class="bpa-row"><span class="bpa-lab" title="{E(lab)}">{E(short)}</span><span class="bpa-track">'
                   + "".join(segs) + f'<b class="bpa-val">{E(disp)}</b></span></div>')
    out.append("</div>")
    out.append(f'<div class="bpa-src">Source: {c["src"]}</div>')
    out.append("</div>")
    chart = "\n".join(out)
    embed = embed_box(c, spec)
    t = c["table"]
    table = ('<details class="bpa-details"><summary>Show the data table</summary><div class="bpa-table-wrap"><table class="bpa-table">'
             f'<caption>{E(t["caption"])}</caption><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in t["head"]) + "</tr></thead><tbody>"
             + "".join("<tr>" + "".join(f"<td>{E(str(x))}</td>" for x in r) + "</tr>" for r in t["rows"])
             + "</tbody></table></div></details>")
    return chart, embed, table


def chart_height(c):
    return 118 + 31 * len(c["rows"]) + (34 if c.get("legend") else 0) + (16 if len(c["src"]) > 160 else 0)


def embed_box(c, spec):
    url = f'{SITE}/embed/{spec["slug"]}/{c["id"]}'
    code = (f'<iframe src="{url}" title="{c["title"]}" width="100%" height="{chart_height(c)}" '
            f'style="border:0;max-width:760px" loading="lazy"></iframe>\n'
            f'<p style="font-size:13px">Source: <a href="{SITE}/{spec["slug"]}">{spec["short_name"]}</a>, by {BRAND}</p>')
    pid = f'bpa-embed-{c["id"]}'
    return (f'<div class="bpa-embed"><button type="button" class="bpa-embed-btn" aria-expanded="false" aria-controls="{pid}" '
            f'data-chart="{c["id"]}"><span aria-hidden="true">&lt;/&gt;</span> Embed this chart</button>'
            f'<div class="bpa-embed-panel" id="{pid}" hidden><textarea class="bpa-embed-code" readonly aria-label="Embed this chart">'
            f'{E(code)}</textarea><div class="bpa-embed-row"><button type="button" class="bpa-embed-copy" data-chart="{c["id"]}" '
            'data-done="Copied!">Copy code</button><span class="bpa-embed-note">Free to use on your site, article or report. '
            'Please keep the source link.</span></div></div></div>')


def embed_page(c, spec, chart):
    css = STATS_CSS.split('<style id="ltt-stats-css">')[1].split("</style>")[0]
    css = "\n".join(l for l in css.splitlines() if l.startswith((".bpa-chart", ".bpa-leg", ".bpa-bars", ".bpa-row", ".bpa-lab",
                                                                   ".bpa-track", ".bpa-seg", ".bpa-val", ".bpa-src", "@media (max-width:520px)")))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{E(c["title"])} | {BRAND}</title>
<meta name="robots" content="noindex, follow"/>
<link rel="canonical" href="{SITE}/{spec["slug"]}"/>
<style>
html,body{{margin:0;padding:0;background:#fff}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#0f172a}}
{css}
.bpa-chart{{margin:0 !important}}
.bpa-src a{{color:#475569}}
.bpa-credit{{font-size:12px;color:#64748b;margin:8px 4px 0;text-align:right}}
.bpa-credit a{{color:#1e3a5f;font-weight:700;text-decoration:none}}
</style>
</head>
<body>
{chart}
<div class="bpa-credit">Chart by <a href="{SITE}/{spec["slug"]}" target="_blank" rel="noopener">{BRAND}</a></div>
</body>
</html>
"""


# ------------------------------------------------------------------ page
def body_html(spec):
    parts, toc = [], []
    for sec in spec["sections"]:
        sid = sec.get("id") or slugify(sec["h2"])
        toc.append((sid, sec.get("toc", sec["h2"])))
        parts.append(f'<h2 id="{sid}">{E(sec["h2"])}</h2>')
        for blk in sec["blocks"]:
            if isinstance(blk, str):
                parts.append(blk)
            elif blk.get("tiles"):
                parts.append('<div class="bpa-tiles">' + "".join(
                    f'<div class="bpa-tile"><div class="bpa-tile-num">{E(n)}</div><div class="bpa-tile-lab">{E(l)}</div></div>'
                    for n, l in blk["tiles"]) + "</div>")
            elif blk.get("chart"):
                ch, emb, tab = chart_html(blk["chart"], spec)
                parts += [ch, emb, tab]
    parts.append(f'<div class="bpa-cite"><strong>Using these statistics?</strong> You are welcome to quote the figures and charts on '
                 f'this page. Please credit and link to <a href="/{spec["slug"]}">{BRAND}, {E(spec["short_name"])}</a>.</div>')
    return "\n".join(parts), toc


def charts_of(spec):
    return [b["chart"] for s in spec["sections"] for b in s["blocks"] if isinstance(b, dict) and b.get("chart")]


def jsonld(spec, today, image):
    url = f"{SITE}/{spec['slug']}"
    g = [{"@type": "Article", "@id": url + "#article", "headline": spec["headline"], "description": spec["meta_description"],
          "image": image, "datePublished": spec.get("date_published", today), "dateModified": today,
          "mainEntityOfPage": url, "inLanguage": "en",
          "author": {"@type": "Person", "name": AUTHOR["name"], "url": SITE + AUTHOR["url"], "jobTitle": "Founder"},
          "publisher": {"@type": "Organization", "name": BRAND, "url": SITE,
                        "logo": {"@type": "ImageObject", "url": SITE + "/assets/icons/icon-512.png"}},
          "citation": spec["citations"]},
         {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
             {"@type": "ListItem", "position": 2, "name": spec["breadcrumb"], "item": url}]}]
    faqs = spec.get("faqs") or [
        (re.sub(r"<[^>]+>", "", m.group(1)).strip(), m.group(2).strip())
        for s in spec["sections"] if s.get("id") == "faq" for b in s["blocks"] if isinstance(b, str)
        for m in [re.match(r"<p><strong>(.*?)</strong>\s*(.*)</p>$", b, re.S)] if m]
    if faqs:
        plain = lambda s: re.sub(r"<[^>]+>", "", s)
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=1)


def build(spec):
    slug = spec["slug"]
    today = dt.date.today().isoformat()
    today_h = dt.date.today().strftime("%b %-d, %Y")
    url = f"{SITE}/{slug}"
    image = SITE + spec["image"]
    s = BeautifulSoup(SHELL.read_text(encoding="utf-8"), "html.parser")

    # head
    s.title.string = spec["title_tag"]
    for sel, val in [('meta[name="description"]', spec["meta_description"]), ('meta[property="og:title"]', spec["title_tag"]),
                     ('meta[property="og:description"]', spec["meta_description"]), ('meta[name="twitter:title"]', spec["title_tag"]),
                     ('meta[name="twitter:description"]', spec["meta_description"]), ('meta[property="og:url"]', url),
                     ('meta[property="og:image"]', image), ('meta[name="twitter:image"]', image),
                     ('meta[property="og:type"]', "article")]:
        t = s.select_one(sel)
        if t:
            t["content"] = val
    s.select_one('link[rel="canonical"]')["href"] = url
    for sel in ['link[rel="preload"][as="image"]', 'link[rel="alternate"][type="text/markdown"]']:
        for l in s.select(sel):
            l.decompose()
    s.head.append(BeautifulSoup(STATS_CSS, "html.parser"))

    # hero
    lead = "".join(f"<p>{p}</p>" for p in spec["lead"])
    n_charts = len(charts_of(spec))
    hero = f'''<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs"><a href="/">Home</a><span class="ltt-bc-sep">›</span><span class="ltt-bc-current">{E(spec["breadcrumb"])}</span></nav>
<span class="ltt-hero-kicker-badge">{E(spec["kicker_badge"])}</span>
</div>
<h1 class="ltt-editorial-h1">{E(spec["h1_main"])} <span class="ltt-h1-muted">{E(spec["h1_muted"])}</span></h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap"><img alt="{AUTHOR["name"]}" class="ltt-author-avatar" height="32" src="{AUTHOR["avatar"]}" width="32"/></div>
<div class="ltt-author-meta">
<div class="ltt-author-line">By <a href="{AUTHOR["url"]}">{AUTHOR["name"]}</a>, Founder</div>
<div class="ltt-author-role">{E(spec["author_role"])} • {n_charts} Charts with Data Tables • <a href="#sources-and-methodology">Methodology</a></div>
</div>
</div>
<div class="ltt-trust-pills"><span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: {today_h}</span></div>
</div>
<div class="ltt-lead-copy">{lead}</div>
</div>
</div>'''
    s.select_one(".ltt-hero-wrap").replace_with(BeautifulSoup(hero, "html.parser"))

    # drop the deck, the sticky booking bar and its sheet
    for sel in [".comparison-table", "#sticky-bar", "#hybridBackdrop", "#Standard-Features"]:
        t = s.select_one(sel)
        if t:
            t.decompose()

    # article column + static table of contents
    body, toc = body_html(spec)
    cont = s.select_one("#content .container-33") or s.select_one("#content")
    cont.clear()
    cont.append(BeautifulSoup(f'<div class="ltt-stats w-richtext">{body}</div>{EMBED_JS}', "html.parser"))
    tocel = s.select_one("#toc")
    tocel.clear()
    tocel["data-synced"] = "true"
    tocel.append(BeautifulSoup("".join(f'<a class="tocitem" href="#{i}">{E(t)}</a>' for i, t in toc), "html.parser"))

    for sc in s.find_all("script"):
        if sc.string and "window.LTT_PAGE_CONFIG =" in sc.string:
            sc.string = "\nwindow.LTT_PAGE_CONFIG = " + json.dumps({"deckId": "ltt-no-deck"}) + ";\n"
    s.select_one("#ltt-schema-jsonld").string = jsonld(spec, today, image)
    for a in s.select(".w--current"):
        a["class"] = [c for c in a.get("class", []) if c != "w--current"]

    txt = str(s)
    out = ROOT / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(txt, encoding="utf-8")

    # embed pages
    edir = ROOT / "embed" / slug
    edir.mkdir(parents=True, exist_ok=True)
    for c in charts_of(spec):
        ch, _, _ = chart_html(c, spec)
        (edir / f'{c["id"]}.html').write_text(embed_page(c, spec, ch), encoding="utf-8")

    main = BeautifulSoup(txt, "html.parser").select_one("main")
    for t in main.find_all(["style", "script"]):
        t.decompose()
    text = main.get_text(" ")
    problems = []
    if "—" in text + spec["title_tag"] + spec["meta_description"] + jsonld(spec, today, image):
        problems.append("em dash")
    left = sorted(set(re.findall(r"(?i)\b(safari camp|dune bashing|al khayma|check availability)\b", text)))
    if left:
        problems.append("shell words: " + ", ".join(left))
    print(f"wrote {out.relative_to(ROOT)} ({len(txt)//1024} KB, {n_charts} charts){'  ! ' + '; '.join(problems) if problems else ''}")


def load(path):
    sp = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m.SPEC


if __name__ == "__main__":
    names = sys.argv[1:]
    files = [SPECS / f"{n}.py" for n in names] if names else sorted(SPECS.glob("*.py"))
    for f in files:
        build(load(f))
