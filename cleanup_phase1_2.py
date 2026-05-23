#!/usr/bin/env python3
"""SkyLinux cleanup script - Phase 1 & 2"""
import os, re, shutil

PROJ = "/home/aselophe/linux-debutant"
MD = PROJ
HTML = f"{PROJ}/docs"

def md(name): return f"{MD}/{name}.md"
def html(name): return f"{HTML}/{name}.html"
def rm_md(n): p = md(n); os.path.exists(p) and os.remove(p)
def rm_html(n): p = html(n); os.path.exists(p) and os.remove(p)

def add_to_section(md_path, section_title, content_lines):
    """Add a new section (## title) to an existing MD file, before any existing ##."""
    with open(md_path) as f:
        content = f.read()
    # Find position to insert (before first ## that is not the main title)
    lines = content.split('\n')
    insert_idx = None
    for i, line in enumerate(lines):
        if line.startswith('## ') and i > 0:
            insert_idx = i
            break
    if insert_idx is None:
        # append before the summary or at end
        for i in range(len(lines)-1, -1, -1):
            if lines[i].startswith('## '):
                insert_idx = i + 1
                break
        if insert_idx is None:
            insert_idx = len(lines)
    
    section = [f"## {section_title}"] + content_lines + ['']
    lines = lines[:insert_idx] + section + lines[insert_idx:]
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines))

def append_to_md(md_path, content_lines):
    """Append content to the end of an MD file."""
    with open(md_path) as f:
        content = f.read()
    if content and not content.endswith('\n'):
        content += '\n'
    content += '\n'.join(content_lines) + '\n'
    with open(md_path, 'w') as f:
        f.write(content)

# ─────────────────────────────────────────────
# PHASE 1.1 : Git merge (29 + 40 → 29)
# ─────────────────────────────────────────────
print("=== PHASE 1.1: Git merge 29+40 ===")
# 29 already has comprehensive content.
# Add unique content from 40 (the "pourquoi" intro, git diff section)
# Section: "Pourquoi un outil de gestion de versions" - very visual story
extra_git = """## 14. Pourquoi un outil de gestion de versions ?

Voici ce qui se passe sans Git :

```text
Tu modifies script.sh
  → Tu ajoutes une fonctionnalité
  → Ça casse tout
  → Tu n'as plus la version qui marchait
  → Panique
```

**Avec Git**, chaque modification est enregistrée. Tu peux revenir à n'importe quel moment, voir exactement ce qui a changé, et travailler avec d'autres personnes sans écraser leur travail.

## 15. La commande git diff

Voir exactement ce qui a changé :

```bash
git diff              # montre les modifications NON indexées
git diff --cached     # montre les modifications indexées (prêtes à valider)
```

Exemple de sortie :

```text
- ancienne_ligne
+ nouvelle_ligne_plus_belle
```

Le `-` = ligne enlevée, le `+` = ligne ajoutée. Indispensable pour relire avant de commiter !

## 16. Workflow quotidien complet

Le cycle de travail typique avec Git :

```bash
# 1. Tu modifies tes fichiers
nano config.txt

# 2. Tu vérifies ce qui a changé
git status        # quels fichiers modifiés
git diff          # détails des changements (lignes ajoutées/enlevées)

# 3. Tu ajoutes les fichiers modifiés à l'index
git add config.txt

# 4. Tu valides avec un message clair
git commit -m "Mise à jour de la configuration serveur"
```
"""
append_to_md(md('29-git-gestion-version'), [extra_git])
# Delete 40
rm_md('40-git-gestion-de-versions')
# Delete 40.html (if exists) and all HTML for deleted MD
rm_html('40-git-gestion-de-versions')
print("  ✓ Merged 40 into 29, deleted 40-git-gestion-de-versions.md and HTML")

