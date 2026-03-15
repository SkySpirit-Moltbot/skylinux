# Leçon 8 : Archivage et compression

Dans cette leçon, nous allons apprendre à **archiver** et **compresser** des fichiers sous Linux. Ces compétences sont essentielles pour :
- Sauvegarder des données
- Réduire la taille pour le transfert
- Archiver des logs
- Packageur des applications

---

## 1. Comprendre la différence

| Terme | Signification |
|-------|---------------|
| **Archiver** | Combiner plusieurs fichiers/dossiers en un seul fichier |
| **Compresser** | Réduire la taille des données avec un algorithme |

**tar** fait l'archiving, **gzip/bzip2/xz** font la compression.

---

## 2. TAR - L'archivage

### Présentation

`tar` (Tape Archive) est la commande standard d'archivage sous Linux. Elle combine plusieurs fichiers en un seul, sans compression par défaut.

### Syntaxe de base

```bash
tar [OPTIONS] [ARCHIVE] [FICHIERS]
```

### Options principales

| Option | Description |
|--------|-------------|
| `-c` | Créer une archive |
| `-x` | Extraire (eXtract) |
| `-t` | Lister le contenu |
| `-v` | Mode verbeux |
| `-f` | Nom du fichier archive |
| `-r` | Ajouter des fichiers à une archive existante |
| `-u` | Mettre à jour seulement si plus récent |
| `-d` | Diff entre archive et système de fichiers |

### Créer une archive (sans compression)

```bash
tar -cvf archive.tar dossier/
# -c = créer, -v = verbeux, -f = nom du fichier

tar -cvf backup.tar ~/Documents ~/Images
# Archiver plusieurs dossiers
```

### Lister le contenu d'une archive

```bash
tar -tvf archive.tar          # Liste détaillée
tar -tvf archive.tar | less   # Paginer
tar -tf archive.tar           # Liste simple
```

### Extraire une archive

```bash
tar -xvf archive.tar                  # Extraire tout
tar -xvf archive.tar -C /autre/dossier/  # Extraire ailleurs
tar -xvf archive.tar fichier.txt      # Extraire un seul fichier
tar -xvf archive.tar --wildcards '*.txt'  # Extraire par pattern
```

---

## 3. Compression avec TAR

### GZIP (.tar.gz ou .tgz)

**Compression rapide, taille moyenne**

```bash
# Créer
tar -cvzf archive.tar.gz dossier/
tar -cvzf backup.tgz dossier/    # Extension alternative

# Lister
tar -tvzf archive.tar.gz

# Extraire
tar -xvzf archive.tar.gz
tar -xvzf archive.tar.gz -C /tmp/
```

### BZIP2 (.tar.bz2 ou .tbz2)

**Compression meilleure, plus lent**

```bash
# Créer
tar -cvjf archive.tar.bz2 dossier/
tar -cvjf backup.tbz2 dossier/

# Lister
tar -tvjf archive.tar.bz2

# Extraire
tar -xvjf archive.tar.bz2
```

### XZ (.tar.xz) - Recommandé

**Meilleure compression, plus lent**

```bash
# Créer
tar -cvJf archive.tar.xz dossier/

# Lister
tar -tvJf archive.tar.xz

# Extraire
tar -xvJf archive.tar.xz
```

### Tableau comparatif

| Format | Extension | Compression | Vitesse | Utilisation |
|--------|-----------|-------------|---------|--------------|
| gzip | .gz | Moyenne | Rapide | Fichiers log, transfert rapide |
| bzip2 | .bz2 | Bonne | Moyen |_backup_archives |
| xz | .xz | Excellente | Lent | Distribution, sauvegarde longue |
| zstd | .zst | Excellente | Rapide | Nouveau, recommandé |

---

## 4. Créer des archives compressées - Guide complet

### Exemple pratique complet

```bash
# Créer une archive compressée de votre home
tar -cvzf ~/backup_home_$(date +%Y%m%d).tar.gz ~/

# Archiver avec exclusion de certains dossiers
tar -cvzf backup.tar.gz dossier/ \
    --exclude='*.log' \
    --exclude='.cache' \
    --exclude='node_modules'

# Archiver plusieurs dossiers avec date
tar -cvzf "backup_$(date +%Y%m%d_%H%M).tar.gz" \
    ~/Documents \
    ~/Images \
    ~/Vidéos
```

### Commandes modernes avec pigz/pbzip2 (parallèle)

```bash
# Si installé: compression parallèle (plus rapide sur multi-core)
tar -cvf archive.tar dossier/ --use-compress-program=pigz
tar -cvf archive.tar dossier/ --use-compress-program=pbzip2
```

---

## 5. ZIP et UNZIP

### Présentation

Le format ZIP est universel et fonctionne sur tous les操作系统.

### Commandes de base

