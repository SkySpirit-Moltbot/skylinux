# Leçon 58 : file et stat — Inspecter les fichiers

Deux commandes pour savoir exactement ce que contient un fichier et ses métadonnées.

## 1. file — Déterminer le type d'un fichier

`file` analyse le contenu du fichier (pas juste l'extension) pour deviner son type.

```bash
# Type basique
file document.pdf
# → document.pdf: PDF document, version 1.4

file photo.jpg
# → photo.jpg: JPEG image data, 1920x1080

file script.sh
# → script.sh: Bourne-Again shell script, ASCII text executable

# Fichier sans extension
file data_bin
# → data_bin: ELF 64-bit LSB executable, x86-64

# Analyser tous les fichiers d'un dossier
file /usr/bin/* | head -10

# Afficher le type MIME
file -i document.pdf
# → document.pdf: application/pdf; charset=binary
```

## 2. stat — Métadonnées détaillées

```bash
# Toutes les infos d'un fichier
stat mon_fichier.txt

# Résultat :
#   Fichier: mon_fichier.txt
#   Taille: 1234      Blocs: 8         Bloc d'E/S: 4096
#   Périphérique: 8,1 Inœud: 456789    Liens: 1
# Accès: (0644/-rw-r--r--) UID: (1000/david) GID: (1000/david)
#  Accès: 2026-05-24 10:30:00.000000000 +0200
# Modif.: 2026-05-23 15:20:00.000000000 +0200
# Changt: 2026-05-23 15:20:00.000000000 +0200
```

## 3. Options utiles de stat

```bash
# Format personnalisé : ne montrer que ce qui t'intéresse
stat -c "%n a une taille de %s octets" mon_fichier.txt

# Afficher seulement la taille
stat -c %s mon_fichier.txt

# Afficher les permissions en octal
stat -c %a mon_fichier.txt
# → 644

# Afficher le propriétaire
stat -c %U mon_fichier.txt

# Vérifier la date de dernière modification
stat -c %y mon_fichier.txt
```

## 4. Comparer file et ls

```bash
# ls montre la taille et la date
ls -l mon_fichier.txt
# -rw-r--r-- 1 david david 1234 mai 23 15:20 mon_fichier.txt

# file montre le TYPE de contenu
file mon_fichier.txt
# mon_fichier.txt: ASCII text

# stat montre TOUTES les métadonnées (inode, blocs, timestamps)
stat mon_fichier.txt
```

## 5. Exercices pratiques

1. **Type mystère** — Crée un fichier sans extension et utilise `file` pour l'identifier
2. **MIME** — Utilise `file -i` sur une image, un PDF et un script .sh
3. **Stat** — Compare les dates "Accès" et "Modif." d'un fichier avec `stat`