# ─────────────────────────────────────────────
# PHASE 1.2 : rsync merge (52+63 → 52)
# ─────────────────────────────────────────────
print("=== PHASE 1.2: rsync merge 52+63 ===")
# 63-rsync-synchronisation.html has content. Need to create 52-rsync.md from it.
# Both 52 and 63 exist as HTML. We'll create a unified 52-rsync.md.
# 52 HTML has the core rsync content. 63 HTML has extra examples.
# Create comprehensive 52-rsync.md from both HTMLs.
rsync_md = """# Leçon 52 : rsync — Synchronisation de fichiers

Dans cette leçon, tu vas maîtriser **rsync** pour synchroniser efficacement des fichiers et répertoires en local ou à distance. C'est l'outil de référence pour les sauvegardes et la copie incrémentale.

---

## 1. Pourquoi rsync ?

- Ne copie que les **fichiers modifiés** (transfert incrémental)
- Beaucoup plus rapide que `cp` pour les gros transferts
- Compression intégrée pour réduire la bande passante
- Supporte SSH pour des transferts sécurisés
- Peut reprendre un transfert interrompu

---

## 2. Syntaxe de base

```bash
rsync [options] SOURCE DESTINATION
```

---

## 3. Options essentielles

| Option | Description |
|--------|-------------|
| `-a` | Mode archive (preserve permissions, owner, timestamps) |
| `-v` | Mode verbeux (affiche les fichiers) |
| `-z` | Compression pendant le transfert |
| `-P` | Montre la progression et permet la reprise |
| `-n` | Mode dry-run (simulation, sans copier) |
| `--delete` | Supprime les fichiers dans DEST qui n'existent plus dans SOURCE |
| `--exclude` | Exclut certains fichiers/répertoires |

---

## 4. Exemples pratiques

### Copie locale simple

```bash
# Synchroniser un répertoire vers un autre
rsync -av /home/david/documents/ /backup/documents/

# Avec barre de progression
rsync -avP /home/david/documents/ /backup/documents/
```

### Transfert via SSH

```bash
# Copier vers un serveur distant
rsync -avz -e ssh /local/dir/ user@serveur:/remote/dir/

# Récupérer depuis un serveur distant
rsync -avz -e ssh user@serveur:/remote/dir/ /local/dir/
```

### Simulation avant action

```bash
# Voir ce qui sera copié sans rien modifier
rsync -avn /source/ /dest/
```

### Exclure des fichiers

```bash
# Exclure un type de fichier
rsync -av --exclude='*.log' /source/ /dest/

# Exclure plusieurs patterns
rsync -av --exclude='*.tmp' --exclude='.git' --exclude='node_modules/' /source/ /dest/
```

### Synchronisation miroir (identique)

```bash
# Supprime les fichiers absents de la source
rsync -av --delete /source/ /dest/
```

---

## 5. Les slashs comptent !

Attention à la présence ou l'absence du `/` final :

| Syntaxe | Comportement |
|---------|-------------|
| `rsync -a /source /dest` | Crée `/dest/source/` |
| `rsync -a /source/ /dest` | Crée `/dest/` (contenu de source) |

---

## 6. Sauvegarde quotidienne classique

```bash
# Script de sauvegarde vers un serveur de backup
rsync -avz --delete -e ssh /home/david/ user@backup-server:/backup/david/
```

---

## 7. Cas d'usage courants

### Déployer un site web

```bash
rsync -avz --delete ./dist/ user@monsite:/var/www/html/
```

### Sauvegarder un serveur vers un NAS

```bash
rsync -avz -e ssh root@monserveur:/var/www/ /mnt/nas/serveur/www/
```

### Déployer une configuration

```bash
rsync -avz -e ssh /home/david/.config/ user@serveur:/home/david/.config/
```

---

## 8. Bonnes pratiques

- Toujours faire un **dry-run** (`-n`) avant une première synchro
- Utiliser `-P` pour les gros transferts (reprise si coupure)
- Protéger les transferts distants avec **SSH**
- Utiliser `--delete` avec prudence en mode miroir

---

## 9. Exercices pratiques

1. **Copie locale** — Synchronise ton dossier `~/Documents` vers `/tmp/backup-documents/` en mode verbeux.
2. **Simulation** — Utilise `-n` pour voir ce qui serait copié sans rien modifier.
3. **Exclusion** — Synchronise un dossier en excluant tous les fichiers `.log` et le dossier `.git`.
4. **Sauvegarde distante** — Si tu as accès SSH à une machine, synchronise un petit dossier via SSH.

---

## 10. Résumé

| Commande | Usage |
|----------|-------|
| `rsync -av source/ dest/` | Synchronisation locale |
| `rsync -avz -e ssh src/ user@host:dst/` | Transfert via SSH |
| `rsync -avP src/ dst/` | Avec progression et reprise |
| `rsync -avn src/ dst/` | Dry-run (simulation) |
| `rsync -av --exclude='*.log' src/ dst/` | Avec exclusions |
| `rsync -av --delete src/ dst/` | Mirroring (synchro exacte) |
"""
with open(md('52-rsync'), 'w') as f:
    f.write(rsync_md)
rm_html('63-rsync-synchronisation')
print("  ✓ Created 52-rsync.md, deleted 63-rsync-synchronisation.html")

# ─────────────────────────────────────────────
# PHASE 1.3 : Cron merge (13+73 → 13)
# ─────────────────────────────────────────────
print("=== PHASE 1.3: Cron merge 13+73 ===")
# Content from 73 to add to 13:
cron_extra = """## 11. Le service cron (systemd)

Sur les systèmes utilisant **systemd**, le service cron s'appelle généralement `cron` ou `crond`. Il tourne en arrière-plan et vérifie toutes les minutes s'il doit exécuter une tâche.

```bash
# Vérifier que cron tourne
systemctl status cron

# Le démarrer automatiquement au boot
systemctl enable cron

# Démarrer maintenant
systemctl start cron

# Redémarrer après modification
systemctl restart cron
```

## 12. Jours de la semaine dans cron

| Valeur | Jour |
|--------|------|
| `0` | Dimanche |
| `1` | Lundi |
| `2` | Mardi |
| `3` | Mercredi |
| `4` | Jeudi |
| `5` | Vendredi |
| `6` | Samedi |
| `7` | Dimanche |

## 13. Éditeurs et sélection

```bash
# Sélectionner nano par défaut
select-editor

# Ou forcer nano
EDITOR=nano crontab -e
```

## 14. Crontab système

```bash
# Emplacements système
/etc/crontab           # Crontab principale du système
/etc/cron.d/           # Fichiers cron supplémentaires
/etc/cron.daily/       # Scripts exécutés quotidiennement
/etc/cron.hourly/      # Scripts exécutés chaque heure
/etc/cron.weekly/      # Scripts exécutés chaque semaine
/etc/cron.monthly/     # Scripts exécutés chaque mois

# Format système (inclut l'utilisateur) :
# 0 3 * * * root /opt/scripts/backup.sh
```

## 15. Restriction d'accès (cron.allow / cron.deny)

```bash
# Autoriser certains utilisateurs
sudo nano /etc/cron.allow
# david
# marie

# Interdire certains utilisateurs
sudo nano /etc/cron.deny
# guest
# testuser
```

## 16. Vérifier le fonctionnement

```bash
# Voir les dernières entrées du journal systemd
journalctl -u cron -e

# Ou via syslog
grep CRON /var/log/syslog

# Lister les tâches cron actives
sudo systemctl status cron
```
"""
append_to_md(md('13-taches-planifiees-cron'), [cron_extra])
rm_html('73-cron-automatiser-taches')
print("  ✓ Merged 73 into 13, deleted 73 HTML")

# ─────────────────────────────────────────────
# PHASE 1.5 : systemd merge
#   21+55+59 → 21   (services + unit files + daemon-reload)
#   35+85 → 35      (boot + targets)
# ─────────────────────────────────────────────
print("=== PHASE 1.5: systemd merges ===")

