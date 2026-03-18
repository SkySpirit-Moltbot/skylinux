#!/usr/bin/env python3
"""
Script de génération HTML pour SkyLinux
Génère les pages HTML à partir des fichiers Markdown avec un template commun.
"""

import os
import re
import glob
from pathlib import Path

# ============ CONFIGURATION ============
REPO_DIR = Path("/home/aselophe/linux-debutant")
DOCS_DIR = REPO_DIR / "docs"

# Titres des leçons (pour la navigation)
LESSONS = {
    "01": "Introduction à Linux",
    "02": "Commandes de base",
    "03": "Permissions Linux",
    "04": "Processus et Services",
    "05": "Installation de logiciels",
    "06": "Réseaux de base",
    "07": "Gestion des fichiers et dossiers",
    "08": "Archivage et compression",
    "09": "Recherche de fichiers et texte",
    "10": "Variables d'environnement et scripts Bash",
    "11": "Surveillance et supervision système",
    "12": "SSH et connexion distante",
    "13": "Tâches planifiées avec Cron",
    "14": "Gestion des utilisateurs et groupes",
    "15": "Redirections et Pipes",
    "16": "Éditeurs de texte en ligne de commande",
    "17": "Les logs système",
    "18": "Gestion des disques et partitions",
    "19": "Sauvegardes et restauration",
    "20": "Sécurité de base sous Linux",
    "21": "Gestion des services avec systemd",
    "22": "Conteneurs Docker",
    "23": "Outils de diagnostic et dépannage",
    "24": "Configuration réseau avancée",
}

# Meta descriptions SEO pour chaque leçon
SEO_META = {
    "01": {"title": "Introduction à Linux - Cours Linux pour débutants | SkyLinux", "desc": "Découvrez Linux, le système d'exploitation gratuit et puissant. Apprenez ce qu'est Linux, pourquoi l'utiliser et les bases du terminal.", "keywords": "linux, introduction, debutant, presentation, pourquoi linux, terminal, shell, distribution, ubuntu, debian"},
    "02": {"title": "Commandes de base Linux - ls, cd, mkdir, rm | SkyLinux", "desc": "Maîtrisez les commandes essentielles de Linux : ls, cd, mkdir, rm, cp, mv, cat, touch.", "keywords": "commandes linux, ls, cd, mkdir, rm, cp, mv, terminal, shell, console, commandes de base"},
    "03": {"title": "Permissions Linux - chmod, chown | SkyLinux", "desc": "Comprenez et maîtrisez les permissions Linux. Apprenez à utiliser chmod, chown.", "keywords": "permissions linux, chmod, chown, rw-r--r--, securite fichiers, droits d'accès"},
    "04": {"title": "Processus et Services Linux - ps, top, kill | SkyLinux", "desc": "Apprenez à gérer les processus sous Linux. Commandes ps, top, htop, kill.", "keywords": "processus linux, ps, top, htop, kill, gestion processus, services, systemctl"},
    "05": {"title": "Installation logiciels Linux - apt, yum | SkyLinux", "desc": "Découvrez comment installer des logiciels sur Linux avec apt, yum, dnf.", "keywords": "installer linux, apt, yum, dnf, pacman, gestionnaire paquets"},
    "06": {"title": "Réseaux de base Linux - ip, ping, netstat | SkyLinux", "desc": "Apprenez les bases du réseau sous Linux. Commandes ip, ping, netstat.", "keywords": "reseau linux, ip, ping, netstat, ifconfig, traceroute, dns"},
    "07": {"title": "Gestion des fichiers Linux - cp, mv, ln, find | SkyLinux", "desc": "Maîtrisez la gestion des fichiers et dossiers sous Linux.", "keywords": "gestion fichiers linux, cp, mv, ln, find, liens symbolique"},
    "08": {"title": "Archivage et compression Linux - tar, gzip, zip | SkyLinux", "desc": "Apprenez à créer des archives et compresser des fichiers.", "keywords": "archivage linux, tar, gzip, bzip2, zip, compression, archive"},
    "09": {"title": "Recherche de fichiers et texte Linux - grep, find | SkyLinux", "desc": "Maîtrisez la recherche sous Linux. Commandes grep, find, locate.", "keywords": "recherche linux, grep, find, locate, awk, sed"},
    "10": {"title": "Variables et scripts Bash Linux | SkyLinux", "desc": "Apprenez à créer des scripts Bash sous Linux.", "keywords": "script bash, shebang, variable bash, automate linux, shell scripting"},
    "11": {"title": "Supervision système Linux - top, free, df | SkyLinux", "desc": "Surveillez votre système Linux avec les commandes de supervision.", "keywords": "supervision linux, top, htop, free, df, du, uptime, performances"},
    "12": {"title": "SSH et connexion distante Linux | SkyLinux", "desc": "Apprenez à vous connecter à distance sur Linux avec SSH.", "keywords": "ssh linux, connexion distante, scp, sftp, cle ssh"},
    "13": {"title": "Tâches planifiées avec Cron Linux | SkyLinux", "desc": "Automatisez vos tâches avec Cron et crontab.", "keywords": "cron linux, crontab, tache planifiee, automatique"},
    "14": {"title": "Gestion utilisateurs et groupes Linux | SkyLinux", "desc": "Gérez les utilisateurs et groupes sous Linux.", "keywords": "utilisateur linux, groupe linux, useradd, usermod, groupadd"},
    "15": {"title": "Redirections et Pipes Linux | SkyLinux", "desc": "Maîtrisez les redirections et pipes sous Linux.", "keywords": "redirection linux, pipe, |, >, >>, tee, chainer commandes"},
    "16": {"title": "Éditeurs de texte Linux - Vim, Nano | SkyLinux", "desc": "Apprenez à utiliser les éditeurs de texte en ligne de commande.", "keywords": "editeur texte linux, vim, nano, vi, editer fichier"},
    "17": {"title": "Les logs système Linux | SkyLinux", "desc": "Analysez les logs système sous Linux.", "keywords": "logs linux, var log, journalctl, dmesg, syslog"},
    "18": {"title": "Gestion des disques et partitions Linux | SkyLinux", "desc": "Gérez les disques et partitions sous Linux.", "keywords": "partition linux, fdisk, lsblk, mkfs, mount, disque"},
    "19": {"title": "Sauvegardes et restauration Linux | SkyLinux", "desc": "Apprenez à créer des sauvegardes et restaurer vos données.", "keywords": "sauvegarde linux, backup, rsync, restauration, tar"},
    "20": {"title": "Sécurité de base sous Linux | SkyLinux", "desc": "Sécurisez votre système Linux.", "keywords": "securite linux, firewall, ufw, iptables, fail2ban"},
    "21": {"title": "Gestion des services avec systemd | SkyLinux", "desc": "Maîtrisez systemd et systemctl pour gérer les services.", "keywords": "systemd, systemctl, service linux, daemon"},
    "22": {"title": "Conteneurs Docker | SkyLinux", "desc": "Découvrez Docker et la conteneurisation sous Linux.", "keywords": "docker, conteneur, container, docker hub, image docker"},
    "23": {"title": "Outils de diagnostic et dépannage Linux | SkyLinux", "desc": "Diagnostiquez et résolvez les problèmes sous Linux.", "keywords": "diagnostic linux, depannage, troubleshooting, strace, lsof"},
    "24": {"title": "Configuration réseau avancée Linux | SkyLinux", "desc": "Maîtrisez la configuration réseau avancée sous Linux.", "keywords": "reseau avance linux, dhcp, dns, iptables, routage"},
}

