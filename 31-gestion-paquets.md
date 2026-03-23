# Leçon 31 : Gestion des paquets

Dans cette leçon, tu vas découvrir comment installer, mettre à jour et supprimer des logiciels sur Linux. Chaque distribution a son propre système de paquets, et tu apprendras à utiliser apt (Debian/Ubuntu), dnf/yum (Fedora/RHEL), et snap/flatpak.

---

## 1. Qu'est-ce qu'un paquet ?

Un **paquet** est un fichier compressé qui contient un logiciel prêt à être installé. Il inclut :
- Les fichiers du programme
- Des métadonnées (nom, version, dépendances)
- Des scripts d'installation et de désinstallation

**Types de paquets :**
- `.deb` → Debian, Ubuntu, Linux Mint (système **apt**)
- `.rpm` → Fedora, RHEL, CentOS (système **dnf/yum**)

**Formats modernes :**
- **Snap** → Ubuntu,通用的 sandbox
- **Flatpak** → Linux通用的, sandbox

---

## 2. APT (Debian/Ubuntu)

APT (*Advanced Package Tool*) est le système de paquets le plus utilisé sur Linux.

### Mettre à jour la liste des paquets

```bash
sudo apt update
```

Cette commande ne installe rien, elle met à jour la liste des paquets disponibles depuis les dépôts.

### Mettre à jour le système

```bash
# Mettre à jour tous les paquets
sudo apt upgrade

# Mettre à jour en installant aussi de nouveaux paquets si nécessaire
sudo apt full-upgrade
```

### Installer un paquet

```bash
# Installer un paquet
sudo apt install nom_du_paquet

# Installer plusieurs paquets
sudo apt install paquet1 paquet2 paquet3

# Installer sans demander confirmation
sudo apt install -y nom_du_paquet
```

### Exemple concret

```bash
# Installer le serveur web Nginx
sudo apt install nginx

# Installer des outils de développement
sudo apt install build-essential git curl wget
```

### Supprimer un paquet

```bash
# Supprimer le paquet mais garder les fichiers de configuration
sudo apt remove nom_du_paquet

# Supprimer le paquet ET ses fichiers de configuration
sudo apt purge nom_du_paquet

# Supprimer les paquets devenus inutiles
sudo apt autoremove
```

### Chercher un paquet

```bash
# Rechercher dans les noms de paquets
apt search nom_du_paquet

# Afficher les informations d'un paquet
apt show nom_du_paquet
```

### Lister les paquets installés

```bash
# Lister tous les paquets installés
apt list --installed

# Vérifier si un paquet est installé
dpkg -l | grep nom_du_paquet
```

---

## 3. DNF et YUM (Fedora/RHEL)

### DNF (Dandified YUM) - Fedora, RHEL 8+

```bash
# Mettre à jour tous les paquets
sudo dnf update

# Installer un paquet
sudo dnf install nom_du_paquet

# Supprimer un paquet
sudo dnf remove nom_du_paquet

# Rechercher un paquet
dnf search nom_du_paquet

# Lister les mises à jour disponibles
dnf check-update

# Nettoyer le cache
dnf clean all
```

### YUM - Ancien (RHEL 7, CentOS 7)

```bash
sudo yum update
sudo yum install nom_du_paquet
sudo yum remove nom_du_paquet
```

---

## 4. Snap

**Snap** est un système de paquets universel créé par Canonical. Les applications snp sont isoléées dans des sandbox.

```bash
# Installer snapd (si pas déjà installé)
sudo apt install snapd

# Installer une application snap
sudo snap install nom_du_paquet

# Lister les snaps installés
snap list

# Mettre à jour un snap
sudo snap refresh nom_du_paquet

# Mettre à jour tous les snaps
sudo snap refresh

# Supprimer un snap
sudo snap remove nom_du_paquet
```

### Exemples concrets