# 21 + 55 + 59 → 21
systemd_21_extra = """## 7. Les types de fichiers Unit

Un fichier unit définit une unité de travail pour systemd. Il existe plusieurs types :

| Type | Extension | Description |
|------|-----------|-------------|
| `Service` | .service | Démarre un processus (nginx, apache, mysql...) |
| `Socket` | .socket | Un socket, déclenche un service à la connexion |
| `Timer` | .timer | Planification temporelle (comme cron) |
| `Path` | .path | Surveille un fichier/répertoire et déclenche un service |
| `Mount` | .mount | Monte un système de fichiers |
| `Target` | .target | Groupe d'unités (runlevels modernes) |

## 8. Où se trouvent les fichiers Unit ?

```bash
/etc/systemd/system/    # Unités personnalisées (admin) — priorité haute
/run/systemd/system/     # Unités runtime (temporaire)
/usr/lib/systemd/system/  # Installées par les paquets — priorité basse
```

## 9. Structure d'un fichier Unit

```bash
# Examiner un fichier existant
cat /lib/systemd/system/sshd.service
```

**Section [Unit]** — Métadonnées et dépendances :

```
[Unit]
Description=Mon service personnalisé
After=network.target mysql.service    # Démarre APRÈS ces unités
Before=nginx.service                 # Démarre AVANT cette unité
Requires=mysql.service               # Dépendance stricte
Wants=redis.service                 # Dépendance souple
```

**Section [Service]** — Configuration du processus :

```
[Service]
Type=simple              # Le programme ne fait pas de fork (défaut)
Type=forking             # Le programme fait un fork (PID attendu)
Type=oneshot             # Une seule exécution puis s'arrête
Type=notify              # Le programme notifie systemd quand prêt

ExecStart=/usr/bin/mon_script.sh    # Commande de démarrage
ExecStop=/usr/bin/mon_script.sh --stop  # Commande d'arrêt
ExecReload=/bin/kill -HUP $MAINPID  # Commande de reload

Restart=always        # Redémarre en cas d'échec
Restart=on-failure     # Redémarre uniquement en cas d'erreur
Restart=no             # Ne redémarre jamais
RestartSec=5           # Pause de 5 secondes avant redémarrage

User=www-data          # Utilisateur qui exécute le processus
Environment="PORT=8080" "ENV=prod"  # Variables d'environnement
WorkingDirectory=/var/www    # Répertoire de travail
```

**Section [Install]** — Comportement au démarrage :

```
[Install]
WantedBy=multi-user.target    # S'active au boot en mode multi-utilisateur
Also=autre-service.service    # Active/désactive aussi cette unité
```

## 10. Créer son propre service

```bash
# 1. Créer le script
sudo nano /opt/monapp/mon_script.sh
chmod +x /opt/monapp/mon_script.sh

# 2. Créer le fichier unit
sudo nano /etc/systemd/system/monapp.service
```

Contenu de `monapp.service` :

```
[Unit]
Description=Mon application personnalisée
After=network.target

[Service]
Type=simple
ExecStart=/opt/monapp/mon_script.sh
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
```

```bash
# 3. Activer le service
sudo systemctl daemon-reload
sudo systemctl enable --now monapp
systemctl status monapp
```

## 11. Commandes avancées systemctl

```bash
# Relancer (stop + start)
sudo systemctl try-restart nginx

# Masquer (rend impossible à démarrer)
sudo systemctl mask nginx
sudo systemctl unmask nginx

# Forcer l'arrêt
sudo systemctl kill -s SIGTERM monapp

# Voir si activé / actif
systemctl is-enabled nginx
systemctl is-active nginx

# Lister tous les services
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service

# Voir les dépendances
systemctl list-dependencies nginx

# Voir le fichier unit chargé
systemctl cat nginx

# Voir les propriétés
systemctl show nginx | grep -E "MainPID|ExecStart|LoadState"
```

## 12. daemon-reload — Pourquoi et quand ?

**Quand daemon-reload est nécessaire :**

| Action | daemon-reload nécessaire ? |
|--------|---------------------------|
| Modifier un fichier .service existant | ✅ Oui |
| Ajouter un nouveau fichier .service | ✅ Oui |
| Modifier via `systemctl edit` | ❌ Non (fait automatiquement) |
| Supprimer un fichier unit | ✅ Oui |

```bash
# Après toute modification :
sudo systemctl daemon-reload
sudo systemctl restart mon-service
```

## 13. Les Targets (cibles) principales

| Target | Description |
|--------|-------------|
| `poweroff.target` | Arrêt complet |
| `rescue.target` | Mode rescue (single user) |
| `multi-user.target` | Multi-utilisateurs, sans GUI |
| `graphical.target` | Multi-utilisateurs avec GUI |
| `reboot.target` | Redémarrage |
| `emergency.target` | Mode emergency (shell minimal) |

```bash
# Voir la target par défaut
systemctl get-default

# Définir la target par défaut
sudo systemctl set-default multi-user.target

# Changer de target à chaud
sudo systemctl isolate multi-user.target

# Lister toutes les targets
systemctl list-units --type=target --all
```

## 14. Bonnes pratiques

- Toujours utiliser `sudo systemctl daemon-reload` après toute modification de fichier unit
- Ne **jamais** éditer directement les fichiers dans `/usr/lib/systemd/`
- Préférer `EnvironmentFile` pour les variables sensibles
- Ne faire tourner un service en root que si nécessaire
- Toujours vérifier avec `systemctl status` après chaque action
"""
append_to_md(md('21-services-systemd'), [systemd_21_extra])
rm_html('55-systemctl-fichiers-unit')
rm_html('59-systemctl-daemon-reload-mask')
print("  ✓ Merged 55+59 into 21")

# 35 + 85 → 35
systemd_35_extra = """## 7. Les targets systemd (runlevels)

Les **targets** systemd sont l'équivalent moderne des runlevels SysVinit. Elles définissent un état du système.

### Targets principales

| Target | Équivalent SysV | Description |
|--------|-----------------|-------------|
| `poweroff.target` | Runlevel 0 | Arrêt complet |
| `rescue.target` | Runlevel 1 | Mode rescue (single user) |
| `multi-user.target` | Runlevel 2, 3, 4, 5 | Multi-utilisateurs, sans GUI |
| `graphical.target` | Runlevel 5 | Multi-utilisateurs avec GUI |
| `reboot.target` | Runlevel 6 | Redémarrage |
| `emergency.target` | — | Mode emergency (shell minimal) |

### Commandes targets

```bash
# Définir la target par défaut
sudo systemctl set-default multi-user.target

# Changer de target à chaud
sudo systemctl isolate multi-user.target

# Mode rescue / emergency
sudo systemctl rescue
sudo systemctl emergency

# Arrêter / redémarrer via systemd
sudo systemctl poweroff
sudo systemctl reboot

# Voir les dépendances d'une target
systemctl list-dependencies graphical.target

# Lister les targets
systemctl list-units --type=target --all
```

### Targets vs Runlevels

| Aspect | SysVinit | systemd |
|--------|----------|---------|
| Changement | `init 3` | `systemctl isolate multi-user.target` |
| Parallélisme | Séquentiel | Parallèle (plus rapide) |
| Configuration | `/etc/rc.d/` | Fichiers dans `/etc/systemd/` |

## 8. Targets et emergency/rescue

```bash
# Mode rescue — comme init 1
sudo systemctl rescue

# Mode emergency — root filesystem en lecture seule
sudo systemctl emergency

# Sortie : Ctrl+D ou exit pour revenir
```

## 9. Créer une target personnalisée

```bash
sudo nano /etc/systemd/system/mon-service.target
```

```
[Unit]
Description=Ma target personnalisée
After=network-online.target
Wants=network-online.target

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mon-service.target
```
"""
append_to_md(md('35-demarrage-systemd'), [systemd_35_extra])
rm_html('85-systemd-targets-runlevels')
print("  ✓ Merged 85 into 35")

