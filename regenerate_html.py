#!/usr/bin/env python3
"""Régénération HTML SkyLinux — blocs de code avec copie + progression"""
import os
import re
from pathlib import Path

BASE = Path('/home/aselophe/linux-debutant')
DOCS = BASE / 'docs'

STYLE = '''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Inter",sans-serif;background:#0a0a0f;color:#e0e0e0;min-height:100vh;padding:40px 20px}
.container{max-width:800px;margin:0 auto}
h1{font-size:1.8rem;background:linear-gradient(135deg,#00d9ff,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:20px}
h2{color:#00d9ff;margin:20px 0 10px}
h3{color:#a855f7;margin:15px 0 8px}
p{line-height:1.7;margin:10px 0;color:#bbb}
code{background:rgba(0,217,255,.1);color:#00d9ff;padding:2px 6px;border-radius:4px;font-family:monospace;font-size:.9em}
table{width:100%;border-collapse:collapse;margin:15px 0}
th,td{border:1px solid #333;padding:8px}
th{background:rgba(0,217,255,.1)}
tr:nth-child(even){background:rgba(255,255,255,.02)}
blockquote{border-left:3px solid #a855f7;padding:10px 15px;margin:15px 0;background:rgba(168,85,247,.1);border-radius:0 8px 8px 0}
blockquote p{color:#ddd;margin:5px 0}
li{line-height:1.8;color:#bbb;margin-left:20px}
li code{background:rgba(0,217,255,.1);color:#00d9ff;padding:2px 6px;border-radius:4px;font-family:monospace}
nav{display:flex;justify-content:space-between;margin-top:30px;padding-top:20px;border-top:1px solid #333}
a{color:#00d9ff;text-decoration:none}a:hover{text-decoration:underline}
hr{border:none;border-top:1px solid #333;margin:20px 0}
p code,li code{background:rgba(0,217,255,.1);color:#00d9ff;padding:2px 6px;border-radius:4px;font-family:monospace}

/* === Code Block avec copie + progression === */
.code-block{background:#111118;border-radius:8px;overflow:hidden;margin:15px 0;border:1px solid #30363d}
.code-block progress{width:100%;height:3px;appearance:none;border:none;display:block}
.code-block progress::-webkit-progress-bar{background:#238636}
.code-block progress::-moz-progress-bar{background:#238636}
.code-block progress.loaded{background:#30363d}
.code-line{display:flex;align-items:center;padding:12px 16px;cursor:pointer;position:relative;transition:background .15s}
.code-line:hover{background:rgba(255,255,255,.04)}
.code-line code{background:none;color:#e6edf3;padding:0;font-family:"Courier New",monospace;font-size:13.5px;line-height:1.5;white-space:pre;flex:1;overflow-x:auto}
.copy-btn{margin-left:12px;background:none;border:1px solid #30363d;border-radius:6px;cursor:pointer;padding:4px 8px;opacity:.5;transition:opacity .2s,border-color .2s;flex-shrink:0;display:flex;align-items:center}
.copy-btn:hover{opacity:1;border-color:#58a6ff}
.copy-btn.copied{border-color:#238636;opacity:1}
.copy-btn svg{width:14px;height:14px;fill:#8b949e;display:block}
.copy-btn.copied svg{fill:#238636}
</style></head>
<body>
<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:15px;margin-bottom:20px;border-bottom:1px solid #333">
<a href="index.html" style="color:#666;text-decoration:none">&larr; Sommaire</a>
<span style="font-size:1.2rem;font-weight:700;background:linear-gradient(135deg,#00d9ff,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent">SkyLinux</span>
</div><div class="container">
'''

NAV = '''
<nav>
___PREV___
___NEXT___
</nav></div>
<script>
function copyCode(el){var container=el.closest(".code-block");var code=el.querySelector("code");var btn=el.querySelector(".copy-btn");var progress=container.querySelector("progress");if(!code||!btn)return;var text=code.textContent;navigator.clipboard.writeText(text).then(function(){btn.classList.add("copied");btn.querySelector("svg").innerHTML='<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>';setTimeout(function(){btn.classList.remove("copied");btn.querySelector("svg").innerHTML='<path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>'},2000);var val=0;progress.value=0;progress.classList.remove("loaded");var interval=setInterval(function(){val+=5;progress.value=val;if(val>=100){clearInterval(interval);setTimeout(function(){progress.classList.add("loaded")},300)}},20)}).catch(function(){var ta=document.createElement("textarea");ta.value=text;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();document.execCommand("copy");document.body.removeChild(ta)})}
</script>
</body></html>'''

