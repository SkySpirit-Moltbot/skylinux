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
- **Snap** → Ubuntu,sandbox universel
- **Flatpak** → sandbox universel pour Linux

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