# ─────────────────────────────────────────────
# PHASE 1.6 : Delete screen duplicate (75)
# ─────────────────────────────────────────────
print("=== PHASE 1.6: Delete screen duplicate ===")
rm_html('75-screen-multiplexeur-terminal')
print("  ✓ Deleted 75-screen-multiplexeur-terminal.html")

# ─────────────────────────────────────────────
# PHASE 2.1 : Permissions merge (03 + 56 → 03)
# ─────────────────────────────────────────────
print("=== PHASE 2: Overlap merges ===")
perms_extra = """## 8. Permissions spéciales (sticky bit, SUID, SGID)

### Sticky bit

Le **sticky bit** sur un répertoire fait que seuls le propriétaire d'un fichier peuvent le supprimer.

```bash
# Exemple : /tmp a le sticky bit
ls -ld /tmp
# drwxrwxrwt ... /tmp (le t final = sticky bit)

# Ajouter le sticky bit
chmod +t /mon/repertoire/
chmod 1775 /mon/repertoire/

# Retirer le sticky bit
chmod -t /mon/repertoire/
```

Utile pour les répertoires partagés où tout le monde peut écrire.

### SUID (Set User ID)

Quand un fichier a le **SUID**, il s'exécute avec les droits de son propriétaire, pas de l'utilisateur qui le lance.

```bash
# Exemple : passwd a le SUID (pour écrire /etc/shadow)
ls -l /usr/bin/passwd
# -rwsr-xr-x 1 root root ... /usr/bin/passwd
#     ^ le s au lieu de x = SUID

# Ajouter le SUID
chmod u+s /chemin/vers/binaire
chmod 4755 /chemin/vers/binaire

# Retirer le SUID
chmod u-s /chemin/vers/binaire
```

⚠️ **Très dangereux** sur un serveur : à utiliser avec extrema prudence.

### SGID (Set Group ID)

Le **SGID** fonctionne comme le SUID mais pour les groupes. Sur un répertoire, tous les fichiers créés héritent du groupe du répertoire.

```bash
# Exemple : répertoire de projet partagé
chmod g+s /home/projet/

# Ajouter le SGID
chmod g+s /chemin/vers/repertoire
chmod 2775 /chemin/vers/repertoire

# Vérifier
ls -ld /home/projet/
# drwxrwsr-x ... /home/projet/  (le s au lieu de x sur groupe)
```

### Résumé sticky/SUID/SGID

| Bit | Octal | Effet |
|-----|-------|-------|
| Sticky | 1xxx | Empêche suppression par non-propriétaire |
| SUID | 4xxx | Exécuter avec droits du propriétaire |
| SGID | 2xxx | Hériter du groupe + exécuter avec droits du groupe |

```bash
# Exemple complet : répertoire partagé sécurisé
chmod 3775 /home/projet/
# 3 = sticky bit (1) + SGID (2)
# 7 = rwx pour propriétaire
# 7 = rwx pour groupe
# 5 = rx pour autres (pas de droit d'écriture)
```

## 9. Umask — Permissions par défaut

L'**umask** définit les permissions retirées par défaut lors de la création d'un fichier ou répertoire.

```bash
# Voir l'umask actuel
umask

# L'umask par défaut est généralement 022
# Pour un fichier : 666 - 022 = 644 (rw-r--r--)
# Pour un répertoire : 777 - 022 = 755 (rwxr-xr-x)

# Modifier l'umask (session actuelle)
umask 027   # rw-r----- (plus restrictif)
umask 077   # rw------- (très restrictif)

# Rendre permanent : ajouter dans ~/.bashrc ou /etc/profile
echo "umask 027" >> ~/.bashrc
source ~/.bashrc
```

### Umask et sécurité

| Umask | Fichiers | Répertoires | Usage |
|-------|----------|-------------|-------|
| 022 | 644 rw-r--r-- | 755 rwxr-xr-x | Standard |
| 027 | 640 rw-r----- | 750 rwxr-x--- | Partagé |
| 077 | 600 rw------- | 700 rwx------ | Privé |

## 10. Modifier les propriétaires et groupes

### Changer le propriétaire

```bash
# Changer le propriétaire d'un fichier
sudo chown utilisateur fichier

# Changer récursivement
sudo chown -R utilisateur /chemin/

# Changer propriétaire ET groupe
sudo chown utilisateur:groupe fichier
```

### Changer le groupe

```bash
# Changer le groupe d'un fichier
sudo chgrp groupe fichier

# Changer récursivement
sudo chgrp -R groupe /chemin/

# Vérifier
ls -l fichier
```

### Exemples pratiques

```bash
# Donner un site web à l'utilisateur www-data
sudo chown -R www-data:www-data /var/www/monsite/

# Répertoire de projet partagé par un groupe
sudo groupadd projet-team
sudo usermod -aG projet-team david
sudo chgrp -R projet-team /home/projet/
chmod -R 2770 /home/projet/
```

## 11. Notation numérique des permissions

| Notation | Signification | Usage |
|----------|---------------|-------|
| `777` | rwxrwxrwx | Tout accessible |
| `755` | rwxr-xr-x | Scripts exécutables |
| `644` | rw-r--r-- | Fichiers normaux |
| `600` | rw------- | Fichiers privés |
| `4755` | rwsr-xr-x | SUID (execute as owner) |
| `2755` | rwxr-sr-x | SGID (inherit group) |
| `1777` | rwxrwxrwt | Sticky bit (no delete) |

```bash
# Exemples
chmod 755 script.sh       # rwxr-xr-x
chmod 644 document.txt    # rw-r--r--
chmod 600 clef-secrete    # rw-------
chmod 4755 /usr/bin/passwd  # SUID
```
"""
append_to_md(md('03-permissions'), [perms_extra])
rm_html('56-chmod-chown-permissions-avancees')
print("  ✓ Merged 56 into 03")

