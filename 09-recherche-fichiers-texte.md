# Leçon 09 : Recherche de fichiers et texte

Dans cette leçon, nous allons maîtriser les outils de recherche sous Linux. Ces commandes sont essentielles pour tout administrateur ou développeur.

---

## 1. FIND - Recherche de fichiers

`find` est l'outil de recherche le plus puissant sous Linux. Il recherche récursivement selon de nombreux critères.

### Syntaxe de base

```bash
find [chemin] [expression]
```

### Rechercher par nom

```bash
find . -name "fichier.txt"              # Nom exact
find . -name "*.txt"                    # Par extension
find . -name "fichier*"                 # Par début de nom
find . -iname "Fichier.txt"             # Insensible à la casse
find . -name "*.log" -o -name "*.txt"   # OU (plusieurs extensions)
```

### Rechercher par type

```bash
find . -type f          # Fichiers seulement
find . -type d          # Répertoires seulement
find . -type l          # Liens symboliques
find . -type s          # Sockets
find . -type p          # Pipes nommés
```

### Rechercher par taille

```bash
find . -size +100M              # Plus de 100 Mo
find . -size -1G                # Moins de 1 Go
find . -size +100k -size -1M    # Entre 100 Ko et 1 Mo
```

### Rechercher par date

```bash
find . -mtime -7           # Modifiés dans les 7 derniers jours
find . -mtime +30          # Modifiés il y a plus de 30 jours
find . -atime -1           # Accédés dans les 24h
find . -ctime -1           # Changés dans les 24h (permissions, contenu)
find . -newer fichier.txt  # Plus récents que fichier.txt
```

### Rechercher par permissions

```bash
find . -perm 644           # Permissions exactement 644
find . -perm -u+x          # Avec bit exécutable pour owner
find . -perm -g=w          # Avec bit écriture pour groupe
```

### Rechercher par propriétaire

```bash
find . -user david         # Propriétaire david
find . -group admin        # Groupe admin
find . -uid 1000           # UID 1000
```

### Rechercher par profondeur

```bash
find . -maxdepth 2         # Maximum 2 niveaux
find . -mindepth 2        # Au moins 2 niveaux
find . -depth 2           # Exactement 2 niveaux
```

### Actions avec find

```bash
# Lister (par défaut -print)
find . -name "*.txt" -print

# Supprimer
find . -name "*.tmp" -delete

# Exécuter une commande
find . -name "*.log" -exec rm {} \;         # Supprimer tous les .log
find . -name "*.txt" -exec wc -l {} \;      # Compter lignes
find . -type f -exec chmod 644 {} \;        # Changer permissions

# Confirmation avant action (-ok)
find . -name "*.bak" -ok rm {} \;            # Demande confirmation

# Plusieurs fichiers
find . -name "*.txt" -exec cp {} {}.bak \;
```

---

## 2. GREP - Recherche de texte

`grep` recherche des motifs (patterns) dans des fichiers.

### Syntaxe de base

```bash
grep [options] "motif" [fichiers]
```

### Options essentielles

| Option | Description |
|--------|-------------|
| `-i` | Insensible à la casse |
| `-n` | Afficher numéros de ligne |
| `-l` | Afficher seulement noms de fichiers |
| `-c` | Compter les occurrences |
| `-v` | Inverser la recherche |
| `-r` | Récursif |
| `-w` | Mot entier |
| `-x` | Ligne entière |
| `-A n` | Afficher n lignes après |
| `-B n` | Afficher n lignes avant |
| `-C n` | Contexte (avant et après) |

### Exemples pratiques

```bash
# Recherche basique
grep "erreur" log.txt

# Avec contexte
grep -n "erreur" log.txt              # Numéros de ligne
grep -C 2 "erreur" log.txt           # 2 lignes avant et après
grep -A 3 "error" log.txt            # 3 lignes après

# Plusieurs fichiers
grep -r "function" *.js              # Dans tous les JS
grep -l "TODO" *                     # Fichiers contenant TODO

# Compter
grep -c "erreur" log.txt              # Nombre d'occurrences
grep -w -c "mot" fichier.txt         # Mots entiers

# Inverser
grep -v "^#" config.txt              # Lignes qui ne commencent pas par #

# Expressions régulières
grep "^debut" fichier.txt             # Ligne commençant par "debut"
grep "fin$" fichier.txt               # Ligne finissant par "fin"
grep "colou?r" fichier.txt            # color ou colour
grep "[0-9]" fichier.txt             # Contient un chiffre
grep -E "[a-z]+@[a-z.]+" fichier.txt # Email simple
```