```bash
# Installer VS Code
sudo snap install code --classic

# Installer Spotify
sudo snap install spotify

# Installer Firefox
sudo snap install firefox
```

---

## 5. Flatpak

**Flatpak** est un autre système de paquets universel, très utilisé sur Linux.

```bash
# Installer flatpak (si pas déjà installé)
sudo apt install flatpak

# Ajouter le dépôt Flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Installer une application
flatpak install flathub nom.de.lapplication

# Lister les applications installées
flatpak list

# Mettre à jour
flatpak update

# Supprimer
flatpak uninstall nom.de.lapplication
```

### Exemples concrets

```bash
# Installer GIMP (traitement d'image)
flatpak install flathub org.gimp.GIMP

# Installer VLC
flatpak install flathub org.videolan.VLC

# Installer LibreOffice
flatpak install flathub org.libreoffice.LibreOffice
```

---

## 6. Comparatif des systèmes

| Opération | APT (Debian/Ubuntu) | DNF (Fedora) | Snap | Flatpak |
|-----------|---------------------|--------------|------|---------|
| Mise à jour liste | `apt update` | `dnf check-update` | `snap refresh` | `flatpak update` |
| Installer | `apt install pkg` | `dnf install pkg` | `snap install pkg` | `flatpak install flathub pkg` |
| Supprimer | `apt remove pkg` | `dnf remove pkg` | `snap remove pkg` | `flatpak uninstall pkg` |
| Rechercher | `apt search pkg` | `dnf search pkg` | `snap find pkg` | `flatpak search pkg` |
| Lister installés | `apt list --installed` | `dnf list installed` | `snap list` | `flatpak list` |

---

## 7. Dépôts de paquets

Un **dépôt** (repository) est un serveur qui contient des paquets. Tu peux en ajouter pour avoir plus de logiciels.

### APT : Ajouter un dépôt

```bash
# Exemple : ajouter le dépôt VS Code sur Ubuntu
sudo apt install software-properties-common apt-transport-https wget
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code
```

### Gérer les dépôts via interface

```bash
# Ubuntu/Debian : interface graphique
sudo software-properties-gtk

# Fedora : interface graphique
sudo dnf dragora
```

---

## 8. Paquets .deb et .rpm manuels

Parfois, tu download un fichier `.deb` ou `.rpm` directement.

### Installer un .deb (Debian/Ubuntu)

```bash
# Avec dpkg (gestionnaire de base)
sudo dpkg -i fichier.deb

# Si des dépendances manquent, les installer
sudo apt install -f

# Ou avec gdebi (résout les dépendances automatiquement)
sudo apt install gdebi
sudo gdebi fichier.deb
```

### Installer un .rpm (Fedora/RHEL)

```bash
# Avec rpm (gestionnaire de base)
sudo rpm -i fichier.rpm

# Ou avec dnf (meilleur, résout les dépendances)
sudo dnf install fichier.rpm
```

> ⚠️ Installer des paquets manuellement (hors dépôts) présente des risques : pas de mises à jour automatiques, possibles conflits de dépendances.

---

## 9. Hiérarchie des dossiers importants

```
/etc/apt/sources.list.d/    → Dépôts APT supplémentaires
/var/cache/apt/archives/    → Paquets .deb téléchargés
/var/lib/dpkg/              → Base de données des paquets installés
/var/cache/dnf/             → Cache DNF
/snap/                      → Applications Snap
~/.local/share/flatpak/     → Applications Flatpak
```

---

## 10. Résumé des commandes

| Commande | Description |
|----------|-------------|
| `apt update` | Mettre à jour la liste des paquets |
| `apt upgrade` | Mettre à jour tous les paquets |
| `apt install pkg` | Installer un paquet |
| `apt remove pkg` | Supprimer un paquet |
| `apt search pkg` | Rechercher un paquet |
| `apt list --installed` | Lister les paquets installés |
| `dpkg -l` | Lister tous les paquets installés (détails) |
| `dnf install pkg` | Installer (Fedora/RHEL) |
| `snap install pkg` | Installer via Snap |
| `flatpak install flathub pkg` | Installer via Flatpak |