# ─────────────────────────────────────────────
# PHASE 2.2 : find merge (09 + 57 → 09)
# ─────────────────────────────────────────────
find_extra = """## 9. La commande find — Rechercher des fichiers

`find` permet de rechercher des fichiers selon de nombreux critères : nom, type, date, taille, permissions...

### Syntaxe de base

```bash
find répertoire critères action
```

### Rechercher par nom

```bash
# Par nom exact
find /home -name "rapport.txt"

# Par pattern (insensible à la casse)
find /home -iname "*.pdf"

# Recherche par expression
find . -name "*.log" -o -name "*.tmp"
```

### Rechercher par type

```bash
find /home -type f          # Fichiers seulement
find /home -type d          # Répertoires seulement
find /home -type l          # Liens symboliques seulement
find /home -type s          # Sockets
find /home -type p          # Pipes
```

### Rechercher par date

```bash
find /home -mtime -7        # Modifiés dans les 7 derniers jours
find /home -mtime 7         # Modifiés il y a exactement 7 jours
find /home -mtime +30       # Modifiés il y a plus de 30 jours

find /home -atime -1        # Accédés dans les dernières 24h
find /home -ctime -3        # Changés (métadonnées) dans les 3 derniers jours
```

### Rechercher par taille

```bash
find /home -size +100M      # Plus de 100 Mo
find /home -size -1G        # Moins de 1 Go
find /home -size 10M        # Exactement 10 Mo (tolérance 10M)
```

### Rechercher par permissions

```bash
find /home -perm 644         # Exactement 644
find /home -perm -u=x       # Exécutables par le propriétaire
find /home -perm /u+w       # Au moins writable par owner
```

### Actions sur les résultats

```bash
# Afficher les détails (-ls = comme ls -l)
find /home -name "*.txt" -ls

# Afficher le nombre
find /home -name "*.txt" | wc -l

# Exécuter une commande sur chaque résultat (-exec)
find /home -name "*.tmp" -exec rm {} \;
# {} = le fichier trouvé, \; = fin de la commande

# Demander confirmation (-ok, comme -exec mais avec ask)
find /home -name "*.log" -ok rm {} \;

# Supprimer les fichiers trouvés
find /home -name "*.bak" -delete

# Copier les résultats
find /home -name "*.jpg" -exec cp {} /backup/photos/ \;
```

### Combiner plusieurs critères

```bash
# ET (les deux conditions)
find /home -name "*.pdf" -size +5M

# OU (l'un ou l'autre)
find /home \( -name "*.log" -o -name "*.tmp" \)

# NOT (inversion)
find /home -not -name "*.py"

# Par date ET par nom
find /home -name "*.txt" -mtime -7
```

### Exemples pratiques complets

```bash
# Trouver tous les fichiers de plus de 100 Mo dans /home
find /home -type f -size +100M -ls

# Supprimer les fichiers .log de plus de 30 jours
find /var/log -name "*.log" -mtime +30 -delete

# Trouver les fichiers modifiés aujourd'hui
find /home -mtime 0 -ls

# Trouver les fichiers exécutables
find /home -type f -perm /u=x -ls

# Archiver les fichiers de plus de 1 an
find /home -mtime +365 -exec tar -czf archive.tar.gz {} +
```
"""
# Find the best insertion point - before any "##" that is beyond standard content
append_to_md(md('09-recherche-fichiers-texte'), [find_extra])
rm_html('57-find-recherche-fichiers')
print("  ✓ Merged 57 into 09")

# ─────────────────────────────────────────────
# PHASE 2.3 : SSH keys merge (12 + 74 → 12)
# ─────────────────────────────────────────────
ssh_keys_extra = """## 8. Générer des clés SSH (ssh-keygen)

La **clé SSH** permet de s'authentifier sans mot de passe. Plus sécurisé et plus pratique.

### Générer une paire de clés

```bash
# Clé RSA (compatible partout)
ssh-keygen -t rsa -b 4096 -C "contact@hinni-swiss.com"

# Clé Ed25519 (recommandée, plus moderne et rapide)
ssh-keygen -t ed25519 -C "contact@hinni-swiss.com"

# Clé RSA avec commentaire personnalisé
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_perso -C "mon-email@exemple.com"
```

### Les questions de ssh-keygen

```
Enter file in which to save the key (/home/david/.ssh/id_rsa):  [Entrée]
Enter passphrase (empty for no passphrase):                     [mot de passe]
Enter same passphrase again:                                   [confirmation]
```

> 💡 Utilise une passphrase vide seulement pour les serveurs internes. Pour tout le reste, utilise une passphrase forte — tu peux utiliser `ssh-agent` pour ne la saisir qu'une fois.

### Emplacements par défaut

| Type | Clé privée | Clé publique |
|------|-----------|-------------|
| RSA | `~/.ssh/id_rsa` | `~/.ssh/id_rsa.pub` |
| Ed25519 | `~/.ssh/id_ed25519` | `~/.ssh/id_ed25519.pub` |
| ECDSA | `~/.ssh/id_ecdsa` | `~/.ssh/id_ecdsa.pub` |

### Vérifier ses clés

```bash
ls -la ~/.ssh/
# -rw------- id_rsa       (clé privée, permissions 600)
# -rw-r--r-- id_rsa.pub   (clé publique)
```

## 9. Déployer sa clé publique sur le serveur

```bash
# Méthode automatique (ssh-copy-id)
ssh-copy-id user@serveur

# Méthode manuelle
cat ~/.ssh/id_rsa.pub | ssh user@serveur "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Vérifier que ça fonctionne
ssh user@serveur
```

### authorized_keys — Le fichier des clés autorisées

```bash
# Voir les clés autorisées sur un serveur
cat ~/.ssh/authorized_keys

# Format d'une ligne :
# ssh-ed25519 AAAAC3... mon-commentaire
```

## 10. Options avancées de ssh-keygen

```bash
# Spécifier un nom et emplacement personnalisé
ssh-keygen -t ed25519 -f ~/.ssh/serveur-dedie -C "serveur-prod"

# Générer une clé sans passphrase (pour les scripts)
ssh-keygen -t ed25519 -f ~/.ssh/backup-key -N ""

# Changer la passphrase d'une clé existante
ssh-keygen -p -f ~/.ssh/id_ed25519

# Fingerprint d'une clé (voir si c'est la bonne)
ssh-keygen -lf ~/.ssh/id_ed25519.pub

# Combien de bits pour une clé RSA
ssh-keygen -t rsa -b 8192 -C "ultra-securise"
```

## 11. ssh-agent — Ne saisir la passphrase qu'une fois

```bash
# Démarrer ssh-agent pour la session
eval "$(ssh-agent -s)"

# Ajouter sa clé (demande la passphrase)
ssh-add ~/.ssh/id_ed25519

# Lister les clés chargées
ssh-add -l

# Ajouter toutes les clés
ssh-add ~/.ssh/id_ed25519 ~/.ssh/serveur-dedie
```
"""
append_to_md(md('12-ssh-connexion-distante'), [ssh_keys_extra])
rm_html('74-openssl-ssh-keygen')
print("  ✓ Merged 74 into 12")