```bash
# Créer une archive ZIP
zip -r archive.zip dossier/
zip -r backup.zip file1.txt file2.txt

# Options utiles
zip -r -9 archive.zip dossier/    # Compression maximale (1-9)
zip -r -e archive.zip dossier/    # Chiffré (mot de passe)
zip -r -v archive.zip dossier/    # Verbeux
zip -r --exclude='*.log' archive.zip dossier/

# Lister le contenu
unzip -l archive.zip

# Extraire
unzip archive.zip                  # Extraire tout
unzip archive.zip -d /destination/ # Extraire ailleurs
unzip archive.zip fichier.txt      # Un seul fichier
unzip -p archive.zip fichier.txt   # Vers stdout

# Extraire avec mot de passe
unzip -P motdepasse archive.zip
```

---

## 6. Formats avancés

### 7Z (7-Zip)

```bash
# Installer si besoin
sudo apt install p7zip-full

# Créer
7z a archive.7z dossier/
7z a -mx=9 archive.7z dossier/   # Compression maximale

# Lister
7z l archive.7z

# Extraire
7z x archive.7z

# Avec mot de passe
7z a -p archive.7z dossier/
```

### ZSTD (recommandé - rapide et bon)

```bash
# Installer
sudo apt install zstd

# Créer
tar -cvzf - dossier/ | zstd > archive.tar.zst
# ou
tar -I zstd -cvf archive.tar.zst dossier/

# Extraire
tar -I zstd -xvf archive.tar.zst
```

---

## 7. Manipulations avancées

### Ajouter des fichiers à une archive existante

```bash
# Avec tar et gzip
gzip -d archive.tar.gz
tar -rvf archive.tar nouveau_fichier.txt
gzip archive.tar

# Avec zip
zip -r archive.zip nouveau_fichier.txt
```

### Mise à jour incrémentale

```bash
# Sauvegarde complète
tar -cvzf backup-full.tar.gz dossier/

# Sauvegarde incrémentale (uniquement fichiers modifiés)
tar -cvzf backup-$(date +%Y%m%d).tar.gz \
    -N "2024-01-01" dossier/
```

### Vérifier l'intégrité

```bash
# Vérifier tar.gz
gzip -t archive.tar.gz
tar -tzf archive.tar.gz

# Vérifier zip
zip -T archive.zip

# Vérifier 7z
7z t archive.7z
```

---

## 8. Exercices pratiques

### Exercice 1 : Créer une backup complète
```bash
# Backup de ~/Documents avec exclusions
tar -cvzf ~/backup_documents_$(date +%Y%m%d).tar.gz \
    ~/Documents \
    --exclude='.cache' \
    --exclude='.local' \
    --exclude='*.tmp'

# Vérifier
tar -tvzf ~/backup_documents_*.tar.gz | head -20
```

### Exercice 2 : Restaurer sélectivement
```bash
# Lister d'abord
tar -tvzf backup.tar.gz | grep important

# Extraire juste ce fichier
tar -xvzf backup.tar.gz chemin/vers/important.txt
```

### Exercice 3 : Archiver et déplacer sur un autre serveur
```bash
# Sur la machine source
tar -cvzf - dossier/ | ssh user@serveur "cat > backup.tar.gz"

# Sur le serveur distant
ssh user@serveur "tar -cvzf - dossier/" > local-backup.tar.gz
```

### Exercice 4 : Créer une archive horodatée
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M)
tar -cvzf "/backup/backup_$DATE.tar.gz" ~/Documents
echo "Backup créé: backup_$DATE.tar.gz"
```

---

## 9. Tableau résumé

| Action | gzip | bzip2 | xz | zip |
|--------|------|-------|-----|-----|
| Archiver + compresser | `tar -cvzf file.tar.gz dir/` | `tar -cvjf file.tar.bz2 dir/` | `tar -cvJf file.tar.xz dir/` | `zip -r file.zip dir/` |
| Lister | `tar -tvzf file.tar.gz` | `tar -tvjf file.tar.bz2` | `tar -tvJf file.tar.xz` | `unzip -l file.zip` |
| Extraire | `tar -xvzf file.tar.gz` | `tar -xvjf file.tar.bz2` | `tar -xvJf file.tar.xz` | `unzip file.zip` |

---

## 10. Bonnes pratiques

1. **Utilisez .tar.xz** pour l'archivage long terme (meilleure compression)
2. **Utilisez .tar.gz** pour les transferts rapides
3. **Utilisez zip** pour partager avec Windows/Mac
4. **Vérifiez toujours** l'archive après création
5. **Excluez les fichiers inutiles** (cache, node_modules, .git)
6. **Gardez des sauvegardes incrémentales**
7. **Testez la restauration** régulièrement !

---

Ces commandes sont essentielles pour tout administrateur Linux ! 💪