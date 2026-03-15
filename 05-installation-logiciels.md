# Leçon 5 : Installation de logiciels

Dans cette leçon, tu vas maîtriser l'installation, la mise à jour et la suppression de logiciels sur Linux avec différents gestionnaires de paquets.

---

## 1. Gestionnaires de paquets

### Les principaux

| Gestionnaire | Distributions | Type |
|--------------|---------------|------|
| **APT** | Debian, Ubuntu, Mint | .deb |
| **DNF/YUM** | Fedora, RHEL, CentOS | .rpm |
| **Pacman** | Arch, Manjaro | .pkg.tar |
| **Zypper** | openSUSE | .rpm |

Nous allonsfocuser sur **APT** car c'est le plus utilisé.

---

## 2. APT - Commandes de base

### Mettre à jour les dépôts

```bash
sudo apt update              # Mettre à jour la liste des paquets
sudo apt update && sudo apt upgrade  # Mise à jour complète
```

### Installer un logiciel

```bash
sudo apt install firefox     # Installer un paquet
sudo apt install firefox -y  # Confirmer automatiquement
sudo apt install -y firefox vlc  # Plusieurs paquets
```

### Mettre à jour

```bash
sudo apt upgrade             # Mettre à jour les paquets existants
sudo apt full-upgrade        # Mise à jour complète (peut supprimer)
sudo apt dist-upgrade        # Mise à jour de version
```

### Supprimer

```bash
sudo apt remove firefox      # Supprimer (garde config)
sudo apt purge firefox       # Supprimer + config
sudo apt autoremove          # Supprimer dépendances inutilisées
sudo apt autopurge           # Supprimer config + dépendances
```

---

## 3. Rechercher et informer

### Rechercher un paquet

```bash
apt search vlc               # Rechercher dans les dépôts
apt search --names-only vlc  # Chercher seulement dans le nom
apt-cache policy vlc         # Toutes les versions disponibles
```

### Informations sur un paquet

```bash
apt show firefox             # Détails complets
apt list --all-versions vlc  # Toutes les versions
apt list --installed         # Tous les paquets installés
apt list --upgradable        # Paquets avec mise à jour
```

### Lister les fichiers d'un paquet

```bash
dpkg -L firefox             # Liste des fichiers installés
dpkg -s firefox             # Statut du paquet
```

---

## 4. DPKG - Gestionnaire de base

`dpkg` est le gestionnaire de bas niveau (.deb).

### Installer un fichier .deb local

```bash
sudo dpkg -i paquet.deb          # Installer
sudo dpkg -i -r paquet.deb       # Réparer les dépendances
sudo dpkg -P paquet              # Purger complètement
```

### Lister les paquets

```bash
dpkg -l                     # Liste de tous les paquets
dpkg -l | grep ^ii          # Seulement installés
dpkg -l firefox             # Statut d'un paquet
```

---

## 5. SNAP - Empaquetage universel

Snap fonctionne sur toutes les distributions.

### Commandes snap

```bash
snap find vlc                 # Rechercher
sudo snap install vlc        # Installer
sudo snap remove vlc         # Supprimer
snap list                    # Liste installées
snap refresh                 # Mettre à jour
snap refresh vlc             # Mettre à jour un seul
snap revert vlc             # Revenir à la version précédente
```

### Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Fonctionne partout | Plus lourd (sandbox) |
| Versions récentes | Démarrage plus lent |
| Indépendance du système | Espace disque supplémentaire |

---

## 6. FLATPAK - Alternative moderne

```bash
# Installer flatpak
sudo apt install flatpak

# Ajouter un dépôt
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Installer
flatpak install flathub org.videolan.VLC
flatpak install flathub org.mozilla.firefox

# Mettre à jour
flatpak update

# Lister
flatpak list
```

---

## 7. PIP - Packages Python

### Installer des packages Python

```bash
pip install nom_paquet              # Installer
pip install -U nom_paquet          # Mettre à jour
pip install -r requirements.txt   #Depuis requirements
pip uninstall nom_paquet            # Désinstaller

# Python 3 spécifique
pip3 install nom_paquet
```

### Gérer les versions

```bash
pip freeze                         # Liste tous les packages
pip freeze > requirements.txt     # Sauvegarder dépendances
pip list --outdated               # Packages obsolètes
pip install --upgrade pip          # Mettre à jour pip
```

---

## 8. Node.js (NPM)

```bash
# Installer un package global
sudo npm install -g nom_paquet

# Installer local
npm install nom_paquet

# Installer depuis package.json
npm install

# Mettre à jour
npm update

# Lister
npm list -g --depth=0
```

---

## 9. RUBYGEMS

```bash
gem install nom_gem           # Installer
gem update nom_gem            # Mettre à jour
gem uninstall nom_gem         # Supprimer
gem list                      # Lister
gem list --local
```

---

## 10. Installation depuis les sources

Parfois, il faut compiler depuis les sources.

```bash
# Télécharger
wget https://exemple.com/paquet.tar.gz
tar -xzf paquet.tar.gz
cd paquet/

# Compiler
./configure
make
sudo make install

# ou avec cmake
mkdir build && cd build
cmake ..
make
sudo make install
```

---

## 11. Nettoyage et maintenance

### Nettoyer le système

```bash
sudo apt clean                 # Vider le cache apt
sudo apt autoclean           # Supprimer anciens .deb
sudo apt autoremove           # Supprimer dépendances inutilisées
sudo apt autopurge           # + fichiers config

# Nettoyer les journaux
sudo journalctl --vacuum-size=100M
```

### Espace disque

```bash
# Voir ce qui prend de la place
df -h                         # Disque
du -sh /var/cache/apt/archives  # Cache apt
du -sh /* 2>/dev/null | sort -h  # Dossiers volumineux
```

---

## 12. Exercices pratiques

### Exercice 1 : Installer htop
```bash
sudo apt update
sudo apt install htop
htop
```

### Exercice 2 : Installer un logiciel depuis un .deb
```bash
# Télécharger un .deb (ex: from https://.deb)
wget https://exemple.com/paquet.deb
sudo dpkg -i paquet.deb
# Si erreur dépendances:
sudo apt install -f
```

### Exercice 3 : Nettoyer le système
```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt clean
```

---

## 13. Résumé

| Commande | Description |
|---------|-------------|
| `apt update` | Mettre à jour les listes |
| `apt install` | Installer un paquet |
| `apt remove` | Supprimer (garde config) |
| `apt purge` | Supprimer + config |
| `apt upgrade` | Mettre à jour |
| `apt search` | Rechercher |
| `dpkg -i` | Installer un .deb |
| `snap install` | Installer un snap |
| `pip install` | Installer package Python |
| `apt autoremove` | Nettoyer dépendances |

---

Maîtrise ces commandes et tu pourras installer n'importe quel logiciel sur Linux ! 💪