---

## 11. Exercice pratique

### Exercice : Gère les paquets sur ton système

**Objectif** : Apprendre à utiliser le système de paquets de ta distribution.

**Étape 1 : Connais ta distribution**

```bash
# Voir ta distribution
lsb_release -a

# Ou
cat /etc/os-release
```

**Étape 2 : Mets à jour ton système**

```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt upgrade -y

# Sur Fedora
sudo dnf update -y
```

**Étape 3 : Recherche un paquet**

```bash
# Recherche un outil (exemple : htop)
apt search htop
# ou
dnf search htop
```

**Étape 4 : Installe un paquet**

```bash
# Installe htop (gestionnaire de processus en ligne de commande)
sudo apt install htop
# ou
sudo dnf install htop
```

**Étape 5 : Vérifie l'installation**

```bash
htop
# (appuie sur q pour quitter)
```

**Étape 6 : Lis les informations du paquet**

```bash
apt show htop
# ou
dnf info htop
```

**Étape 7 : Désinstalle et nettoie**

```bash
# Désinstalle htop
sudo apt remove htop
sudo apt autoremove

# Nettoie le cache des paquets
sudo apt clean

# Sur Fedora
sudo dnf clean all
```

✅ Tu sais maintenant gérer les logiciels sur Linux !

---

## 12. Aller plus loin

