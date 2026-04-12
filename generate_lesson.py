import re, sys

STYLE_HEADER = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Inter", sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; padding: 40px 20px; }
.container { max-width: 800px; margin: 0 auto; }
h1 { font-size: 1.8rem; background: linear-gradient(135deg, #00d9ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
h2 { color: #00d9ff; margin: 20px 0 10px; }
h3 { color: #a855f7; margin: 15px 0 8px; }
p { line-height: 1.7; margin: 10px 0; color: #bbb; }
code { background: rgba(0,217,255,0.1); color: #00d9ff; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }
table { width: 100%; border-collapse: collapse; margin: 15px 0; }
th, td { border: 1px solid #333; padding: 8px; }
th { background: rgba(0,217,255,0.1); }
tr:nth-child(even) { background: rgba(255,255,255,0.02); }
blockquote { border-left: 3px solid #a855f7; padding: 10px 15px; margin: 15px 0; background: rgba(168,85,247,0.1); border-radius: 0 8px 8px 0; }
blockquote p { color: #ddd; margin: 5px 0; }
li { line-height: 1.8; color: #bbb; margin-left: 20px; }
li code { background: rgba(0,217,255,0.1); color: #00d9ff; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
nav { display: flex; justify-content: space-between; margin-top: 30px; padding-top: 20px; border-top: 1px solid #333; }
a { color: #00d9ff; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none; border-top: 1px solid #333; margin: 20px 0; }
.code-block { background: #111118; border-radius: 8px; overflow: hidden; margin: 15px 0; border: 1px solid #30363d; }
.code-line { display: flex; align-items: center; padding: 12px 16px; cursor: pointer; position: relative; transition: background 0.15s; }
.code-line:hover { background: rgba(255,255,255,0.04); }
.code-line code { background: none; color: #e6edf3; padding: 0; font-family: 'Courier New', monospace; font-size: 13.5px; line-height: 1.5; white-space: pre; flex: 1; overflow-x: auto; }
.copy-btn { margin-left: 12px; background: none; border: 1px solid #30363d; border-radius: 6px; cursor: pointer; padding: 4px 8px; opacity: 0.5; transition: opacity 0.2s, border-color 0.2s; flex-shrink: 0; display: flex; align-items: center; }
.copy-btn:hover { opacity: 1; border-color: #58a6ff; }
.copy-btn.copied { border-color: #238636; opacity: 1; }
.copy-btn svg { width: 14px; height: 14px; fill: #8b949e; display: block; }
.copy-btn.copied svg { fill: #238636; }
</style>
</head>
<body>
<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:15px;margin-bottom:20px;border-bottom:1px solid #333;">
<a href="index.html" style="color:#666;text-decoration:none;">&larr; Sommaire</a>
<span style="font-size:1.2rem;font-weight:700;background:linear-gradient(135deg,#00d9ff,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">SkyLinux</span>
</div>
<div class="container">
'''

NAV_FOOTER = '''
<nav>
PREV_LINK
NEXT_LINK
</nav>
</div>
<script>
function copyCode(el) {
  var code = el.querySelector('code').innerText;
  navigator.clipboard.writeText(code).then(function() {
    el.querySelector('.copy-btn').classList.add('copied');
    setTimeout(function() { el.querySelector('.copy-btn').classList.remove('copied'); }, 1500);
  });
}
document.querySelectorAll('.code-line').forEach(function(el) { el.addEventListener('click', function() { copyCode(el); }); });
</script>
</body>
</html>
'''

def convert_code_block(text):
    def replacer(m):
        code = m.group(1)
        lines = code.strip().split('\n')
        blocks = ['<div class="code-block">']
        for line in lines:
            escaped = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            blocks.append('<div class="code-line" onclick="copyCode(this)"><code>' + escaped + '</code><button class="copy-btn" aria-label="Copier"><svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg></button></div>')
        blocks.append('</div>')
        return '\n'.join(blocks)
    return re.sub(r'```(?:bash)?\n(.*?)```', replacer, text, flags=re.DOTALL)

def convert_inline_code(text):
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    return text

def convert_markdown(text):
    text = convert_code_block(text)
    text = convert_inline_code(text)
    lines = text.split('\n')
    result = []
    in_list = False
    in_blockquote = False
    in_table = False
    
    for line in lines:
        if line.startswith('## '):
            if in_list: result.append('</ul>'); in_list = False
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if in_table: result.append('</table>'); in_table = False
            result.append('<h2>' + line[3:] + '</h2>')
        elif line.startswith('### '):
            if in_list: result.append('</ul>'); in_list = False
            result.append('<h3>' + line[4:] + '</h3>')
        elif line.startswith('- '):
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if in_table: result.append('</table>'); in_table = False
            if not in_list:
                result.append('<ul>'); in_list = True
            result.append('<li>' + line[2:] + '</li>')
        elif line.startswith('|'):
            if in_list: result.append('</ul>'); in_list = False
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if not in_table:
                result.append('<table>'); in_table = True
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(set(c.replace('-','').replace(':','').replace(' ','').replace('+','')) <= set('') or c.startswith(':') for c in cells if c):
                continue
            is_th = result and result[-1] == '<table>'
            tag = '<th>' if is_th else '<td>'
            end = '</th>' if tag == '<th>' else '</td>'
            result.append('<tr>' + ''.join(tag + c + end for c in cells) + '</tr>')
        elif line.startswith('---'):
            if in_list: result.append('</ul>'); in_list = False
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if in_table: result.append('</table>'); in_table = False
            result.append('<hr />')
        elif line.startswith('> '):
            if in_list: result.append('</ul>'); in_list = False
            if in_table: result.append('</table>'); in_table = False
            if not in_blockquote:
                result.append('<blockquote>'); in_blockquote = True
            result.append('<p>' + line[2:] + '</p>')
        else:
            if in_list: result.append('</ul>'); in_list = False
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if in_table: result.append('</table>'); in_table = False
            if line.strip():
                result.append('<p>' + line + '</p>')
    
    if in_list: result.append('</ul>')
    if in_blockquote: result.append('</blockquote>')
    if in_table: result.append('</table>')
    return '\n'.join(result)

def wrap_lesson(filename, title, keywords, prev_link, next_link):
    with open(filename) as f:
        content = f.read()
    
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    actual_title = title_match.group(1) if title_match else title
    content = re.sub(r'^# .+\n', '', content)
    
    html_content = convert_markdown(content)
    
    page = STYLE_HEADER
    page += '<h1>' + actual_title + '</h1>\n'
    page += html_content
    
    prev_nav = ('<a href="' + prev_link + '">&larr; ' + prev_link.split('/')[-1].replace('.html','').replace('-',' ') + '</a>') if prev_link else '<span></span>'
    next_nav = ('<a href="' + next_link + '">' + next_link.split('/')[-1].replace('.html','').replace('-',' ') + ' &rarr;</a>') if next_link else '<span></span>'
    nav = NAV_FOOTER.replace('PREV_LINK', prev_nav).replace('NEXT_LINK', next_nav)
    page += nav
    
    with open(filename, 'w') as f:
        f.write(page)
    print('Processed:', filename)

wrap_lesson(
    '/home/aselophe/linux-debutant/docs/49-journalctl-logs-systemd.html',
    'Leçon 49', 'journalctl, linux, logs systemd, debutant',
    '48-awk-manipuler-texte.html', '50-grep-sed-xargs.html'
)
wrap_lesson(
    '/home/aselophe/linux-debutant/docs/50-grep-sed-xargs.html',
    'Leçon 50', 'grep, sed, xargs, linux, recherche texte, debutant',
    '49-journalctl-logs-systemd.html', '51-sort-uniq-wc.html'
)
wrap_lesson(
    '/home/aselophe/linux-debutant/docs/51-sort-uniq-wc.html',
    'Leçon 51', 'sort, uniq, wc, linux, tri, debutant',
    '50-grep-sed-xargs.html', 'index.html'
)
