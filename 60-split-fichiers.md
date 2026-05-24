# Leçon 60 : split et cat — Diviser et assembler des fichiers

Deux opérations complémentaires : `split` découpe un fichier en morceaux, `cat` les recolle.

## 1. split — Découper un fichier

```bash
# Découper en morceaux de 1000 lignes
split -l 1000 gros_fichier.txt morceau_
# → morceau_aa, morceau_ab, morceau_ac...

# Découper par taille (10 Mo)
split -b 10M grosse_archive.tar.gz partie_
# → partie_aa, partie_ab...

# Découper un CSV en gardant l'en-tête
head -1 data.csv > entete.csv
tail -n +2 data.csv | split -l 50000 - morceau_
for f in morceau_*; do cat entete.csv "$f" > "$f.csv"; done
```

## 2. Options de split

```bash
# -b : taille en octets, Ko, Mo, Go
split -b 100K fichier part_

# -l : nombre de lignes
split -l 5000 fichier part_

# -d : suffixes numériques au lieu de aa, ab, ac
split -d -l 1000 fichier part_
# → part_00, part_01, part_02...

# -n : diviser en N morceaux égaux
split -n 5 fichier part_

# Préfixe personnalisé
split -l 1000 fichier 2026-05-24_section_
```

## 3. cat — Assembler (et plus)

```bash
# Assembler des morceaux = fichier original
cat morceau_* > fichier_reconstitue.txt

# Vérifier : les tailles doivent correspondre
wc -l fichier_reconstitue.txt
wc -l gros_fichier.txt

# Afficher plusieurs fichiers à la suite
cat debut.txt milieu.txt fin.txt

# Numéroter les lignes à l'affichage
cat -n fichier.txt

# Créer un fichier rapidement
cat > nouveau_fichier.txt << 'EOF'
Ligne 1
Ligne 2
EOF
```

## 4. Cas concret : transférer un gros fichier par email

```bash
# Ta pièce jointe fait 30 Mo, la limite est 10 Mo
split -b 9M gros_document.pdf doc_part_

# Résultat : doc_part_aa, doc_part_ab, doc_part_ac, doc_part_ad

# Le destinataire recolle :
cat doc_part_* > gros_document.pdf
```

## 5. Exercices pratiques

1. **Split** — Prends un fichier texte, découpe-le en morceaux de 50 lignes
2. **Cat** — Recolle les morceaux et vérifie que le résultat est identique à l'original
3. **Taille** — Découpe une archive en morceaux de 1 Mo avec des suffixes numériques