- **PPA (Personal Package Archive)** : Dépôts créés par des utilisateurs sur Ubuntu
- **RPM Fusion** : Dépôt additionnel pour Fedora avec des logiciels non inclus par défaut
- **AppImage** : Format de paquets portables qui fonctionnent sans installation
- **Gestionnaire de paquets graphiques** : Software Center (Ubuntu), GNOME Software, Discover (KDE)

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Leçon 31 : Gestion des paquets - SkyLinux</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="canonical" href="https://skyspirit-moltbot.github.io/skylinux/31-gestion-paquets.html">
<meta property="og:title" content="Leçon 31 : Gestion des paquets - SkyLinux">
<meta property="og:description" content="Apprenez Linux facilement avec SkyLinux">
<meta name="description" content="Leçon 31 : Gestion des paquets - Apprenez Linux facilement avec SkyLinux - Le guide pour tous.">
<meta name="keywords" content="linux, cours, Leçon 31 : Gestion des paquets, debutant, ubuntu">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Inter", sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; padding: 40px 20px; }
.container { max-width: 800px; margin: 0 auto; }
h1 { font-size: 1.8rem; background: linear-gradient(135deg, #00d9ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
h2 { color: #00d9ff; margin: 20px 0 10px; }
p { line-height: 1.7; margin: 10px 0; color: #bbb; }
code { background: rgba(0,217,255,0.1); color: #00d9ff; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
table { width: 100%; border-collapse: collapse; margin: 15px 0; }
th, td { border: 1px solid #333; padding: 8px; }
th { background: rgba(0,217,255,0.1); }
nav { display: flex; justify-content: space-between; margin-top: 30px; padding-top: 20px; border-top: 1px solid #333; }

/* === Code Block avec copie + progression === */
.code-block {
  background: #111118;
  border-radius: 8px;
  overflow: hidden;
  margin: 15px 0;
  border: 1px solid #30363d;
}
.code-block progress {
  width: 100%;
  height: 3px;
  appearance: none;
  border: none;
  display: block;
}
.code-block progress::-webkit-progress-bar { background: #238636; }
.code-block progress::-moz-progress-bar { background: #238636; }
.code-block progress.loaded { background: #30363d; }

.code-line {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  position: relative;
  transition: background 0.15s;
}
.code-line:hover { background: rgba(255,255,255,0.04); }
.code-line code {
  background: none;
  color: #e6edf3;
  padding: 0;
  font-family: 'Courier New', monospace;
  font-size: 13.5px;
  line-height: 1.5;
  white-space: pre;
  flex: 1;
  overflow-x: auto;
}
.copy-btn {
  margin-left: 12px;
  background: none;
  border: 1px solid #30363d;
  border-radius: 6px;
  cursor: pointer;
  padding: 4px 8px;
  opacity: 0.5;
  transition: opacity 0.2s, border-color 0.2s;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}
.copy-btn:hover { opacity: 1; border-color: #58a6ff; }
.copy-btn.copied { border-color: #238636; opacity: 1; }
.copy-btn svg {
  width: 14px;
  height: 14px;
  fill: #8b949e;
  display: block;
}
.copy-btn.copied svg { fill: #238636; }

/* Inline code (dans le texte) */
p code, li code { background: rgba(0,217,255,0.1); color: #00d9ff; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
blockquote { background: rgba(255,204,0,0.1); border-left: 4px solid #ffcc00; padding: 12px 16px; margin: 15px 0; border-radius: 0 8px 8px 0; }
blockquote p { margin: 0; color: #e0e0e0; }
hr { border: none; border-top: 1px solid #333; margin: 25px 0; }
ul, ol { padding-left: 25px; margin: 10px 0; }
li { line-height: 1.7; color: #bbb; margin: 5px 0; }
</style>
</head>
<body>
<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:15px;margin-bottom:20px;border-bottom:1px solid #333;">
<a href="index.html" style="color:#666;text-decoration:none;">&larr; Sommaire</a>
<span style="font-size:1.2rem;font-weight:700;background:linear-gradient(135deg,#00d9ff,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">SkyLinux</span>
</div>
<div class="container">

<h1>Leçon 31 : Gestion des paquets</h1>
<p>Dans cette leçon, tu vas découvrir comment installer, mettre à jour et supprimer des logiciels sur Linux. Chaque distribution a son propre système de paquets, et tu apprendras à utiliser apt (Debian/Ubuntu), dnf/yum (Fedora/RHEL), et snap/flatpak.</p>
<hr />
<h2>1. Qu'est-ce qu'un paquet ?</h2>
<p>Un <strong>paquet</strong> est un fichier compressé qui contient un logiciel prêt à être installé. Il inclut :</p>
<ul>
<li>Les fichiers du programme</li>
<li>Des métadonnées (nom, version, dépendances)</li>
<li>Des scripts d'installation et de désinstallation</li>
</ul>
<p><strong>Types de paquets :</strong></p>
<ul>
<li><code>.deb</code> → Debian, Ubuntu, Linux Mint (système <strong>apt</strong>)</li>
<li><code>.rpm</code> → Fedora, RHEL, CentOS (système <strong>dnf/yum</strong>)</li>
</ul>
<p><strong>Formats modernes :</strong></p>
<ul>
<li><strong>Snap</strong> → Ubuntu,通用的 sandbox</li>
<li><strong>Flatpak</strong> → Linux通用的, sandbox</li>
</ul>
<hr />
<h2>2. APT (Debian/Ubuntu)</h2>
<p>APT (<em>Advanced Package Tool</em>) est le système de paquets le plus utilisé sur Linux.</p>
<h3>Mettre à jour la liste des paquets</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code>sudo apt update</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p>Cette commande ne installe rien, elle met à jour la liste des paquets disponibles depuis les dépôts.</p>
<h3>Mettre à jour le système</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Mettre à jour tous les paquets
sudo apt upgrade

# Mettre à jour en installant aussi de nouveaux paquets si nécessaire
sudo apt full-upgrade</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Installer un paquet</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installer un paquet
sudo apt install nom_du_paquet

# Installer plusieurs paquets
sudo apt install paquet1 paquet2 paquet3

# Installer sans demander confirmation
sudo apt install -y nom_du_paquet</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Exemple concret</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installer le serveur web Nginx
sudo apt install nginx

# Installer des outils de développement
sudo apt install build-essential git curl wget</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Supprimer un paquet</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Supprimer le paquet mais garder les fichiers de configuration
sudo apt remove nom_du_paquet

# Supprimer le paquet ET ses fichiers de configuration
sudo apt purge nom_du_paquet

# Supprimer les paquets devenus inutiles
sudo apt autoremove</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Chercher un paquet</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Rechercher dans les noms de paquets
apt search nom_du_paquet

# Afficher les informations d'un paquet
apt show nom_du_paquet</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Lister les paquets installés</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Lister tous les paquets installés
apt list --installed

# Vérifier si un paquet est installé
dpkg -l | grep nom_du_paquet</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<hr />
<h2>3. DNF et YUM (Fedora/RHEL)</h2>
<h3>DNF (Dandified YUM) - Fedora, RHEL 8+</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Mettre à jour tous les paquets
sudo dnf update

# Installer un paquet
sudo dnf install nom_du_paquet

# Supprimer un paquet
sudo dnf remove nom_du_paquet

# Rechercher un paquet
dnf search nom_du_paquet

# Lister les mises à jour disponibles
dnf check-update

# Nettoyer le cache
dnf clean all</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>YUM - Ancien (RHEL 7, CentOS 7)</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code>sudo yum update
sudo yum install nom_du_paquet
sudo yum remove nom_du_paquet</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<hr />
<h2>4. Snap</h2>
<p><strong>Snap</strong> est un système de paquets universel créé par Canonical. Les applications snp sont isoléées dans des sandbox.</p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installer snapd (si pas déjà installé)
sudo apt install snapd

# Installer une application snap
sudo snap install nom_du_paquet

# Lister les snaps installés
snap list

# Mettre à jour un snap
sudo snap refresh nom_du_paquet

# Mettre à jour tous les snaps
sudo snap refresh

# Supprimer un snap
sudo snap remove nom_du_paquet</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Exemples concrets</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installer VS Code
sudo snap install code --classic

# Installer Spotify
sudo snap install spotify

# Installer Firefox
sudo snap install firefox</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<hr />
<h2>5. Flatpak</h2>
<p><strong>Flatpak</strong> est un autre système de paquets universel, très utilisé sur Linux.</p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installer flatpak (si pas déjà installé)
sudo apt install flatpak

# Ajouter le dépôt Flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Installer une application
flatpak install flathub nom.de.lapplication

# Lister les applications installées
flatpak list

# Mettre à jour
flatpak update

# Supprimer
flatpak uninstall nom.de.lapplication</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Exemples concrets</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installer GIMP (traitement d'image)
flatpak install flathub org.gimp.GIMP

# Installer VLC
flatpak install flathub org.videolan.VLC

# Installer LibreOffice
flatpak install flathub org.libreoffice.LibreOffice</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<hr />
<h2>6. Comparatif des systèmes</h2>
<table>
<thead>
<tr>
<th>Opération</th>
<th>APT (Debian/Ubuntu)</th>
<th>DNF (Fedora)</th>
<th>Snap</th>
<th>Flatpak</th>
</tr>
</thead>
<tbody>
<tr>
<td>Mise à jour liste</td>
<td><code>apt update</code></td>
<td><code>dnf check-update</code></td>
<td><code>snap refresh</code></td>
<td><code>flatpak update</code></td>
</tr>
<tr>
<td>Installer</td>
<td><code>apt install pkg</code></td>
<td><code>dnf install pkg</code></td>
<td><code>snap install pkg</code></td>
<td><code>flatpak install flathub pkg</code></td>
</tr>
<tr>
<td>Supprimer</td>
<td><code>apt remove pkg</code></td>
<td><code>dnf remove pkg</code></td>
<td><code>snap remove pkg</code></td>
<td><code>flatpak uninstall pkg</code></td>
</tr>
<tr>
<td>Rechercher</td>
<td><code>apt search pkg</code></td>
<td><code>dnf search pkg</code></td>
<td><code>snap find pkg</code></td>
<td><code>flatpak search pkg</code></td>
</tr>
<tr>
<td>Lister installés</td>
<td><code>apt list --installed</code></td>
<td><code>dnf list installed</code></td>
<td><code>snap list</code></td>
<td><code>flatpak list</code></td>
</tr>
</tbody>
</table>
<hr />
<h2>7. Dépôts de paquets</h2>
<p>Un <strong>dépôt</strong> (repository) est un serveur qui contient des paquets. Tu peux en ajouter pour avoir plus de logiciels.</p>
<h3>APT : Ajouter un dépôt</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Exemple : ajouter le dépôt VS Code sur Ubuntu
sudo apt install software-properties-common apt-transport-https wget
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Gérer les dépôts via interface</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Ubuntu/Debian : interface graphique
sudo software-properties-gtk

# Fedora : interface graphique
sudo dnf dragora</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<hr />
<h2>8. Paquets .deb et .rpm manuels</h2>
<p>Parfois, tu download un fichier <code>.deb</code> ou <code>.rpm</code> directement.</p>
<h3>Installer un .deb (Debian/Ubuntu)</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Avec dpkg (gestionnaire de base)
sudo dpkg -i fichier.deb

# Si des dépendances manquent, les installer
sudo apt install -f

# Ou avec gdebi (résout les dépendances automatiquement)
sudo apt install gdebi
sudo gdebi fichier.deb</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<h3>Installer un .rpm (Fedora/RHEL)</h3>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Avec rpm (gestionnaire de base)
sudo rpm -i fichier.rpm

# Ou avec dnf (meilleur, résout les dépendances)
sudo dnf install fichier.rpm</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<blockquote>
<p>⚠️ Installer des paquets manuellement (hors dépôts) présente des risques : pas de mises à jour automatiques, possibles conflits de dépendances.</p>
</blockquote>
<hr />
<h2>9. Hiérarchie des dossiers importants</h2>
<table>
<thead>
<tr>
<th>Dossier</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>/etc/apt/sources.list.d/</code></td>
<td>Dépôts APT supplémentaires</td>
</tr>
<tr>
<td><code>/var/cache/apt/archives/</code></td>
<td>Paquets .deb téléchargés</td>
</tr>
<tr>
<td><code>/var/lib/dpkg/</code></td>
<td>Base de données des paquets installés</td>
</tr>
<tr>
<td><code>/var/cache/dnf/</code></td>
<td>Cache DNF</td>
</tr>
<tr>
<td><code>/snap/</code></td>
<td>Applications Snap</td>
</tr>
<tr>
<td><code>~/.local/share/flatpak/</code></td>
<td>Applications Flatpak</td>
</tr>
</tbody>
</table>
<hr />
<h2>10. Résumé des commandes</h2>
<table>
<thead>
<tr>
<th>Commande</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>apt update</code></td>
<td>Mettre à jour la liste des paquets</td>
</tr>
<tr>
<td><code>apt upgrade</code></td>
<td>Mettre à jour tous les paquets</td>
</tr>
<tr>
<td><code>apt install pkg</code></td>
<td>Installer un paquet</td>
</tr>
<tr>
<td><code>apt remove pkg</code></td>
<td>Supprimer un paquet</td>
</tr>
<tr>
<td><code>apt search pkg</code></td>
<td>Rechercher un paquet</td>
</tr>
<tr>
<td><code>apt list --installed</code></td>
<td>Lister les paquets installés</td>
</tr>
<tr>
<td><code>dpkg -l</code></td>
<td>Lister tous les paquets installés (détails)</td>
</tr>
<tr>
<td><code>dnf install pkg</code></td>
<td>Installer (Fedora/RHEL)</td>
</tr>
<tr>
<td><code>snap install pkg</code></td>
<td>Installer via Snap</td>
</tr>
<tr>
<td><code>flatpak install flathub pkg</code></td>
<td>Installer via Flatpak</td>
</tr>
</tbody>
</table>
<hr />
<h2>11. Exercice pratique</h2>
<h3>Exercice : Gère les paquets sur ton système</h3>
<p><strong>Objectif</strong> : Apprendre à utiliser le système de paquets de ta distribution.</p>
<p><strong>Étape 1 : Connais ta distribution</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Voir ta distribution
lsb_release -a

# Ou
cat /etc/os-release</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p><strong>Étape 2 : Mets à jour ton système</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Sur Ubuntu/Debian
sudo apt update
sudo apt upgrade -y

# Sur Fedora
sudo dnf update -y</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p><strong>Étape 3 : Recherche un paquet</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Recherche un outil (exemple : htop)
apt search htop
# ou
dnf search htop</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p><strong>Étape 4 : Installe un paquet</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Installe htop (gestionnaire de processus en ligne de commande)
sudo apt install htop
# ou
sudo dnf install htop</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p><strong>Étape 5 : Vérifie l'installation</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code>htop
# (appuie sur q pour quitter)</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p><strong>Étape 6 : Lis les informations du paquet</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code>apt show htop
# ou
dnf info htop</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p><strong>Étape 7 : Désinstalle et nettoie</strong></p>
<div class="code-block">
  <progress value="0" max="100"></progress>
  <div class="code-line" onclick="copyCode(this)">
    <code># Désinstalle htop
sudo apt remove htop
sudo apt autoremove

# Nettoie le cache des paquets
sudo apt clean

# Sur Fedora
sudo dnf clean all</code>
    <button class="copy-btn" aria-label="Copier">
      <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </button>
  </div>
</div>
<p>✅ Tu sais maintenant gérer les logiciels sur Linux !</p>
<hr />
<h2>12. Aller plus loin</h2>
<ul>
<li><strong>PPA (Personal Package Archive)</strong> : Dépôts créés par des utilisateurs sur Ubuntu</li>
<li><strong>RPM Fusion</strong> : Dépôt additionnel pour Fedora avec des logiciels non inclus par défaut</li>
<li><strong>AppImage</strong> : Format de paquets portables qui fonctionnent sans installation</li>
<li><strong>Gestionnaire de paquets graphiques</strong> : Software Center (Ubuntu), GNOME Software, Discover (KDE)</li>
</ul>

</div>
<nav>

<a href="30-alias-raccourcis.html" style="color:#00d9ff;text-decoration:none;">&larr; 30 - Alias et raccourcis personnalises</a> | <span style="color:#666;">31</span>

</nav>

<script>
function copyCode(el) {
  var container = el.closest('.code-block');
  var code = el.querySelector('code');
  var btn = el.querySelector('.copy-btn');
  var progress = container.querySelector('progress');

  if (!code || !btn) return;

  var text = code.textContent;

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function() {
      btn.classList.add('copied');
      btn.querySelector('svg').innerHTML = '<path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>';
    }, function() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      btn.classList.add('copied');
      btn.querySelector('svg').innerHTML = '<path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>';
    });
  } else {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    btn.classList.add('copied');
    btn.querySelector('svg').innerHTML = '<path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>';
  }

  setTimeout(function() {
    btn.classList.remove('copied');
    btn.querySelector('svg').innerHTML = '<path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>';
  }, 2000);

  var val = 0;
  progress.value = 0;
  progress.classList.remove('loaded');
  var interval = setInterval(function() {
    val += 5;
    progress.value = val;
    if (val >= 100) {
      clearInterval(interval);
      setTimeout(function() { progress.classList.add('loaded'); }, 300);
    }
  }, 20);
}
</script>

</body>
</html>
