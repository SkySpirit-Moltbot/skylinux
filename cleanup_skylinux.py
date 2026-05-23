#!/usr/bin/env python3
"""
SkyLinux Cleanup Script v2
Fusionne les doublons, renumérote, régénère les HTML.
Backup: ~/.openclaw/backups/skylinux-backup-20260523-1111.tar.gz
"""
import os, re, sys
from pathlib import Path

BASE = Path("/home/aselophe/linux-debutant")
DOCS = BASE / "docs"
TO_DELETE_MD = set()
TO_DELETE_HTML = set()

# ============================================================
# ÉTAPE 1: Fusion Git 29+40
# ============================================================
print("=== ÉTAPE 1: Fusion Git (29+40) ===")
f29 = BASE / "29-git-gestion-version.md"
f40 = BASE / "40-git-gestion-de-versions.md"

if f29.exists() and f40.exists():
    lecon29 = f29.read_text()
    lecon40 = f40.read_text()
    
    # Extraire section "Pourquoi" de 40
    m = re.search(r'(## 1\. Pourquoi.*?)(?=## 2\.)', lecon40, re.DOTALL)
    if m and "Pourquoi Git" not in lecon29:
        lecon29 = lecon29.replace("## 1. Qu'est-ce que Git ?", 
                                   m.group(1).strip() + "\n\n---\n\n## 2. Qu'est-ce que Git ?")
        # Renumérote sections 2→3, 3→4, ..., 12→14, 13→15
        for old, new in [(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,14),(13,15)]:
            lecon29 = re.sub(rf'\n## {old}\. ', f'\n## {new}. ', lecon29)
    
    # Extraire "Commandes utiles du quotidien"
    m2 = re.search(r'(## 8\. Commandes utiles.*?)(?=## Exercice)', lecon40, re.DOTALL)
    if m2 and "Commandes utiles du quotidien" not in lecon29:
        lecon29 = lecon29.replace("## 14. Résumé des commandes", 
                                   m2.group(1).strip() + "\n\n---\n\n## 14. Résumé des commandes")
    
    f29.write_text(lecon29)
    TO_DELETE_MD.add("40-git-gestion-de-versions.md")
    print("  ✅ Git fusionné (29 enrichi, 40 supprimé)")
else:
    print(f"  ⚠️ Fichiers manquants: 29={f29.exists()} 40={f40.exists()}")

# ============================================================
# ÉTAPE 2: Extraction de contenu HTML
# ============================================================
print("\n=== ÉTAPE 2: Extraction HTML pour fusions ===")

def extract_html_sections(html_path):
    """Extrait les sections h2 d'un HTML, retourne texte MD"""
    p = DOCS / html_path
    if not p.exists():
        return None
    html = p.read_text()
    sections = []
    for m in re.finditer(r'<h2>(.*?)</h2>(.*?)(?=<h2>|<nav>|<script>|$)', html, re.DOTALL):
        h2 = m.group(1).strip()
        body = m.group(2)
        texts = []
        for tag in re.finditer(r'<(?:p|li)>(.*?)</(?:p|li)>', body, re.DOTALL):
            t = re.sub(r'<[^>]+>', '', tag.group(1)).strip()
            if t:
                texts.append(t)
        if texts:
            sections.append(f"### {h2}\n\n" + "\n\n".join(texts))
    return sections

def append_section(md_rel, title, html_source):
    """Ajoute une section fusionnée à un fichier MD"""
    mp = BASE / md_rel
    if not mp.exists():
        print(f"    ⚠️ Cible MD manquante: {md_rel}")
        return False
    sections = extract_html_sections(html_source)
    if not sections:
        print(f"    ⚠️ Pas de contenu dans {html_source}")
        return False
    content = mp.read_text()
    if f"## {title}" in content:
        print(f"    ⏭️ Déjà présent: {title}")
        return False
    new_section = f"\n---\n\n## {title}\n\n" + "\n\n".join(sections) + "\n"
    content += new_section
    mp.write_text(content)
    return True

# ============================================================
# ÉTAPE 3: Fusions
# ============================================================
print("\n=== ÉTAPE 3: Exécution des fusions ===")

