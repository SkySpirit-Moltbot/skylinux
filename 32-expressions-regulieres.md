# Leçon 32 : Expressions Régulières (Regex)

Dans cette leçon, tu vas découvrir les expressions régulières (Regex), un outil puissant pour rechercher et manipuler du texte. Utilisées avec `grep`, `sed`, `awk` et bien d'autres commandes, les Regex te permettront de trouver exactement ce que tu cherches, même dans des fichiers complexes.

---

## 1. Qu'est-ce qu'une expression régulière ?

Une **expression régulière** (Regex) est un motif (pattern) qui décrit un ensemble de chaînes de caractères. C'est un langage de recherche avancées qui permet de :

- Rechercher un texte dans un fichier
- Valider un format (email, numéro de téléphone, etc.)
- Extraire des parties d'un texte
- Remplacer du texte automatiquement

Les Regex sont omniprésentes sur Linux : dans `grep`, `sed`, `awk`, `find`, `perl`, et même dans de nombreux éditeurs de texte et langages de programmation.

---

## 2. Les métacaractères de base

Les métacaractères sont les symboles spéciaux qui donnent tout leur pouvoir aux Regex.

| Métacaractère | Signification | Exemple |
|---|---|---|
| `.` | N'importe quel caractère (sauf saut de ligne) | `a.c` → "aac", "abc", "a1c" |
| `^` | Début de ligne | `^Bonjour` → lignes commençant par "Bonjour" |
| `$` | Fin de ligne | `soir$` → lignes finissant par "soir" |
| `*` | 0 ou plus du caractère précédent | `ab*c` → "ac", "abc", "abbc" |
| `+` | 1 ou plus du caractère précédent | `ab+c` → "abc", "abbc" (pas "ac") |
| `?` | 0 ou 1 du caractère précédent | `ab?c` → "ac", "abc" |
| `[ ]` | Classe de caractères | `[aeiou]` → n'importe quelle voyelle |
| `[^ ]` | Négation d'une classe | `[^0-9]` → tout sauf un chiffre |
| `\` | Échappement | `\.` → le caractère point literal |
| `|` | OU logique | `cat\|dog` → "cat" ou "dog" |
| `( )` | Groupement | `(ab)+` → "ab", "abab", "ababab" |
| `{n}` | Exactement n fois | `a{3}` → "aaa" |
| `{n,m}` | Entre n et m fois | `a{2,4}` → "aa", "aaa", "aaaa" |

---

## 3. Les classes de caractères abrégées

| Classe | Équivalent | Signification |
|---|---|---|
| `\d` | `[0-9]` | Un chiffre |
| `\D` | `[^0-9]` | Tout sauf un chiffre |
| `\w` | `[a-zA-Z0-9_]` | Un caractère alphanumérique |
| `\W` | `[^a-zA-Z0-9_]` | Tout sauf un caractère alphanumérique |
| `\s` | `[ \t\n\r\f]` | Un espace blanc |
| `\S` | `[^ \t\n\r\f]` | Tout sauf un espace blanc |

---

## 4. grep — Recherche dans les fichiers

`grep` est la commande la plus utilisée pour rechercher du texte avec des Regex.

### Syntaxe de base

```bash
grep "motif" fichier
```

### Recherche basique

```bash
# Rechercher une ligne contenant "error"
grep "error" /var/log/syslog

# Rechercher sans tenir compte de la casse
grep -i "error" /var/log/syslog

# Rechercher récursivement dans un dossier
grep -r "error" /var/log/

# Afficher les numéros de ligne
grep -n "error" fichier.log
```

### Utiliser les Regex avec grep

```bash
# Activer les Regex étendues (plus de métacaractères)
grep -E "expression" fichier

# Ou utiliser egrep (équivalent)
egrep "erreur|warning" /var/log/syslog
```

### Exemples concrets

```bash
# Lignes commençant par "Error"
grep -E "^Error" log.txt

# Lignes finissant par ".log"
grep -E "\.log$" fichier.txt

# Lignes contenant "a" puis n'importe quoi puis "b"
grep -E "a.*b" fichier.txt

# Lignes contenant un chiffre
grep -E "[0-9]" fichier.txt