### EGREP et FGREP

```bash
egrep "mot1|mot2|mot3" fichier.txt   # Étendu (équivalent grep -E)
fgrep "texte.literal" fichier.txt    # Littéral (équivalent grep -F)
```

---

## 3. LOCATE - Recherche rapide

`locate` utilise une base de données pré-construite (updatedb), ce qui le rend très rapide.

### Commandes de base

```bash
locate fichier.txt           # Rechercher par nom
locate -i fichier.txt        # Insensible à la casse
locate "*.txt"              # Avec wildcard
```

### Options utiles

```bash
locate -c                    # Compter les résultats
locate -l 10                 # Limiter à 10 résultats
locate -i -l 5 "document"   # Limiter et insensible
```

### Mettre à jour la base

```bash
sudo updatedb               # Mettre à jour la base (nécessite root)
```

> ⚠️ **Note** : locate ne trouve pas les fichiers créés depuis la dernière mise à jour de la base.

---

## 4. WHICH, WHEREIS, TYPE - Recherche de commandes

### which - Trouver une commande

```bash
which python                 # Chemin de python
which -a python              # Toutes les occurrences
which -s python             # Silence (0 si trouvé)
```

### whereis - Localiser binary, source, man

```bash
whereis python              # Binary, source et man
whereis -m python           # Seulement les pages man
whereis -s python           # Seulement les sources
whereis -b python           # Seulement les binaires
```

### type - Type de commande

```bash
type ls                     # alias, function, ou builtin
type -t ls                  # Alias, builtin, file, function
type -a ls                  # Toutes les définitions
```

---

## 5. Statistiques et comptage

### wc - Compter lignes, mots, caractères

```bash
wc fichier.txt              # Lignes mots octets
wc -l fichier.txt           # Nombre de lignes
wc -w fichier.txt           # Nombre de mots
wc -c fichier.txt           # Nombre d'octets
wc -m fichier.txt           # Nombre de caractères
```

### sort - Trier

```bash
sort fichier.txt            # Trier alphabétiquement
sort -n fichier.txt         # Trier numériquement
sort -r fichier.txt         # Inverser l'ordre
sort -u fichier.txt         # Trier et supprimer doublons
sort -k2 fichier.txt        # Trier par colonne 2
```

### uniq - Lignes uniques

```bash
uniq fichier.txt            # Supprimer doublons adjacents
uniq -c fichier.txt         # Avec compteur
uniq -d fichier.txt        # Afficher seulement doublons
uniq -u fichier.txt        # Afficher lignes uniques
```

---

## 6. Recherche avancée combinée

### Rechercher et traiter

```bash
# Trouver puis exécuter
find . -name "*.log" -exec wc -l {} \; | sort -n

# Rechercher du texte dans les résultats
find . -name "*.txt" | xargs grep "erreur"

# Rechercher avec confirmation
find . -name "*.bak" -ok rm {} \;

# Compter occurrences dans plusieurs fichiers
grep -r "error" . --include="*.log" | wc -l

# Lister fichiers modifiés récemment
find . -mtime -1 -type f
```

---

## 7. Exercices pratiques

### Exercice 1 : Trouver tous les fichiers PHP modifiés récemment
```bash
find . -name "*.php" -mtime -7
```

### Exercice 2 : Rechercher une fonction dans le code
```bash
grep -rn "function maFonction" --include="*.js" .
```

### Exercice 3 : Compter les lignes de code
```bash
find . -name "*.py" -exec wc -l {} \; | awk '{sum+=$1} END {print sum}'
```

### Exercice 4 : Supprimer tous les fichiers temporaires
```bash
find . -name "*.tmp" -type f -delete
```

### Exercice 5 : Rechercher dans les logs d'erreurs
```bash
grep -i "error\|fail\|critical" /var/log/syslog | tail -20
```

---

## 8. Tableau résumé

