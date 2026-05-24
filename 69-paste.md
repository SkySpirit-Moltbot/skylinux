# Leçon 69 : paste — Fusionner des lignes de fichiers

`paste` fusionne des fichiers ligne par ligne. L'équivalent horizontal de `cat` (qui concatène verticalement).

## 1. Principe de base

```bash
# Deux fichiers : prenoms.txt et noms.txt
cat prenoms.txt
# Alice
# Bob
# Charlie

cat noms.txt
# Dupont
# Martin
# Dubois

# Fusionner côte à côte
paste prenoms.txt noms.txt
# Alice	Dupont
# Bob	Martin
# Charlie	Dubois
```

Par défaut, le séparateur est la tabulation.

## 2. Changer le délimiteur

```bash
# Avec -d : délimiteur personnalisé
paste -d ',' prenoms.txt noms.txt
# Alice,Dupont
# Bob,Martin
# Charlie,Dubois

# Délimiteur multiple (alterne)
paste -d ',|' fichier1 fichier2 fichier3 fichier4
# → séparateur 1: ,  séparateur 2: |  séparateur 3: ,  séparateur 4: | ...
```

## 3. Mode série (-s)

```bash
# Sans -s : fusion colonne par colonne (défaut)
paste fichier1 fichier2
# Alice	1
# Bob	2

# Avec -s : tout sur une ligne
paste -s fichier1 fichier2
# Alice	Bob	Charlie
# 1	2	3

# Avec -s et délimiteur
paste -sd ',' fichier1
# Alice,Bob,Charlie
```

## 4. Cas pratiques

```bash
# Créer un CSV à partir de deux fichiers
paste -d ',' ids.txt noms.txt emails.txt > contacts.csv

# Transformer une colonne en ligne (l'inverse de cat)
cat liste.txt | paste -sd ','
# → item1,item2,item3

# Reconstituer /etc/passwd utile
cut -d ':' -f 1 /etc/passwd > users.txt
cut -d ':' -f 7 /etc/passwd > shells.txt
paste -d ' utilise ' users.txt shells.txt

# Numéroter les lignes d'un fichier
seq $(wc -l < fichier.txt) | paste -d '. ' - fichier.txt
```

Le `-` dans paste signifie "lire depuis stdin".

## 5. paste vs join

| Commande | Usage |
|----------|-------|
| `paste` | Fusion simple ligne à ligne |
| `join` | Fusion avec clé commune (comme SQL JOIN) |

```bash
# paste : fusion bête par position
paste ids.txt noms.txt

# join : fusion intelligente sur un champ commun
join -1 1 -2 1 ids.txt noms.txt
```

## 6. Exercices pratiques

1. **Fusion** — Crée deux fichiers de 5 lignes et fusionne-les avec paste
2. **CSV** — Transforme une liste verticale en CSV horizontal avec `paste -sd ','`
3. **Numérotation** — Numérote les lignes d'un fichier avec seq + paste