# Lignes contenant un mot de 3 lettres
grep -E "\b[a-z]{3}\b" fichier.txt
```

---

## 5. sed — Recherche et remplacement

`sed` permet de rechercher ET remplacer du texte avec des Regex.

### Syntaxe de base

```bash
sed 's/ancien/nouveau/' fichier
```

Le `s` veut dire "substitute" (remplacer).

### Remplacement simple

```bash
# Remplacer la première occurrence de "foo" par "bar" sur chaque ligne
sed 's/foo/bar/' fichier.txt

# Remplacer TOUTES les occurrences (flag g = global)
sed 's/foo/bar/g' fichier.txt

# Remplacer sur plusieurs fichiers
sed -i 's/foo/bar/g' fichier1.txt fichier2.txt
```

### Avec les Regex

```bash
# Remplacer tout chiffre par un X
sed -E 's/[0-9]/X/g' fichier.txt

# Remplacer un format IP (ex: 192.168.1.1) par "REDACTED"
sed -E 's/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/REDACTED/g' fichier.txt

# Supprimer les lignes vides
sed '/^$/d' fichier.txt

# Supprimer les lignes commençant par #
sed '/^#/d' fichier.txt

# Ajouter du texte avant chaque ligne
sed -E 's/^/PREFIXE: /' fichier.txt
```

### Capturer des groupes

Les parenthèses `()` créent des groupes, et `\1`, `\2` font référence à ces groupes :

```bash
# Inverser deux mots séparés par un tiret (a-b → b-a)
sed -E 's/([a-z]+)-([a-z]+)/\2-\1/g' fichier.txt

# Extraire le domaine d'un email
echo "utilisateur@exemple.com" | sed -E 's/.*@([^.]+)\..*/\1/'
# Résultat : exemple
```

---

## 6. awk — Manipulation de texte avancée

`awk` est extrêmement puissant pour traiter du texte structuré (comme des tableaux ou des logs).

### Syntaxe de base

```bash
awk '/motif/ { action }' fichier
```

### Exemples concrets

```bash
# Afficher la première colonne (par défaut, séparateur = espace)
awk '{ print $1 }' fichier.txt

# Afficher la première et la troisième colonne
awk '{ print $1, $3 }' fichier.txt

# Spécifier un séparateur de champ (ex: deux-points)
awk -F: '{ print $1, $7 }' /etc/passwd

# Rechercher et afficher certaines colonnes
awk -F: '/^root/ { print $1, $7 }' /etc/passwd

# Afficher les lignes avec plus de 80 caractères
awk 'length > 80' fichier.txt

# Additionner une colonne numérique
awk '{ sum += $1 } END { print sum }' fichier.txt
```

### Avec les Regex dans awk

```bash
# Lignes contenant un email
awk '/[a-z]+@[a-z]+\.[a-z]+/' fichier.txt

# Lignes où la 3ème colonne est un nombre > 100
awk '$3 > 100' fichier.txt

# Afficher les lignes où le champ 2 contient "ERREUR"
awk -F, '$2 ~ /ERREUR/ { print $1, $2 }' logs.csv
```

---

## 7. find — Rechercher des fichiers par nom

```bash
# Rechercher des fichiers se terminant par .log
find . -name "*.log"

# Rechercher des fichiers dont le nom contient "error"
find . -name "*error*"

# Rechercher des fichiers de plus de 100 Mo
find . -size +100M

# Rechercher des fichiers modifiés dans les 7 derniers jours
find . -mtime -7

# Combiner avec grep (chercher dans le contenu)
find . -name "*.txt" -exec grep -l "motif" {} \;
```

---

## 8. Exercices pratiques

### Exercice 1 : Débogage avec grep

```bash
# 1. Lis les logs système
cat /var/log/syslog | head -20

# 2. Cherche les lignes contenant "error" (insensible à la casse)
grep -i error /var/log/syslog | head -10

# 3. Cherche les lignes contenant "error" OU "warning"
grep -iE "error|warning" /var/log/syslog | head -10