FUSIONS = [
    # (html_source, md_target, section_title)
    # Cron
    ("73-cron-automatiser-taches.html", "13-taches-planifiees-cron.md", "Complément: Automatisation avancée avec cron"),
    # systemd
    ("55-systemctl-fichiers-unit.html", "21-services-systemd.md", "Complément: Fichiers unit systemd"),
    ("59-systemctl-daemon-reload-mask.html", "21-services-systemd.md", "Complément: daemon-reload et masquage"),
    ("85-systemd-targets-runlevels.html", "35-demarrage-systemd.md", "Complément: Targets et runlevels"),
    # Permissions
    ("56-chmod-chown-permissions-avancees.html", "03-permissions.md", "Complément: Permissions avancées"),
    # Recherche
    ("57-find-recherche-fichiers.html", "09-recherche-fichiers-texte.md", "Complément: find avancé"),
    # SSH
    ("74-openssl-ssh-keygen.html", "12-ssh-connexion-distante.md", "Complément: OpenSSL et clés SSH"),
    # Pare-feu
    ("78-iptables-pare-feu.html", "37-ufw-pare-feu.md", "Complément: iptables"),
    ("79-nftables-pare-feu.html", "37-ufw-pare-feu.md", "Complément: nftables"),
    # Alias
    ("58-alias-fonctions-bash.html", "30-alias-raccourcis.md", "Complément: Fonctions bash"),
    # Utilisateurs
    ("62-useradd-usermod-groupadd.html", "14-gestion-utilisateurs-groupes.md", "Complément: Commandes useradd/usermod"),
    # Processus
    ("82-kill-signaux.html", "11-supervision-systeme.md", "Complément: Signaux et kill"),
    ("72-jobs-processus-arriere-plan.html", "04-processus-services.md", "Complément: Jobs et arrière-plan"),
    # Liens
    ("65-liens-symboliques-pratique.html", "26-liens-symboliques-durs.md", "Complément: Pratique des liens"),
    # Surveillance
    ("64-watch-surveillance-temps-reel.html", "34-surveillance-optimisation-performances.md", "Complément: watch - surveillance temps réel"),
    # Screen
    ("75-screen-multiplexeur-terminal.html", "27-tmux-multiplexeur-terminal.md", "Complément: Screen (alternative à tmux)"),
]

fusion_count = 0
for html_src, md_tgt, title in FUSIONS:
    if append_section(md_tgt, title, html_src):
        fusion_count += 1
        print(f"  ✅ {html_src} → {md_tgt}")
    html_base = html_src.replace(".html", "")
    TO_DELETE_HTML.add(html_src)

# Doublon rsync (52 vs 63, les deux HTML seulement)
if (DOCS / "52-rsync.html").exists() and (DOCS / "63-rsync-synchronisation.html").exists():
    TO_DELETE_HTML.add("63-rsync-synchronisation.html")
    print("  ✅ rsync: 63 supprimé (doublon de 52)")

print(f"  📊 {fusion_count} fusions effectuées")

# ============================================================
# ÉTAPE 4: Extraire MD pour les leçons 49-89 sans source
# ============================================================
print("\n=== ÉTAPE 4: Création MD pour leçons 49-89 ===")

existing_md_nums = set()
for f in BASE.glob("[0-9][0-9]-*.md"):
    existing_md_nums.add(int(f.name[:2]))

def html_to_markdown(html_path, num):
    """Convertit le contenu d'une leçon HTML en Markdown"""
    p = DOCS / html_path
    if not p.exists():
        return None
    html = p.read_text()
    title = ""
    tm = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    if tm:
        title = re.sub(r'<[^>]+>', '', tm.group(1)).strip()
        # Nettoyer les doublons "Leçon XX : Leçon YY :"
        title = re.sub(r'^Leçon \d+\s*:\s*Leçon \d+\s*:', 'Leçon', title)
    
    sections = extract_html_sections(html_path)
    if not sections:
        return None
    
    md = f"# Leçon {num} : {title}\n\n"
    for sec in sections:
        md += sec + "\n\n"
    return md

created = []
for html_file in sorted(DOCS.glob("[5-8][0-9]-*.html")):
    num = int(html_file.name[:2])
    base = html_file.stem
    
    if html_file.name in TO_DELETE_HTML:
        continue
    if num in existing_md_nums:
        continue
    if (BASE / f"{base}.md").exists():
        continue
    
    md_content = html_to_markdown(html_file.name, num)
    if md_content:
        out = BASE / f"{base}.md"
        out.write_text(md_content)
        created.append(out.name)
        print(f"  ✅ {out.name}")

print(f"  📝 {len(created)} nouveaux fichiers MD")

# ============================================================
# ÉTAPE 5: Suppressions
# ============================================================
print("\n=== ÉTAPE 5: Suppression des doublons ===")

for fn in TO_DELETE_MD:
    p = BASE / fn
    if p.exists():
        p.unlink()
        print(f"  🗑️ MD: {fn}")

for fn in TO_DELETE_HTML:
    p = DOCS / fn
    if p.exists():
        p.unlink()
        print(f"  🗑️ HTML: {fn}")

# ============================================================
# ÉTAPE 6: Renumérotation
# ============================================================
print("\n=== ÉTAPE 6: Renumérotation ===")

all_md = sorted(BASE.glob("[0-9][0-9]-*.md"), key=lambda x: int(x.name[:2]))

renamed = 0
for i, md_file in enumerate(all_md, 1):
    new_num = i
    old_num = int(md_file.name[:2])
    
    # Mettre à jour le titre
    content = md_file.read_text()
    content = re.sub(r'^# Leçon \d+\s*:', f'# Leçon {new_num:02d} :', content)
    
    # Renommer si nécessaire
    new_name = re.sub(r'^\d+', f'{new_num:02d}', md_file.name)
    new_path = BASE / new_name
    
    if new_path != md_file:
        md_file.rename(new_path)
        renamed += 1
    
    new_path.write_text(content)