# ─────────────────────────────────────────────
# PHASE 2.4 : Firewall merge (37 + 78 + 79 → 37)
# ─────────────────────────────────────────────
firewall_extra = """## 8. Autres pare-feu : iptables et nftables

UFW est un wrapper simplifié. Pour un contrôle fin, il faut iptables ou nftables.

### iptables — Le pare-feu classique

```bash
# Voir les règles actuelles
sudo iptables -L -n -v

# Règle de base : tout bloquer en entrée, laisser sortir
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Autoriser localhost
sudo iptables -A INPUT -i lo -j ACCEPT

# Autoriser une IP spécifique
sudo iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# Autoriser un port (SSH)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Autoriser HTTP/HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Limiter les connexions SSH (anti brute-force)
sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP

# Supprimer une règle
sudo iptables -D INPUT -p tcp --dport 22 -j ACCEPT
```

### Sauvegarder les règles iptables

```bash
# Ubuntu : installer iptables-persistent
sudo apt install iptables-persistent

# Sauvegarder
sudo netfilter-persistent save

# Sur Debian/Ubuntu ancien :
sudo sh -c "iptables-save > /etc/iptables/rules.v4"
```

### nftables — Le remplaçant moderne

`nftables` est le remplaçant de iptables, plus performant et plus flexible.

```bash
# Installer
sudo apt install nftables

# Démarrer
sudo systemctl enable nftables
sudo systemctl start nftables

# Voir les règles
sudo nft list ruleset

# Créer une table
sudo nft add table inet filter

# Créer des chaînes
sudo nft add chain inet filter input '{ type filter hook input priority 0; policy drop; }'
sudo nft add chain inet filter output '{ type filter hook output priority 0; policy accept; }'

# Autoriser localhost
sudo nft add rule inet filter input iif lo accept

# Autoriser SSH
sudo nft add rule inet filter input tcp dport 22 accept

# Autoriser HTTP/HTTPS
sudo nft add rule inet filter input tcp dport { 80, 443 } accept

# Autoriser ping (icmp)
sudo nft add rule inet filter input ip protocol icmp accept

# Afficher les règles
sudo nft list ruleset

# Supprimer une règle
sudo nft delete rule inet filter input handle 3
```

### Tableau comparatif

| Aspect | UFW | iptables | nftables |
|--------|-----|----------|---------|
| Difficulté | ⭐ Facile | ⭐⭐⭐ Moyen | ⭐⭐⭐⭐ Complexe |
| Performance | Bonne | Bonne | Excellente |
| Cas d'usage | Poste de travail, serveurs simples | Serveurs avec règles complexes | Pare-feu d'entreprise |
| Persistance | `ufw save` | netfilter-persistent | Automatique |

> ⚠️ Si tu utilises UFW, ne mixe pas avec iptables ou nftables sans savoir ce que tu fais.
"""
append_to_md(md('37-ufw-pare-feu'), [firewall_extra])
rm_html('78-iptables-pare-feu')
rm_html('79-nftables-pare-feu')
print("  ✓ Merged 78+79 into 37")

# ─────────────────────────────────────────────
# PHASE 2.5 : Alias merge (30 + 58 → 30)
# ─────────────────────────────────────────────
alias_extra = """## 14. Scripts de configuration d'alias

### Configuration multi-machine via Git

```bash
# 1. Créer un dépôt git avec ton ~/.bashrc
cd ~
git init dotfiles
git add .bashrc .aliases
git commit -m "Mes alias"

# 2. Sur chaque machine, cloner ce dépôt
git clone git@github.com:toi/dotfiles.git
ln -s dotfiles/.bashrc ~/.bashrc
ln -s dotfiles/.aliases ~/.aliases
```

### Alias pour le réseau

```bash
# Surveillance réseau
alias pingf='ping -c 5'              # ping avec 5 paquets
alias netstat='ss -tulnp'            # ports en écoute
alias ipinfo='ip -br addr show'      # adresse IP courte
alias scan='nmap -sT localhost'      # scan de ports

# WiFi (nmcli)
alias wifion='nmcli radio wifi on'
alias wifioff='nmcli radio wifi off'
alias wifistatus='nmcli device wifi list'
```

### Alias pour Git

```bash
# Alias git avancés
alias gst='git status'
alias gco='git checkout'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
alias gd='git diff'
alias gds='git diff --staged'
alias gb='git branch'
alias gbl='git blame'

# Interactive rebase
alias gri='git rebase -i HEAD~'
```

### Alias pour ls

```bash
# ls avec couleurs
alias ls='ls --color=auto'
alias la='ls -A'
alias ll='ls -la'
alias l='ls -CF'
alias lt='ls -lart'         # derniers fichiers modifiés
```
"""
append_to_md(md('30-alias-raccourcis'), [alias_extra])
rm_html('58-alias-fonctions-bash')
print("  ✓ Merged 58 into 30")

