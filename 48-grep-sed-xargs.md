# Leçon 48 : Leçon 50 : grep, sed et xargs — Rechercher, modifier et chaîner

### Objectif

Découvrir trois outils complémentaires pour manipuler du texte en ligne de commande : **grep** (rechercher), **sed** (modifier) et **xargs** (chaîner des commandes).

### Prérequis

Savoir naviguer dans le terminal (leçon 2)

Comprendre les tubes (pipes) (leçon 8)

### 1. grep — Rechercher du texte

grep (Global Regular Expression Print) cherche un motif dans un fichier ou une entrée standard.

# Rechercher "error" dans un fichier

grep "error" /var/log/syslog

# Recherche insensible à la casse

grep -i "warning" app.log

# Afficher les lignes QUI NE contiennent PAS le motif

grep -v "debug" app.log

# Afficher le numéro des lignes

grep -n "error" app.log

# Recherche récursive dans un répertoire

grep -r "failed" /etc/

# Trouver les lignes avec une adresse IP

grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" logs.txt

# Compter le nombre d'occurrences

grep -c "error" app.log

# Afficher 3 lignes avant et après chaque match

grep -B 3 -A 3 "exception" app.log

### 2. sed — Éditeur de flux

sed modifie du texte sans ouvrir de fichier. Il applique des transformations ligne par ligne.

# Remplacer la première occurrence de "foo" par "bar" par ligne

sed 's/foo/bar/' fichier.txt

# Remplacer TOUTES les occurrences (drapeau g)

sed 's/foo/bar/g' fichier.txt

# Modifier le fichier directement (-i)

sed -i 's/localhost/127.0.0.1/g' config.txt

# Remplacer surplace avec backup (.bak)

sed -i.bak 's/old/new/g' config.txt

# Supprimer les lignes contenant un motif

sed '/temporaire/d' logs.txt

# Afficher les lignes 10 à 20

sed -n '10,20p' grand_fichier.txt

# Ajouter du texte après une ligne

sed -i '/pattern/a\Nouvelle ligne' fichier.txt

# Remplacer par une expression régulière

sed -E 's/[0-9]{4}/****/g' fichier.txt

# Remplacer tous les "http://" par "https://" dans un fichier HTML

sed -i 's/http:\/\//https:\/\//g' index.html

# Supprimer tous les espaces de fin de ligne

sed -i 's/[[:space:]]*$//' fichier.txt

### 3. xargs — Construire des commandes

xargs lit des éléments depuis l'entrée standard et les passe comme arguments à une autre commande. Indispensable pour chaîner avec find.

# Compter le nombre de lignes de chaque fichier trouvé

find . -name "*.txt" | xargs wc -l

# Supprimer tous les fichiers .tmp trouvés

find . -name "*.tmp" | xargs rm -f

# Copier tous les fichiers .conf dans backup/

find /etc -name "*.conf" | xargs -I {} cp {} /backup/

# Demander confirmation avant chaque suppression

find . -name "*.log" -mtime +7 | xargs -p rm -f

# Lancer 4 processus en parallèle

find . -name "*.jpg" | xargs -P 4 -I {} convert {} -resize 800x600 {}

### 4. Combiner les trois

# Rechercher les lignes avec "error", remplacer "old" par "new", sauvegarder

grep "error" app.log | sed 's/old/new/g' &gt; app_new.log

# Trouver les fichiers modifiés récemment, afficher leur contenu

find . -mtime -7 -name "*.txt" | xargs grep -l "TODO"

# Nettoyer : trouver les .bak, les compresser, supprimer l'original

find . -name "*.bak" | xargs gzip &amp;&amp; find . -name "*.bak" | xargs rm

### Exercices pratiques

1. **Recherche simple** — Dans /var/log/syslog, trouve toutes les lignes contenant "sshd".

2. **Remplacement** — Dans un fichier config.txt, remplace "port = 8080" par "port = 443" avec sed.

3. **Chaînage** — Trouve tous les fichiers .log dans /var/log/ qui contiennent "error", puis affiche leurs permissions avec ls -l.

4. **Nettoyage** — Trouve tous les fichiers .tmp de plus de 7 jours et supprime-les avec confirmation.

### Navigation

[← Leçon 49 : journalctl](49-journalctl-logs-systemd.html) | [Leçon 51 : sort, uniq et wc](51-sort-uniq-wc.html) | [Sommaire](index.html)