all_md = sorted(BASE.glob("[0-9][0-9]-*.md"), key=lambda x: int(x.name[:2]))
print(f"  📝 {renamed} fichiers renommés, {len(all_md)} leçons total")

# ============================================================
# ÉTAPE 7: Régénération HTML
# ============================================================
print("\n=== ÉTAPE 7: Régénération HTML ===")

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

def md_to_html(md_text):
    """Convertit Markdown en HTML"""
    # Code blocks
    def code_replacer(m):
        code = m.group(1)
        lines = [l for l in code.strip().split('\n') if l.strip()]
        blocks = ['<div class="code-block">']
        for line in lines:
            esc = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            blocks.append(f'<div class="code-line" onclick="copyCode(this)"><code>{esc}</code><button class="copy-btn" aria-label="Copier"><svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg></button></div>')
        blocks.append('</div>')
        return '\n'.join(blocks)
    
    md_text = re.sub(r'```(?:bash|python|sh|console)?\n(.*?)```', code_replacer, md_text, flags=re.DOTALL)
    md_text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', md_text)
    
    lines = md_text.split('\n')
    result = []
    in_list = False
    in_blockquote = False
    in_table = False
    
    for line in lines:
        if line.startswith('### '):
            if in_list: result.append('</ul>'); in_list = False
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if in_table: result.append('</table>'); in_table = False
            result.append('<h3>' + line[4:] + '</h3>')
        elif line.startswith('## '):
            if in_list: result.append('</ul>'); in_list = False
            if in_blockquote: result.append('</blockquote>'); in_blockquote = False
            if in_table: result.append('</table>'); in_table = False
            result.append('<h2>' + line[3:] + '</h2>')
        elif line.startswith('- ') or line.startswith('* '):
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
            if all(set(c.replace('-','').replace(':','').replace(' ','')) <= set('') for c in cells if c):
                continue
            is_th = (len(result) > 0 and result[-1] == '<table>')
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

# Nettoyer les vieux HTML
for old_html in DOCS.glob("[0-9][0-9]-*.html"):
    old_html.unlink()

# Régénérer tous les HTML
all_md = sorted(BASE.glob("[0-9][0-9]-*.md"), key=lambda x: int(x.name[:2]))
n = len(all_md)

for i, md_file in enumerate(all_md):
    content = md_file.read_text()
    
    # Extraire le titre
    tm = re.search(r'^# (.+)$', content, re.MULTILINE)
    actual_title = tm.group(1) if tm else md_file.stem.replace('-', ' ').title()
    content = re.sub(r'^# .+\n', '', content)
    
    html_body = md_to_html(content)
    
    prev_link = next_link = ""
    if i > 0:
        pn = all_md[i-1].name.replace('.md', '.html')
        pt = all_md[i-1].stem
        prev_link = f'<a href="{pn}">&larr; {pt}</a>'
    if i < n - 1:
        nn = all_md[i+1].name.replace('.md', '.html')
        nt = all_md[i+1].stem
        next_link = f'<a href="{nn}">{nt} &rarr;</a>'
    
    nav = NAV_FOOTER.replace('PREV_LINK', prev_link).replace('NEXT_LINK', next_link)
    page = STYLE_HEADER + '<h1>' + actual_title + '</h1>\n' + html_body + nav
    
    (DOCS / md_file.name.replace('.md', '.html')).write_text(page)

print(f"  ✅ {n} HTML régénérés")

# ============================================================
# ÉTAPE 8: Mise à jour index.html
# ============================================================
print("\n=== ÉTAPE 8: Mise à jour index.html ===")

lesson_items = ""
for md_file in all_md:
    content = md_file.read_text()
    tm = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = tm.group(1) if tm else md_file.stem
    html_name = md_file.name.replace('.md', '.html')
    lesson_items += f'        <li><a href="{html_name}">{title}</a></li>\n'

index_path = DOCS / "index.html"
if index_path.exists():
    html = index_path.read_text()
    # Remplacer le <ul> des leçons
    html = re.sub(r'(<ul[^>]*>).*?(</ul>)', f'\\1\n{lesson_items}    \\2', html, flags=re.DOTALL)
    # Mettre à jour le compteur
    html = re.sub(r'\d+ leçons', f'{n} leçons', html)
    index_path.write_text(html)
    print(f"  ✅ index.html mis à jour ({n} leçons)")

# ============================================================
# RÉSUMÉ
# ============================================================
print("\n" + "="*60)
print("RÉSUMÉ DU NETTOYAGE SKYLINUX")
print("="*60)
print(f"  Leçons avant : 89")
print(f"  Leçons après : {n}")
print(f"  Suppressions  : {len(TO_DELETE_MD) + len(TO_DELETE_HTML)} (doublons)")
print(f"  MD créés      : {len(created)}")
print(f"  Fusions       : {fusion_count}")
print(f"  HTML régénérés: {n}")
print("="*60)
print("✅ Terminé !")
