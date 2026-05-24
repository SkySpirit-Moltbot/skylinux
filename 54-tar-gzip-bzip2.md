# Leçon 54 : tar, gzip et bzip2 — Archiver et compresser

Trois outils complémentaires : `tar` rassemble des fichiers en une archive, `gzip` et `bzip2` compressent. Souvent utilisés ensemble.

## 1. tar — Mettre en archive

```bash
# Créer une archive (regrouper sans compresser)
tar cf mon_archive.tar /home/david/Documents/

# Options :
# c = create (créer)
# f = file (nom du fichier archive)

# Lister le contenu d'une archive
tar tf mon_archive.tar

# Extraire une archive
tar xf mon_archive.tar
```

## 2. tar + gzip = .tar.gz (le standard Linux)

```bash
# Créer une archive compressée (gzip)
tar czf mon_archive.tar.gz /home/david/Documents/
# z = gzip

# Extraire
tar xzf mon_archive.tar.gz

# Taille : gzip compresse bien, décompresse vite
```

## 3. tar + bzip2 = .tar.bz2 (meilleure compression)

```bash
# Créer une archive avec bzip2 (plus lent, plus efficace)
tar cjf mon_archive.tar.bz2 /home/david/Documents/
# j = bzip2

# Extraire
tar xjf mon_archive.tar.bz2
```

## 4. Comparaison gzip vs bzip2

| Format | Compression | Vitesse | Usage typique |
|--------|------------|---------|---------------|
| `.tar.gz` | Bonne | Rapide | Usage général |
| `.tar.bz2` | Meilleure | Lent | Archives finales, distribution |
| `.tar.xz` | Excellente | Très lent | Très gros volumes |

## 5. gzip et bzip2 seuls (fichier unique)

```bash
# Compresser un fichier
gzip fichier.txt          # → fichier.txt.gz
bzip2 fichier.txt         # → fichier.txt.bz2

# Décompresser
gunzip fichier.txt.gz     # → fichier.txt
bunzip2 fichier.txt.bz2   # → fichier.txt

# Garder l'original après compression
gzip -k fichier.txt       # garde fichier.txt + crée fichier.txt.gz

# Voir le taux de compression
gzip -l fichier.txt.gz
```

## 6. Exemples concrets

```bash
# Sauvegarder /etc en une archive compressée
sudo tar czf /tmp/etc-backup-$(date +%Y%m%d).tar.gz /etc/

# Extraire un seul fichier d'une archive
tar xzf mon_archive.tar.gz chemin/vers/fichier.txt

# Créer une archive SANS le chemin complet
tar czf docs.tar.gz -C /home/david/Documents .

# Voir ce qui serait extrait (dry-run... pas vraiment, utiliser -t)
tar tzf archive.tar.gz | head -20
```

## 7. Exercices pratiques

1. **Archive** — Crée une archive `.tar.gz` de ton dossier `~/Documents`
2. **Liste** — Affiche le contenu de l'archive avec `tar tzf`
3. **Extraction** — Extrais l'archive dans `/tmp/test-extract/`
4. **Comparaison** — Compresse un gros fichier avec gzip puis bzip2, compare les tailles avec `ls -lh`