# ─────────────────────────────────────────────
# PHASE 2.6 : Users merge (14 + 62 → 14)
# ─────────────────────────────────────────────
users_extra = """## 10. Gestion avancée des utilisateurs

### Vérouillage et expiration de compte

```bash
# Vérouiller un compte
sudo passwd -l nom_utilisateur

# Déverrouiller
sudo passwd -u nom_utilisateur

# Expirer le mot de passe (forcer changement au prochain login)
sudo passwd -e nom_utilisateur

# Voir le statut du mot de passe
sudo passwd -S nom_utilisateur
# PS = mot de passe actif, NP = pas de mot de passe, L = verrouillé
```

### Expiration de compte (date limite)

```bash
# Définir une date d'expiration
sudo usermod -e 2026-12-31 nom

# Voir la date d'expiration
sudo chage -l nom

# Forcer le changement de mot de passe
sudo chage -d 0 nom    # expire immédiatement
sudo chage -d 2025-01-01 nom  # expire à cette date
```

### Gestion des groupes avancée

```bash
# Ajouter plusieurs utilisateurs à un groupe
sudo usermod -aG groupe user1
sudo usermod -aG groupe user2

# Ajouter au groupe sudo (équivalent de admin)
sudo usermod -aG sudo nom_utilisateur
sudo usermod -aG sudo,david,www-data nom_utilisateur

# Voir tous les groupes d'un utilisateur
groups nom_utilisateur
id nom_utilisateur
```

### Lister les utilisateurs système

```bash
# Tous les utilisateurs (UID >= 1000 = utilisateurs normaux)
getent passwd | awk -F: '$3 >= 1000 {print $1}'

# Derniers utilisateurs à se connecter
lastlog

# Utilisateurs connectés actuellement
who
w
```

### Scripts de gestion par lot

```bash
#!/bin/bash
# Créer plusieurs utilisateurs d'un coup

UTILISATEURS=("alice" "bob" "caroline")

for user in "${UTILISATEURS[@]}"; do
    # Créer l'utilisateur
    sudo useradd -m -s /bin/bash "$user"
    
    # Ajouter au groupe commun
    sudo usermod -aG developers "$user"
    
    # Message
    echo "Utilisateur $user créé"
done

# Lister les utilisateurs créés
getent passwd | grep -E "^(${UTILISATEURS[*]})"
```

### Vérouiller l'accès SSH par clé seulement (sans mot de passe)

```bash
# Sur le serveur, modifier /etc/ssh/sshd_config :
# PasswordAuthentication no
# PubkeyAuthentication yes

sudo nano /etc/ssh/sshd_config
sudo systemctl restart sshd
```
"""
append_to_md(md('14-gestion-utilisateurs-groupes'), [users_extra])
rm_html('62-useradd-usermod-groupadd')
print("  ✓ Merged 62 into 14")

# ─────────────────────────────────────────────
# PHASE 2.7 : Processus/Signaux merge
#   11 + 82 → 11
#   04 + 72 → 04
# ─────────────────────────────────────────────
signals_extra = """## 11. Signaux système et gestion avancée

### Signaux importants (rappels)

| Signal | Numéro | Description |
|--------|--------|-------------|
| SIGTERM | 15 | Terminaison normale (propre) |
| SIGKILL | 9 | Terminaison forcée |
| SIGSTOP | 19 | Suspendre le processus |
| SIGCONT | 18 | Reprendre le processus |
| SIGHUP | 1 | Hangup (reload config) |
| SIGINT | 2 | Interruption (Ctrl+C) |

### Envoyer un signal à un processus

```bash
# Signal TERM (propre)
kill 1234
kill -15 1234

# Signal KILL (forcement)
kill -9 1234

# Envoyer un signal à tous les processus d'un utilisateur
kill -SIGTERM -u david

# Suspendre / Reprendre
kill -STOP 1234
kill -CONT 1234
```

### Signaux et scripts Bash

```bash
#!/bin/bash
# Gestion des signaux dans un script

# Intercepter un signal (ici SIGINT = Ctrl+C)
trap 'echo "Interruption détectée, nettoyage..."; rm -f /tmp/temp.*; exit' SIGINT SIGTERM

# Boucle infinie
while true; do
    echo "Travail en cours..."
    sleep 5
done
```

### nice et renice — Priorité des processus

```bash
# Lancer avec priorité basse (19 = plus basse)
nice -n 19 tar -czf backup.tar.gz /home

# Lancer avec priorité haute (-20 = plus haute, root only)
sudo nice -n -10 serveur

# Vérifier la priorité
ps -eo pid,ni,cmd | grep mon-processus

# Changer la priorité d'un processus en cours
sudo renice 10 -p 1234
sudo renice -5 -u david    # tous les进程 de david à priorité haute
```

### Utiliser renice avec un script

```bash
#!/bin/bash
# Lancer un script en arrière-plan avec priorité basse
nice -n 19 ./mon-script.sh &

# Récolter le PID
PID=$!
echo "Script lancé avec PID $PID"

# later, ajuster la priorité
renice +5 -p $PID
```
"""
append_to_md(md('11-supervision-systeme'), [signals_extra])
rm_html('82-kill-signaux')
print("  ✓ Merged 82 into 11")

# Merge 04 + 72 (jobs)
jobs_extra = """## 11. Contrôle des tâches (Job Control) — Complément

### Gérer les jobs en arrière-plan

```bash
# Lancer une commande longue en arrière-plan
commande_lourde &

# voir les jobs
jobs
# [1]+  Running    sleep 100 &
# [2]-  Stopped    nano notes.txt

# Ramener un job au premier plan
fg %1

# Reprendre un job arrêté en arrière-plan
bg %1

# Tuer un job spécifique
kill %1
```

### nohup — Garder une commande active après déconnexion

```bash
# Lancer une commande qui survit à la déconnexion
nohup ./mon-script.sh &

# La sortie est enregistrée dans nohup.out
tail -f nohup.out

# rediriger la sortie vers un fichier
nohup ./mon-script.sh > output.log 2>&1 &

# Se déconnecter sans problème
exit
```

### screen et tmux — Sessions persistantes

(voir aussi **Leçon 27 : tmux**)

```bash
# Créer une session screen
screen -S travaux

# Détacher (sans fermer) : Ctrl+A puis D

# Lister les sessions
screen -ls

# Se reconnecter à une session
screen -r travaux

# Supprimer une session
screen -X -S travaux quit
```

### subshells et regroupement

```bash
# Lancer plusieurs commandes en parallèle (subshell)
( commande1 & commande2 & commande3 & wait )

# ou avec process substitution
while read line; do
    echo "$line"
done < <( commande_lente )
```
"""
append_to_md(md('04-processus-services'), [jobs_extra])
rm_html('72-jobs-processus-arriere-plan')
print("  ✓ Merged 72 into 04")

