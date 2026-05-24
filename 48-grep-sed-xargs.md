# Leçon 48 : grep, sed et xargs — Rechercher, modifier et chaîner

Dans cette leçon, tu vas maîtriser trois outils fondamentaux pour traiter du texte en ligne de commande : `grep` pour chercher, `sed` pour modifier, et `xargs` pour enchaîner des commandes.

## 1. grep — Rechercher dans du texte

`grep` cherche des motifs dans des fichiers ou dans le flux d'entrée.

```bash
# Syntaxe de base
grep [options] "motif" fichier

# Chercher un mot dans un fichier
grep "erreur" /var/log/syslog

# Ignorer la casse (majuscule/minuscule)
grep -i "erreur" /var/log/syslog

# Chercher récursivement dans tous les fichiers d'un dossier
grep -r "TODO" ~/projets/

# Afficher le numéro de ligne
grep -n "fonction" script.sh

# Compter les occurrences
grep -c "200" access.log

# Inverser : lignes qui ne contiennent PAS le motif
grep -v "DEBUG" app.log

# Motif exact (mot entier)
grep -w "port" config.txt

# Afficher le nom du fichier pour chaque correspondance
grep -l "FIXME" *.c
```

**Astuce** : combine grep avec un pipe pour filtrer la sortie d'une autre commande :

```bash
ps aux | grep firefox
dmesg | grep -i usb
history | grep rsync
```

## 2. Expressions régulières avec grep

```bash
# Lignes qui commencent par "root"
grep "^root" /etc/passwd

# Lignes qui finissent par ".conf"
grep "\.conf$" /etc/file_list.txt

# L'un ou l'autre (erreur OU warning)
grep -E "erreur|warning" /var/log/syslog

# Un chiffre suivi de "Go"
grep -E "[0-9]+Go" disque_info.txt
```

## 3. sed — Modifier du texte en flux

`sed` (stream editor) modifie du texte ligne par ligne. Idéal pour des remplacements automatisés.

```bash
# Syntaxe : sed 's/motif/remplacement/' fichier

# Remplacer la première occurrence par ligne
sed 's/rouge/bleu/' fichier.txt

# Remplacer TOUTES les occurrences par ligne
sed 's/rouge/bleu/g' fichier.txt

# Modifier le fichier sur place (--in-place)
sed -i 's/192.168.1.1/10.0.0.1/g' config.conf

# Supprimer les lignes vides
sed '/^$/d' fichier.txt

# Supprimer une ligne spécifique (la 5e)
sed '5d' fichier.txt

# Afficher seulement les lignes 10 à 20
sed -n '10,20p' fichier.txt

# Sauvegarder l'original avant modification
sed -i.bak 's/old/new/g' config.conf
# → crée config.conf.bak avant de modifier config.conf
```

**Cas concret** : changer toutes les occurrences d'une IP dans 50 fichiers de config :

```bash
sed -i 's/192.168.1.100/10.0.50.100/g' /etc/app/configs/*.conf
```

## 4. xargs — Transformer des résultats en arguments

`xargs` prend chaque ligne de l'entrée standard et la passe comme argument à une commande.

```bash
# Sans xargs : rm ne peut pas lire depuis stdin
# ❌ find . -name "*.tmp" | rm

# Avec xargs : chaque fichier devient un argument de rm
find . -name "*.tmp" | xargs rm

# Traiter les noms avec des espaces (important !)
find . -name "*.log" -print0 | xargs -0 rm

# Afficher ce qui va être exécuté (dry-run)
ls *.txt | xargs -t rm

# Limiter le nombre d'arguments par lot
echo {1..100} | xargs -n 5
# Résultat : 1 2 3 4 5
#           6 7 8 9 10
#           ...

# Exécuter en parallèle (plus rapide !)
find . -name "*.jpg" | xargs -P 4 -I {} convert {} -resize 50% small/{}
```

## 5. La puissance de la combinaison

```bash
# Trouver tous les "TODO" dans les scripts Python et les compter
grep -r "TODO" ~/projets/ --include="*.py" | wc -l

# Remplacer "localhost" par "mon-serveur.local" dans tous les .conf
grep -rl "localhost" /etc/ | xargs sed -i 's/localhost/mon-serveur.local/g'

# Trouver les 5 plus gros fichiers .log et afficher leur taille
find /var/log -name "*.log" -type f | xargs ls -lhS | head -5
```

## 6. Exercices pratiques

1. **grep** — Trouve toutes les lignes contenant "error" (insensible à la casse) dans `/var/log/syslog`
2. **sed** — Crée un fichier test et remplace toutes les occurrences de "chien" par "chat"
3. **xargs** — Liste tous les `.txt` du dossier courant et supprime-les avec xargs
4. **Combo** — Trouve tous les fichiers `.conf` modifiés aujourd'hui et affiche leur nom

---

**Résumé** : grep pour chercher, sed pour modifier, xargs pour enchaîner. Ensemble, ils couvrent 90% des tâches de traitement de texte en shell.
