# Leçon 52 : df et du — Gérer l'espace disque

Deux commandes indispensables pour savoir où passe ton espace disque : `df` pour une vue d'ensemble, `du` pour descendre dans le détail.

## 1. df — Espace disponible par partition

```bash
# Vue d'ensemble en format lisible
df -h

# Résultat type :
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   32G   16G  67% /
# /dev/sdb1       200G  120G   71G  63% /home
```

Options utiles :

```bash
# Afficher le type de système de fichiers
df -hT

# Afficher seulement les systèmes de fichiers locaux (pas les tmpfs)
df -hl

# Voir l'espace inode (nombre de fichiers max)
df -i

# Un disque peut être plein en inodes même avec de l'espace libre !
```

## 2. du — Espace consommé par dossier

```bash
# Taille d'un dossier spécifique
du -sh /home/david/Documents

# Taille de chaque sous-dossier de /var
du -sh /var/*

# Trier du plus gros au plus petit
du -sh /var/* | sort -rh

# Descendre dans l'arborescence
du -h --max-depth=1 /home/david/
```

## 3. Top 10 des plus gros dossiers

```bash
# Trouver ce qui prend le plus de place
du -ah /home/david | sort -rh | head -10

# Par dossier uniquement (pas les fichiers)
du -h --max-depth=1 / | sort -rh | head -10

# Version plus rapide sur les gros systèmes
ncdu /home/david/
# (ncdu est interactif, à installer avec apt install ncdu)
```

## 4. Nettoyer l'espace disque

```bash
# Trouver les gros fichiers (> 100 Mo)
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# Vider la corbeille
rm -rf ~/.local/share/Trash/*

# Nettoyer les logs anciens
sudo journalctl --vacuum-size=500M

# Nettoyer le cache des paquets (Debian/Ubuntu)
sudo apt clean

# Voir la taille du cache apt AVANT nettoyage
du -sh /var/cache/apt/
```

## 5. Exercices pratiques

1. **État du disque** — Exécute `df -h` et note quel disque est le plus rempli
2. **Espace home** — Affiche la taille totale de ton `/home` avec `du -sh`
3. **Top 10** — Trouve les 10 plus gros répertoires de `/var`
4. **Gros fichiers** — Trouve les fichiers de plus de 50 Mo avec `find`
