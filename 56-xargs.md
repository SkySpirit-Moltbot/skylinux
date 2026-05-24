# Leçon 56 : xargs — Construire des commandes à partir de résultats

`xargs` transforme des lignes de texte en arguments pour une autre commande. C'est le chaînon manquant entre `find` et `rm`, entre `ls` et `wc`.

## 1. Le problème que xargs résout

```bash
# ❌ Ne fonctionne pas : rm attend des arguments, pas du stdin
find . -name "*.tmp" | rm

# ✅ xargs fait le pont
find . -name "*.tmp" | xargs rm
```

## 2. Syntaxe de base

```bash
commande_source | xargs commande_cible

# Exemple : supprimer tous les .log
find /var/log -name "*.log" -type f | xargs rm -v
# -v pour voir ce qui est supprimé
```

## 3. Options essentielles

```bash
# -n : combien d'arguments par commande
echo "a b c d e f" | xargs -n 2
# → a b
# → c d
# → e f

# -I : remplacer par chaque élément
ls *.jpg | xargs -I {} convert {} -resize 50% small/{}
# {} est remplacé par chaque nom de fichier

# -t : afficher la commande exécutée (debug)
ls *.tmp | xargs -t rm
# → rm fichier1.tmp fichier2.tmp

# -p : demander confirmation avant chaque commande
find . -name "*.bak" | xargs -p rm

# -0 : gérer les noms avec espaces (indispensable !)
find . -name "*.log" -print0 | xargs -0 rm
```

## 4. Cas pratiques

```bash
# Compter les lignes de tous les fichiers .py
find . -name "*.py" | xargs wc -l

# Chercher un motif dans tous les .conf
find /etc -name "*.conf" -type f | xargs grep "Listen"

# Créer plusieurs dossiers d'un coup
echo "projet1 projet2 projet3" | xargs -n 1 mkdir

# Redémarrer tous les conteneurs Docker
docker ps -q | xargs docker restart

# Archiver les fichiers modifiés depuis 7 jours
find . -type f -mtime -7 | xargs tar czf recent.tar.gz
```

## 5. Parallélisme avec -P

```bash
# Convertir 100 images en parallèle (4 processus simultanés)
find . -name "*.jpg" | xargs -P 4 -I {} convert {} -resize 50% converted/{}

# -P 0 = autant de processus que de cœurs
```

## 6. Exercices pratiques

1. **Suppression** — Supprime tous les `.tmp` d'un dossier avec find + xargs
2. **Comptage** — Compte les lignes de tous les `.sh` du dossier courant avec xargs wc -l
3. **Recherche** — Cherche le mot "localhost" dans tous les `.conf` de `/etc` avec find + xargs grep