# ============ TEMPLATES ============

# Template pour le header (commun à toutes les pages de leçon)
HEADER_TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<meta name="robots" content="index, follow">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: Inter, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; padding: 20px; line-height: 1.7; }}
.container {{ max-width: 800px; margin: 0 auto; }}
h1 {{ font-size: 1.8rem; margin-bottom: 20px; color: #00d9ff; }}
h2 {{ font-size: 1.4rem; margin: 30px 0 15px; color: #fff; border-bottom: 1px solid #333; padding-bottom: 8px; }}
h3 {{ font-size: 1.15rem; margin: 20px 0 10px; color: #ddd; }}
p {{ margin: 12px 0; color: #ccc; }}
ul, ol {{ margin: 12px 0; padding-left: 25px; }}
li {{ margin: 6px 0; color: #bbb; }}
code {{ background: #1a1a24; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; color: #ff7b72; }}
pre {{ background: #1a1a24; padding: 15px; border-radius: 8px; overflow-x: auto; margin: 15px 0; border: 1px solid #333; }}
pre code {{ background: none; padding: 0; color: #e0e0e0; }}
table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
th, td {{ padding: 10px; text-align: left; border: 1px solid #333; }}
th {{ background: #1a1a24; color: #00d9ff; }}
hr {{ border: none; border-top: 1px solid #333; margin: 30px 0; }}
blockquote {{ border-left: 3px solid #00d9ff; padding-left: 15px; margin: 15px 0; color: #888; font-style: italic; }}
.header {{ display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; margin-bottom: 20px; border-bottom: 1px solid #333; }}
.header a {{ color: #666; text-decoration: none; }}
.header .logo {{ font-size: 1.2rem; font-weight: 700; background: linear-gradient(135deg, #00d9ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
nav {{ display: flex; justify-content: space-between; margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; }}
nav a {{ color: #00d9ff; text-decoration: none; }}
.footer {{ text-align: center; margin-top: 40px; color: #555; font-size: 0.85rem; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<a href="index.html">&larr; Sommaire</a>
<span class="logo">SkyLinux</span>
</div>
'''

# Footer template
FOOTER_TEMPLATE = '''
<div class="footer">
<p>Par SkyLinux - Cours Linux gratuit</p>
</div>
</div>
</body>
</html>
'''

# Template pour la navigation en bas de page
NAV_TEMPLATE = '''
<nav>
<a href="{prev_link}">&larr; {prev_title}</a>
<a href="{next_link}">{next_title} &rarr;</a>
</nav>
'''

NAV_FIRST_TEMPLATE = '''
<nav>
<a href="index.html">&larr; Sommaire</a>
<a href="{next_link}">{next_title} &rarr;</a>
</nav>
'''

NAV_LAST_TEMPLATE = '''
<nav>
<a href="{prev_link}">&larr; {prev_title}</a>
<span style="color:#666;">Fin</span>
</nav>
'''


def get_md_files():
    """Récupère tous les fichiers MD triés par ordre."""
    files = sorted(glob.glob(str(REPO_DIR / "*.md")))
    return [f for f in files if not f.endswith("BIBLIOGRAPHIE.md") and not f.endswith("README.md")]


def extract_title(content):
    """Extrait le titre de la leçon depuis le contenu Markdown."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1) if match else "Leçon"


def markdown_to_html_simple(content):
    """Conversion simple Markdown vers HTML."""
    html = content
    
    # Titres
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Code blocks
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Code inline
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Gras
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    
    # Listes
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', html)
    
    # Tableaux
    html = re.sub(r'\|(.+)\|\n\|[-|]+\|\n((?:\|.+\|\n?)+)', lambda m: table_to_html(m), html)
    
    # Ligne horizontale
    html = re.sub(r'^---$', '<hr>', html, flags=re.MULTILINE)
    
    # Paragraphes
    html = re.sub(r'\n\n+', '\n', html)
    html = re.sub(r'^(?!<[hupol]|<li|<td|<th|<pre|<div|<span)(.+)$', r'<p>\1</p>', html, flags=re.MULTILINE)
    
    return html


def table_to_html(match):
    """Convertit un tableau Markdown en HTML."""
    lines = match.group(2).strip().split('\n')
    header = match.group(1).split('|')[1:-1]
    
    html = '<table>\n<tr>'
    for h in header:
        html += f'<th>{h.strip()}</th>'
    html += '</tr>\n'
    
    for line in lines:
        cols = [c.strip() for c in line.split('|')[1:-1]]
        html += '<tr>'
        for c in cols:
            html += f'<td>{c}</td>'
        html += '</tr>\n'
    
    html += '</table>'
    return html


def get_lesson_num(filename):
    """Extrait le numéro de leçon du nom du fichier."""
    basename = os.path.basename(filename)
    match = re.match(r'(\d+)', basename)
    return match.group(1) if match else None


def generate_lesson_page(md_file, prev_file, next_file):
    """Génère une page de leçon HTML."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    num = get_lesson_num(md_file)
    title = extract_title(content)
    html_content = markdown_to_html_simple(content)
    
    # Meta SEO
    meta = SEO_META.get(num, {"title": f"{title} | SkyLinux", "desc": title, "keywords": "linux"})
    
    # Navigation
    if prev_file:
        prev_num = get_lesson_num(prev_file)
        prev_title = f"{prev_num} - {LESSONS.get(prev_num, '')}"
        prev_link = os.path.basename(prev_file)
    else:
        prev_title = " Sommaire"
        prev_link = "index.html"
    
    if next_file:
        next_num = get_lesson_num(next_file)
        next_title = f"{next_num} - {LESSONS.get(next_num, '')}"
        next_link = os.path.basename(next_file)
        nav = NAV_TEMPLATE.format(prev_link=prev_link, prev_title=prev_title, next_link=next_link, next_title=next_title)
    else:
        prev_num = get_lesson_num(md_file)
        prev_title = f"{prev_num} - {LESSONS.get(prev_num, '')}"
        nav = NAV_LAST_TEMPLATE.format(prev_link=prev_link, prev_title=prev_title)
    
    # Remplacer le titre dans le contenu
    html_content = re.sub(r'<h1>.*</h1>', f'<h1>{title}</h1>', html_content, count=1)
    
    # Construire la page complète
    page = HEADER_TEMPLATE.format(
        title=meta["title"],
        description=meta["desc"],
        keywords=meta["keywords"]
    )
    page += html_content
    page += nav
    page += FOOTER_TEMPLATE
    
    # Sauvegarder
    output_file = DOCS_DIR / f"{num}-{LESSONS.get(num, 'lecon').lower().replace(' ', '-').replace('é', 'e').replace('è', 'e')}.html"
    # Utiliser le même nom de fichier que maintenant pour éviter les cassures
    md_basename = os.path.basename(md_file)
    html_basename = md_basename.replace('.md', '.html')
    output_file = DOCS_DIR / html_basename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(page)
    
    print(f"✓ {html_basename}")
    return output_file


def main():
    """Point d'entrée principal."""
    print("Génération des pages HTML...\n")
    
    md_files = get_md_files()
    
    for i, md_file in enumerate(md_files):
        prev_file = md_files[i-1] if i > 0 else None
        next_file = md_files[i+1] if i < len(md_files) - 1 else None
        generate_lesson_page(md_file, prev_file, next_file)
    
    print(f"\n✓ Terminé ! {len(md_files)} pages générées dans {DOCS_DIR}/")


if __name__ == "__main__":
    main()