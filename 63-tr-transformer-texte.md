# Leçon 63 : tr — Transformez du texte facilement

`tr` (translate) remplace ou supprime des caractères. Simple, rapide, parfait pour nettoyer du texte en pipeline.

## 1. Remplacer des caractères

```bash
# Syntaxe : tr 'anciens' 'nouveaux'

# Remplacer a par X, b par Y, c par Z
echo "abc" | tr 'abc' 'XYZ'
# → XYZ

# Tout en majuscules
echo "bonjour" | tr 'a-z' 'A-Z'
# → BONJOUR

# Tout en minuscules
echo "BONJOUR" | tr 'A-Z' 'a-z'
# → bonjour
```

## 2. Supprimer des caractères (-d)

```bash
# Supprimer tous les chiffres
echo "abc123def456" | tr -d '0-9'
# → abcdef

# Supprimer les retours chariot Windows (\r)
tr -d '\r' < fichier_windows.txt > fichier_linux.txt

# Supprimer les espaces
echo "a b c" | tr -d ' '
# → abc
```

## 3. Comprimer les répétitions (-s)

```bash
# Remplacer les espaces multiples par un seul
echo "a    b     c" | tr -s ' '
# → a b c

# Remplacer les sauts de ligne multiples
cat fichier.txt | tr -s '\n'

# Supprimer les lignes vides
cat fichier.txt | tr -s '\n' '\n'
```

## 4. Cas pratiques

```bash
# Nettoyer un CSV : remplacer les virgules par des tabulations
cat data.csv | tr ',' '\t' > data.tsv

# Transformer une liste verticale en horizontale
seq 1 10 | tr '\n' ' '
# → 1 2 3 4 5 6 7 8 9 10

# Extraire seulement les chiffres d'une ligne
echo "Commande #42: 150 CHF" | tr -d -c '0-9'
# → 42150

# -c = complement (tout SAUF ce qui est spécifié)

# ROT13 (chiffrement léger)
echo "secret" | tr 'a-zA-Z' 'n-za-mN-ZA-M'
```

## 5. tr + cut : combo gagnant

```bash
# Extraire les noms d'utilisateurs séparés par des espaces
who | tr -s ' ' | cut -d ' ' -f 1

# Nettoyer la sortie de ps
ps aux | tr -s ' ' | cut -d ' ' -f 11-
```

## 6. Exercices pratiques

1. **Majuscules** — Transforme un fichier texte en majuscules avec tr
2. **Nettoyage** — Supprime tous les chiffres d'une chaîne
3. **Espaces** — Nettoie un fichier avec des espaces multiples en un seul espace par ligne
