# Leçon 8 : Archivage et compression

## Introduction

Dans cette leçon, nous allons apprendre à **archiver** et **compresser** des fichiers sous Linux. C'est très utile pour :
- Réduire la taille de gros dossiers
- Sauvegarder des fichiers
- Transférer des données plus rapidement

---

## Commandes principales

### 1. TAR - Archiver sans compression

**Créer une archive :**
```bash
tar -cvf mon_archive.tar dossier/
```

**Extraire une archive :**
```bash
tar -xvf mon_archive.tar
```

### 2. TAR + GZIP - Compression .tar.gz

**Créer :**
```bash
tar -cvzf archive.tar.gz dossier/
```

**Extraire :**
```bash
tar -xvzf archive.tar.gz
```

### 3. TAR + BZIP2 - Compression .tar.bz2

**Créer :**
```bash
tar -cvjf archive.tar.bz2 dossier/
```

**Extraire :**
```bash
tar -xvjf archive.tar.bz2
```

### 4. ZIP - Format universel

**Créer :**
```bash
zip -r archive.zip dossier/
```

**Extraire :**
```bash
unzip archive.zip
```

---

## Options utiles

| Option | Description |
|--------|-------------|
| -c | Créer une archive |
| -x | Extraire |
| -v | Mode verbeux (affiche les fichiers) |
| -f | Nom du fichier |
| -z | Compression gzip |
| -j | Compression bzip2 |
| -r | Récursif (dossiers) |

---

## Exemples pratiques

### Sauvegarder un dossier personnel
```bash
tar -cvzf backup_home.tar.gz ~/Documents
```

### Créer une archive de plusieurs dossiers
```bash
tar -cvzf mes_fichiers.tar.gz ~/Documents ~/Images ~/Vidéos
```

### Lister le contenu d'une archive sans extraire
```bash
tar -tvf archive.tar.gz
```

---

## Résumé

| Commande | Extension | Compression |
|----------|-----------|-------------|
| tar | .tar | Aucune |
| tar + gzip | .tar.gz | Moyenne |
| tar + bzip2 | .tar.bz2 | Haute |
| zip | .zip | Moyenne |

---

## Exercice

1. Crée un dossier "test" avec quelques fichiers
2. Crée une archive compressée : `tar -cvzf test.tar.gz test/`
3. Supprime le dossier original
4. Extrait l'archive : `tar -xvzf test.tar.gz`

---

*N'hésitez pas à pratiquer !*