COPY_SVG = '<svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>'

def code_block(m):
    """Convertit ```bash ... ``` en div.code-block avec progress + copy-btn"""
    code_text = m.group(1).strip()
    # Échapper HTML
    escaped = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'<div class="code-block">\n  <progress value="0" max="100"></progress>\n  <div class="code-line" onclick="copyCode(this)">\n    <code>{escaped}</code>\n    <button class="copy-btn" aria-label="Copier">\n      {COPY_SVG}\n    </button>\n  </div>\n</div>'

def convert(md_text):
    # Blocs de code ```...``` → placeholder pour protéger du parsing paragraphe
    placeholders = {}
    counter = [0]
    def save_code_block(m):
        counter[0] += 1
        key = f'%%CODEBLOCK{counter[0]}%%'
        placeholders[key] = code_block(m)
        return key
    md_text = re.sub(r'```(?:bash|python|sh|shell|console|text|plain)?\s*\n(.*?)```', save_code_block, md_text, flags=re.DOTALL)
    # Code inline
    md_text = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', r'<code>\1</code>', md_text)
    
    lines = md_text.split('\n')
    res, ul, bq, tbl = [], False, False, False
    for line in lines:
        # Titres
        if line.startswith('### '):
            if ul: res.append('</ul>'); ul = False
            if bq: res.append('</blockquote>'); bq = False
            if tbl: res.append('</table>'); tbl = False
            res.append('<h3>' + line[4:] + '</h3>')
        elif line.startswith('## '):
            if ul: res.append('</ul>'); ul = False
            if bq: res.append('</blockquote>'); bq = False
            if tbl: res.append('</table>'); tbl = False
            res.append('<h2>' + line[3:] + '</h2>')
        # Listes
        elif re.match(r'^[\-\*]\s', line):
            if bq: res.append('</blockquote>'); bq = False
            if tbl: res.append('</table>'); tbl = False
            if not ul: res.append('<ul>'); ul = True
            res.append('<li>' + line[2:] + '</li>')
        # Tableaux
        elif line.startswith('|'):
            if ul: res.append('</ul>'); ul = False
            if bq: res.append('</blockquote>'); bq = False
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(set(c.replace('-', '').replace(':', '').replace(' ', '')) <= set('') for c in cells if c):
                continue  # ligne séparateur
            if not tbl: res.append('<table>'); tbl = True
            is_th = (len(res) > 0 and res[-1] == '<table>')
            tag = '<th>' if is_th else '<td>'
            end = '</th>' if is_th else '</td>'
            res.append('<tr>' + ''.join(tag + c + end for c in cells) + '</tr>')
        # Séparateur
        elif line.startswith('---'):
            if ul: res.append('</ul>'); ul = False
            if bq: res.append('</blockquote>'); bq = False
            if tbl: res.append('</table>'); tbl = False
            res.append('<hr/>')
        # Citations
        elif line.startswith('> '):
            if ul: res.append('</ul>'); ul = False
            if tbl: res.append('</table>'); tbl = False
            if not bq: res.append('<blockquote>'); bq = True
            res.append('<p>' + line[2:] + '</p>')
        else:
            if ul: res.append('</ul>'); ul = False
            if bq: res.append('</blockquote>'); bq = False
            if tbl: res.append('</table>'); tbl = False
            # Remplacer les placeholders de code-block dans la ligne AVANT de wrapper
            for key, html_block in placeholders.items():
                if key in line:
                    # Le placeholder est sur sa propre ligne → remplacer par le HTML brut
                    res.append(html_block)
                    line = line.replace(key, '')
            if line.strip():
                res.append('<p>' + line + '</p>')
    if ul: res.append('</ul>')
    if bq: res.append('</blockquote>')
    if tbl: res.append('</table>')
    result = '\n'.join(res)
    # Réinsérer les blocs de code protégés
    for key, html in placeholders.items():
        result = result.replace(key, html)
    return result

