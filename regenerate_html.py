#!/usr/bin/env python3
"""Régénération HTML pour SkyLinux après nettoyage"""
import re
from pathlib import Path

BASE = Path('/home/aselophe/linux-debutant')
DOCS = BASE / 'docs'

STYLE = '''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
nav{display:flex;justify-content:space-between;margin-top:30px;padding-top:20px;border-top:1px solid #333}
a{color:#00d9ff;text-decoration:none}a:hover{text-decoration:underline}
hr{border:none;border-top:1px solid #333;margin:20px 0}
.code-block{background:#111118;border-radius:8px;overflow:hidden;margin:15px 0;border:1px solid #30363d}
.code-line{display:flex;align-items:center;padding:12px 16px;cursor:pointer;transition:background .15s}
.code-line:hover{background:rgba(255,255,255,.04)}
.code-line code{background:none;color:#e6edf3;padding:0;font-family:'Courier New',monospace;font-size:13.5px;line-height:1.5;white-space:pre;flex:1;overflow-x:auto}
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
</nav></div></body></html>'''

def convert(md_text):
    md_text = re.sub(r'```(?:bash|python|sh)?\n(.*?)```',
        lambda m: '<div class="code-block"><div class="code-line"><code>' + 
        m.group(1).strip().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;') + 
        '</code></div></div>', md_text, flags=re.DOTALL)
    md_text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', md_text)
    lines = md_text.split('\n')
    res, ul, bq, tbl = [], False, False, False
    for line in lines:
        if line.startswith('### '):
            if ul: res.append('</ul>'); ul=False
            if bq: res.append('</blockquote>'); bq=False
            if tbl: res.append('</table>'); tbl=False
            res.append('<h3>'+line[4:]+'</h3>')
        elif line.startswith('## '):
            if ul: res.append('</ul>'); ul=False
            if bq: res.append('</blockquote>'); bq=False
            if tbl: res.append('</table>'); tbl=False
            res.append('<h2>'+line[3:]+'</h2>')
        elif line.startswith('- ') or line.startswith('* '):
            if bq: res.append('</blockquote>'); bq=False
            if tbl: res.append('</table>'); tbl=False
            if not ul: res.append('<ul>'); ul=True
            res.append('<li>'+line[2:]+'</li>')
        elif line.startswith('|'):
            if ul: res.append('</ul>'); ul=False
            if bq: res.append('</blockquote>'); bq=False
            if not tbl: res.append('<table>'); tbl=True
            cells=[c.strip() for c in line.split('|')[1:-1]]
            if all(set(c.replace('-','').replace(':','').replace(' ',''))<=set('') for c in cells if c): continue
            is_th=(len(res)>0 and res[-1]=='<table>')
            tag='<th>' if is_th else '<td>'; end='</th>' if is_th else '</td>'
            res.append('<tr>'+''.join(tag+c+end for c in cells)+'</tr>')
        elif line.startswith('---'):
            if ul: res.append('</ul>'); ul=False
            if bq: res.append('</blockquote>'); bq=False
            if tbl: res.append('</table>'); tbl=False
            res.append('<hr/>')
        elif line.startswith('> '):
            if ul: res.append('</ul>'); ul=False
            if tbl: res.append('</table>'); tbl=False
            if not bq: res.append('<blockquote>'); bq=True
            res.append('<p>'+line[2:]+'</p>')
        else:
            if ul: res.append('</ul>'); ul=False
            if bq: res.append('</blockquote>'); bq=False
            if tbl: res.append('</table>'); tbl=False
            if line.strip(): res.append('<p>'+line+'</p>')
    if ul: res.append('</ul>')
    if bq: res.append('</blockquote>')
    if tbl: res.append('</table>')
    return '\n'.join(res)

# Régénérer
all_md = sorted(BASE.glob('[0-9][0-9]-*.md'), key=lambda x: int(x.name[:2]))
n = len(all_md)

# Nettoyer vieux HTML
for f in DOCS.glob('[0-9][0-9]-*.html'):
    f.unlink()

for i, md_file in enumerate(all_md):
    content = md_file.read_text()
    tm = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = tm.group(1) if tm else md_file.stem
    body_text = re.sub(r'^# .+\n', '', content)
    html_body = convert(body_text)
    prev = f'<a href="{all_md[i-1].name.replace(".md",".html")}">&larr; {all_md[i-1].stem}</a>' if i>0 else ''
    next = f'<a href="{all_md[i+1].name.replace(".md",".html")}">{all_md[i+1].stem} &rarr;</a>' if i<n-1 else ''
    nav = NAV.replace('___PREV___', prev).replace('___NEXT___', next)
    page = STYLE + '<h1>' + title + '</h1>\n' + html_body + nav
    (DOCS / md_file.name.replace('.md', '.html')).write_text(page)

# Index
items = ''
for m in all_md:
    c = m.read_text()
    t = re.search(r'^# (.+)$', c, re.MULTILINE)
    tit = t.group(1) if t else m.stem
    items += f'        <li><a href="{m.name.replace(".md",".html")}">{tit}</a></li>\n'

ip = DOCS / 'index.html'
if ip.exists():
    h = ip.read_text()
    h = re.sub(r'(<ul[^>]*>).*?(</ul>)', r'\1\n'+items+r'        \2', h, flags=re.DOTALL)
    h = re.sub(r'\d+ leçons', f'{n} leçons', h)
    ip.write_text(h)

print(f'✅ {n} leçons HTML régénérées, index mis à jour')
