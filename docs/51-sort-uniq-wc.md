# Leçon 51 : sort, uniq et wc — Trier, dédoublonner et compter

## Objectif

Maîtriser trois commandes essentielles pour traiter des données textuelles : **sort** (trier), **uniq** (dédoublonner) et **wc** (compter).

## Prérequis

- Savoir utiliser les tubes (pipes) (leçon 15)
- Connaître les bases du terminal (leçon 2)

---

## 1. sort — Trier des lignes

`sort` trie les lignes d'un fichier ou de l'entrée standard.

### Tri basique

```bash
# Trier un fichier alphabétiquement
sort fichier.txt

# Trier numériquement
sort -n nombres.txt

# Trier en ordre inverse
sort -r fichier.txt

# Trier par colonne (ex: colonne 3)
sort -k3 fichier.txt
```

### Options utiles

```bash
# Supprimer les doublons pendant le tri
sort -u fichier.txt

# Trier selon un délimiteur (ex: colonne 2, délimiteur :)
sort -t: -k2 fichier.txt

# Trier numériquement avec去掉 les chaînes non-numériques
sort -V versions.txt
```

### Exemples concrets

```bash
# Trier les processus par mémoire utilisée
ps aux | sort -k4 -rn | head -10

# Trier les fichiers par taille
ls -la | sort -k5 -rn

# Trier un fichier CSV par la colonne 3
sort -t',' -k3 usernames.csv
```

---

## 2. uniq — Supprimer les doublons

`uniq` supprime les lignes adjacentes identiques. Utile après un tri.

### Utilisation basique

```bash
# Supprimer les lignes identiques consécutives
uniq fichier.txt

# Compter les occurrences de chaque ligne
uniq -c fichier.txt

# Afficher uniquement les lignes DUPLIQUÉES
uniq -d fichier.txt

# Afficher les lignes qui apparaissent une seule fois
uniq -u fichier.txt
```

### Combinaison avec sort

```bash
# Supprimer TOUS les doublons (y compris non-adjacents)
sort fichier.txt | uniq

# Compter les occurrences uniques
sort fichier.txt | uniq -c | sort -rn

# Trouver les 10 mots les plus fréquents
cat words.txt | sort | uniq -c | sort -rn | head -10
```

---

## 3. wc — Compter

`wc` (word count) compte les lignes, mots et caractères.

### Commandes de base

```bash
# Compter les lignes
wc -l fichier.txt

# Compter les mots
wc -w fichier.txt

# Compter les caractères
wc -c fichier.txt

# Tout afficher (lignes, mots, caractères, fichier)
wc fichier.txt
```

### Exemples concrets

```bash
# Compter le nombre de fichiers dans un répertoire
ls -1 | wc -l

# Compter les lignes de code dans un projet
find . -name "*.py" -exec cat {} \; | wc -l

# Compter le nombre d'utilisateurs
cat /etc/passwd | wc -l

# Compter les lignes dans plusieurs fichiers
wc -l *.log
```

---

## 4. Combiner les trois

```bash
# Trouver les 5 IP les plus fréquentes dans les logs
cat /var/log/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5

# Lister les utilisateurs uniques connectés
who | awk '{print $1}' | sort | uniq

# Compter les lignes de chaque type d'erreur
grep "ERROR" app.log | wc -l

# Analyser les connexions SSH
last | awk '{print $1}' | sort | uniq -c | sort -rn
```

---

## Exercices pratiques

1. **Tri simple** — Trie le fichier `/etc/passwd` par ordre alphabétique des noms d'utilisateurs.

2. **Dédoublonnage** — À partir d'une liste de mots avec doublons, affiche uniquement les mots uniques.

3. **Statistiques** — À partir du fichier `/var/log/syslog`, compte combien de fois chaque programme apparaît.

4. **Analyse** — Trouve les 3 adresses IP qui ont le plus accédé à ton système (utilise `last` ou les logs SSH).

---

## Résumé

| Commande | Rôle | Exemple |
|----------|------|---------|
| `sort` | Trier les lignes | `sort -n fichier.txt` |
| `sort -r` | Trier en ordre inverse | `sort -r liste.txt` |
| `sort -u` | Trier et dédoublonner | `sort -u fichier.txt` |
| `sort -k` | Trier par colonne | `sort -k3 -t: fichier.txt` |
| `uniq` | Supprimer les doublons | `sort fichier | uniq` |
| `uniq -c` | Compter les occurrences | `uniq -c fichier.txt` |
| `uniq -d` | Afficher les doublons | `uniq -d fichier.txt` |
| `wc -l` | Compter les lignes | `wc -l *.log` |
| `wc -w` | Compter les mots | `wc -w document.txt` |

---

## Navigation

[← Leçon 50 : grep, sed et xargs](50-grep-sed-xargs.html) | [Sommaire](index.html)