# Régénérer tous les HTML
all_md = sorted(BASE.glob('[0-9][0-9]-*.md'), key=lambda x: int(x.name[:2]))
n = len(all_md)

for f in DOCS.glob('[0-9][0-9]-*.html'):
    f.unlink()

for i, md_file in enumerate(all_md):
    content = md_file.read_text()
    tm = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = tm.group(1) if tm else md_file.stem
    body_text = re.sub(r'^# .+\n', '', content)
    html_body = convert(body_text)
    prev = f'<a href="{all_md[i-1].name.replace(".md",".html")}">&larr; {all_md[i-1].stem}</a>' if i > 0 else ''
    nxt = f'<a href="{all_md[i+1].name.replace(".md",".html")}">{all_md[i+1].stem} &rarr;</a>' if i < n - 1 else ''
    nav = NAV.replace('___PREV___', prev).replace('___NEXT___', nxt)
    page = STYLE + '<h1>' + title + '</h1>\n' + html_body + nav
    (DOCS / md_file.name.replace('.md', '.html')).write_text(page)

# Régénérer l'index
ip = DOCS / 'index.html'
old_html = ip.read_text() if ip.exists() else ''

# Construire la liste des items
items = ''
for m in all_md:
    c = m.read_text()
    t = re.search(r'^# (.+)$', c, re.MULTILINE)
    title = t.group(1) if t else m.stem
    title_short = re.sub(r'^Leçon \d+\s*:\s*', '', title)
    num = m.name[:2]
    html_name = m.name.replace('.md', '.html')
    items += f'<a href="{html_name}" class="item"><span class="num">{num}</span><span class="title">{title_short}</span><span class="arrow">-&gt;</span></a>\n'

# Remplacer la liste dans l'index existant
# Chercher les marqueurs (flexible: avec ou sans < devant)
import re
idx_match_start = re.search(r'<p\s+class=["\']list-title["\']>', old_html)
idx_match_end = re.search(r'<p\s+class=["\']footer["\']>', old_html)

if idx_match_start and idx_match_end:
    header = old_html[:idx_match_start.start()]
    footer = old_html[idx_match_end.start():]
    # Reconstruire avec le marqueur correct
    new_html = header + '<p class="list-title">📖 Sommaire des leçons</p>\n<div class="list">\n' + items + '</div>\n' + footer
    # Mettre à jour compteurs
    new_html = re.sub(r'<span id="nb-lecons">\d+</span>', f'<span id="nb-lecons">{n}</span>', new_html)
    new_html = re.sub(r'<span id="nb-lecons2">\d+</span>', f'<span id="nb-lecons2">{n}</span>', new_html)
    new_html = re.sub(r'\d+ leçons', f'{n} leçons', new_html)
    ip.write_text(new_html)
else:
    print('⚠️ Index non trouvé, création simple')
    # Fallback simple
    idx = f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><title>SkyLinux</title></head><body><h1>SkyLinux</h1><div class="list">\n{items}</div></body></html>'
    ip.write_text(idx)

print(f'✅ {n} leçons HTML régénérées + index mis à jour')

# ---- Génération du sitemap ----
from datetime import datetime
html_files = sorted(f for f in os.listdir(DOCS) if f.endswith('.html') and f[0].isdigit())
TODAY = datetime.now().strftime('%Y-%m-%d')
urls = []
urls.append(f'  <url>\n    <loc>https://skyspirit-moltbot.github.io/skylinux/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>')
urls.append(f'  <url>\n    <loc>https://skyspirit-moltbot.github.io/skylinux/index.html</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>')
for f in html_files:
    urls.append(f'  <url>\n    <loc>https://skyspirit-moltbot.github.io/skylinux/{f}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>')
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n'
with open(DOCS / 'sitemap.xml', 'w') as sf:
    sf.write(sitemap)
print(f'✅ Sitemap généré: {len(urls)} URLs')