# ─────────────────────────────────────────────
# PHASE 2.8 : Liens merge (26 + 65 → 26)
# ─────────────────────────────────────────────
liens_extra = """## 7. Liens symboliques pratiques (complément)

### Trouver tous les liens symboliques

```bash
# Trouver les liens dans un répertoire
find /home -type l -ls

# Trouver les liens cassés (qui pointent vers un fichier effacé)
find /home -type l -xtype l

# Afficher où pointe un lien
readlink -f /home/david/Bureau/mes-documents
# /home/david/mes-documents
```

### Créer des liens symboliques vers des commandes

```bash
# Créer un raccourci pour une commande avec chemin long
sudo ln -s /opt/mon-programme/bin/mon-cmd /usr/local/bin/mon-cmd

# Mettre à jour une commande système sans réinstaller
sudo ln -sf /nouveau/chemin/commande /usr/bin/commande

# Voir si une commande est un lien
type nom_commande
which nom_commande
```

### Utilisation avancée : structure de projet

```bash
# Projet avec versions multiples
/opt/
  mon-app/
    1.0/     (lien)
    2.0/     (lien)
    current/ -> 2.0/
    
# Le lien current pointe toujours vers la version active
# Mettre à jour : ln -snf /opt/mon-app/3.0 /opt/mon-app/current
```

### Copier vs lier : quand utiliser un lien ?

| Action | Effet | Usage |
|--------|-------|-------|
| `cp fichier lien` | Copie indépendante |backup simple |
| `ln fichier lien_dur` | Même inode, même contenu | backup automatique |
| `ln -s cible lien_sym` | Raccourci | Accès pratique |

### Liens symboliques et systemd

```bash
# Un service peut pointer vers un autre via lien symbolique
# Pour créé un service "custom-nginx" basé sur nginx :
sudo cp /lib/systemd/system/nginx.service /etc/systemd/system/custom-nginx.service
sudo systemctl daemon-reload
sudo systemctl enable custom-nginx
```

### Utiliser les liens pour organiser sa configuration

```bash
# dotfiles : garder sa config dans Git
ln -sf ~/dotfiles/.bashrc ~/.bashrc
ln -sf ~/dotfiles/.gitconfig ~/.gitconfig
ln -sf ~/dotfiles/.config/nvim ~/.config/nvim

# Vérifier que les liens sont valides
ls -la ~/.bashrc
```

### Script : nettoyer les liens cassés

```bash
#!/bin/bash
# Trouver et supprimer les liens cassés
find /home -type l -xtype l -delete

# Lister les liens dans un dossier
find /home -maxdepth 2 -type l -ls
```
"""
append_to_md(md('26-liens-symboliques-durs'), [liens_extra])
rm_html('65-liens-symboliques-pratique')
print("  ✓ Merged 65 into 26")

# ─────────────────────────────────────────────
# PHASE 2.9 : Surveillance watch merge (34 + 64 → 34)
# ─────────────────────────────────────────────
watch_extra = """## 11. La commande watch — Surveiller en temps réel

`watch` exécute une commande périodiquement et affiche le résultat plein écran.

### Syntaxe de base

```bash
watch commande
watch -n 2 'commande'   # toutes les 2 secondes (par défaut 2s)
```

### Exemples pratiques

```bash
# Surveiller l'espace disque
watch -n 5 'df -h /'

# Surveiller la mémoire
watch -n 2 'free -h'

# Surveiller les connexions réseau
watch -n 3 'ss -tuln'

# Surveiller les processus CPU
watch -n 2 'ps aux --sort=-%cpu | head -10'

# Surveiller un fichier journal en temps réel
watch -n 1 'tail /var/log/syslog | tail -5'

# Surveiller les modifications d'un répertoire
watch -n 2 'ls -lrt /home/david/telechargements/ | tail -5'
```

### Options utiles

```bash
# highlight : surligner les différences entre lesactualisations
watch -n 2 -d 'ps aux | grep python'

# Beep : émettre un son si quelque chose change
# (nécessite say ou espeak)
watch -n 5 'cat /tmp/alerte.txt'

# Passing output through grep
watch -n 2 'tail -20 /var/log/syslog | grep -i error'
```

### Combiner avec d'autres outils

```bash
# Surveillance DNS
watch -n 5 'nslookup monsite.com'

# Surveillance temperature (si lm-sensors installé)
watch -n 2 'sensors | grep Temp'

# Surveillance d'un service
watch -n 2 'systemctl status nginx | grep Active'

# Surveillance de l'espace (alerte si > 90%)
watch -n 60 'df -h / | tail -1 | awk "{print \$5}" | grep -q 9 && echo "ALERTE"'

# Surveillance avec logs
watch -n 10 'echo "=== $(date) ===" && df -h /' | tee /tmp/surveillance.log
```

### Script de surveillance continue avec watch

```bash
#!/bin/bash
# Surveillance mémoire + swap + processes

watch -n 5 '
echo "=== $(date +"%Y-%m-%d %H:%M:%S") ==="
echo ""
echo "--- MEMORY ---"
free -h
echo ""
echo "--- TOP 5 CPU ---"
ps aux --sort=-%cpu | head -6
echo ""
echo "--- TOP 5 MEMORY ---"
ps aux --sort=-%mem | head -6
'
```
"""
append_to_md(md('34-surveillance-optimisation-performances'), [watch_extra])
rm_html('64-watch-surveillance-temps-reel')
print("  ✓ Merged 64 into 34")

print("\n✅ PHASE 1+2 COMPLETE")