# 4. Affiche les 2 lignes après chaque correspondance
grep -iA 2 "error" /var/log/syslog | head -20
```

### Exercice 2 : Nettoyage de texte avec sed

```bash
# 1. Crée un fichier test
echo "Serveur1: 192.168.1.1 - OK" > test.txt
echo "Serveur2: 10.0.0.5 - ERREUR" >> test.txt
echo "Serveur3: 172.16.0.1 - OK" >> test.txt

# 2. Remplace "ERREUR" par "FAILED"
sed -i 's/ERREUR/FAILED/g' test.txt

# 3. Remplace les adresses IP par "XXX.XXX.XXX.XXX"
sed -iE 's/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/XXX.XXX.XXX.XXX/g' test.txt

# 4. Affiche le résultat
cat test.txt
```

### Exercice 3 : Extraction de données avec awk

```bash
# 1. Crée un fichier CSV test
echo "Prenom,Nom,Age,Ville" > personnes.csv
echo "Jean,Dupont,28,Paris" >> personnes.csv
echo "Marie,Martin,34,Lyon" >> personnes.csv
echo "Pierre,Durand,45,Bruxelles" >> personnes.csv

# 2. Affiche seulement les noms
awk -F, '{ print $2 }' personnes.csv

# 3. Affiche les personnes de plus de 30 ans
awk -F, '$3 > 30 { print $1, $2, $3 }' personnes.csv

# 4. Ajoute une colonne calculée
awk -F, '{ print $1, $2, $3*12 " mois" }' personnes.csv
```

### Exercice 4 : Validation de format

```bash
# Vérifier si une variable correspond à un format
email="utilisateur@exemple.com"

# Avec grep et regex
if echo "$email" | grep -qE "^[a-z]+@[a-z]+\.[a-z]{2,}$"; then
    echo "Email valide"
else
    echo "Email invalide"
fi

# Vérifier un numéro de téléphone suisse
tel="079 456 96 45"
if echo "$tel" | grep -qE "^[0-9]{3} [0-9]{3} [0-9]{2} [0-9]{2}$"; then
    echo "Numéro suisse valide"
fi
```

---

## 9. Patterns courants à retenir

| Besoin | Pattern | Exemple |
|---|---|---|
| Email simple | `[a-z]+@[a-z]+\.[a-z]{2,}` | `test@exemple.com` |
| Numéro suisse | `[0-9]{3} [0-9]{3} [0-9]{2} [0-9]{2}` | `079 456 96 45` |
| Adresse IP v4 | `[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}` | `192.168.1.1` |
| Date JJ/MM/AAAA | `[0-9]{2}/[0-9]{2}/[0-9]{4}` | `24/03/2026` |
| URL | `https?://[a-z.]+\.[a-z]{2,}` | `https://exemple.com` |
| Mot de 3 à 10 lettres | `\b[a-zA-Z]{3,10}\b` | bonjour |
| Ligne commençant par # | `^#` | commentaires |
| Ligne vide | `^$` | ligne vide |

---

## 10. Résumé des commandes

| Commande | Description |
|---|---|
| `grep "motif" fichier` | Rechercher un motif dans un fichier |
| `grep -E "regex" fichier` | Utiliser les Regex étendues |
| `grep -i "motif" fichier` | Recherche insensible à la casse |
| `grep -n "motif" fichier` | Afficher les numéros de ligne |
| `grep -r "motif" dossier/` | Recherche récursive |
| `sed 's/a/b/g' fichier` | Remplacer a par b (global) |
| `sed -E 's/regex/remp/g'` | Remplacement avec Regex |
| `sed -i 's/a/b/' fichier` | Remplacement sur fichier directement |
| `awk '{ print $1 }' fichier` | Afficher la première colonne |
| `awk -F: '{ print $1 }'` | Spécifier le séparateur (ici `:`) |
| `find . -name "*.txt"` | Rechercher des fichiers par nom |
| `find . -regex ".*\.log"` | Rechercher par Regex |

---

## 11. Aller plus loin

- **Perl/PCRE** : Les Regex de Perl sont encore plus puissantes (supportées par `grep -P`)
- **Langages de programmation** : Python, JavaScript, PHP supportent tous les Regex
- **Outils en ligne** : regex101.com pour tester tes Regex visuellement
- **sed et awk avancés** : utiliser `sed -i` pour modification in-place, `awk` pour du parsing CSV/JSON léger