| Commande | Utilisation |
|----------|-------------|
| `find` | Recherche multicritères de fichiers |
| `grep` | Recherche de texte dans fichiers |
| `locate` | Recherche rapide par base de données |
| `which` | Trouver le chemin d'une commande |
| `whereis` | Localiser binary, source, man |
| `type` | Déterminer le type de commande |
| `wc` | Compter lignes/mots/caractères |
| `sort` | Trier un fichier |
| `uniq` | Lignes uniques |

---

Maîtrise ces outils et tu pourras trouver n'importe quoi sur ton système Linux ! 🔍
---

## Complément: find avancé

### Syntaxe de base

Par défaut, find parcourt récursivement tous les sous-répertoires à partir du chemin indiqué.

### Recherche par nom

Recherche le fichier rapport.txt dans /home.

Recherche tous les fichiers se terminant par .log.

Recherche tous les fichiers PDF.

L'option -iname ignore la casse (README, readme, Readme...).

### Recherche par type

Recherche un répertoire nommé "Backup".

Liste tous les liens symboliques dans /var.

### Recherche par taille

Trouve tous les fichiers de plus de 100 Mo dans /home.

Trouve les fichiers log de plus de 1 Go.

### Recherche par date

Trouve les fichiers modifiés dans les 7 derniers jours.

Trouve les fichiers log non modifiés depuis plus de 30 jours.

Trouve les fichiers non accédés depuis plus d'un an.

### Recherche par permissions

Trouve les fichiers avec les permissions exactes 644.

Trouve les fichiers qui ont au moins le bit d'écriture pour le propriétaire.

Trouve les fichiers accessibles en écriture par quelqu'un.

### Recherche par propriétaire

Trouve les fichiers appartenant à l'utilisateur david.

Trouve les fichiers belonging au groupe developers.

Trouve les fichiers sans propriétaire valide (utilisateur supprimé).

### Combinaison de critères

Trouve les fichiers .txt de plus de 1 Mo.

Trouve les fichiers JPEG ou PNG.

Trouve les fichiers .log non modifiés récemment (équivalent à +7).

Trouve les documents Word modifiés dans les 30 derniers jours.

### Actions sur les résultats

Affiche un listing détaillé des résultats.

Supprime les fichiers temporaires trouvés. Attention : vérifiez d'abord sans -delete !

Supprime tous les fichiers .bak. Le {} est remplacé par le nom du fichier trouvé.

Copie tous les fichiers JPEG vers /backup/photos/.

Demande confirmation avant de supprimer chaque fichier.

Archive tous les fichiers log trouvés.

### Limiter la profondeur de recherche

Recherche uniquement dans les 2 premiers niveaux de répertoires.

Recherche uniquement à partir du 3ème niveau.

Liste uniquement les répertoires immédiats de /home.

### Recherche vide

Trouve les fichiers et répertoires vides.

Supprime tous les fichiers et répertoires vides dans /tmp.

### Exemples pratiques

Afficheinformations détaillées des fichiers de plus de 100 Mo.

Affiche les fichiers modifiés aujourd'hui par david.

Supprime les fichiers temporaires non accédés depuis 7 jours.

Trouve les liens symboliques qui pointent vers des fichiers inexistants.

Trouve le fichier avec l'inode 12345678 (utile pour supprimer les fichiers spéciaux).

Crée une archive de tous les fichiers du site web modifiés cette semaine.

### Performance

Pour les recherches fréquentes ou sur de grandes arborescences, quelques conseils :

Spécifiez toujours le chemin de départ le plus précis possible
Utilisez -maxdepth pour limiter la profondeur si possible

Placez les critères les plus restrictifs en premier

Pour une recherche par nom uniquement, locate peut être plus rapide (base de données), mais find est toujours à jour

### Résumé

La commande find est un outilextrêmement puissant pour rechercher des fichiers selon de multiples critères. Combinez les options pour créer des recherches très précises, et utilisez -exec ou xargs pour effectuer des actions sur les résultats.

L'essentiel à retenir :

find /chemin -name "*.ext" — recherche basique par extension

-type f/d/l — filtre par type de fichier

-size +100M — filtre par taille

-mtime -7 — filtre par date de modification

-exec cmd {} \; — exécute une commande sur chaque résultat

-delete — supprime les fichiers trouvés (avec prudence !)
