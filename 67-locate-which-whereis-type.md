# Leçon 67 : locate, which, whereis et type — Rechercher efficacement

Quatre commandes pour trouver rapidement des fichiers et programmes sans parcourir tout le disque.

## 1. locate — Recherche éclair par nom

`locate` utilise une base de données pré-indexée. Ultra-rapide mais pas en temps réel.

```bash
# Installer si nécessaire
sudo apt install plocate

# Mettre à jour la base de données
sudo updatedb

# Chercher un fichier par nom
locate fstab
# → /etc/fstab
# → /usr/share/doc/mount/examples/fstab

# Ignorer la casse
locate -i README

# Limiter le nombre de résultats
locate -l 10 .conf

# Compter les résultats
locate -c .pdf
```

**Attention** : `locate` ne voit pas les fichiers créés depuis le dernier `updatedb`. Pour du temps réel, utilise `find`.

## 2. which — Où est cet exécutable ?

```bash
# Trouver le chemin d'une commande
which python3
# → /usr/bin/python3

which ls
# → /usr/bin/ls

# Afficher TOUS les emplacements (pas seulement le premier)
which -a python3
# → /usr/bin/python3
# → /usr/local/bin/python3
```

## 3. whereis — Localiser binaire, sources, manuel

```bash
whereis bash
# → bash: /usr/bin/bash /etc/bash.bashrc /usr/share/man/man1/bash.1.gz

# Seulement le binaire
whereis -b bash

# Seulement les pages de manuel
whereis -m bash
```

## 4. type — Comment le shell interprète cette commande ?

```bash
# Est-ce un binaire, un alias, une fonction ?
type ls
# → ls est un alias pour « ls --color=auto »

type -a ls
# → ls est un alias pour « ls --color=auto »
# → ls est /usr/bin/ls

type cd
# → cd est une primitive du shell

type -t pwd
# → builtin
```

Types possibles : `alias`, `keyword`, `function`, `builtin`, `file`

## 5. Comparaison

| Commande | Ce qu'elle trouve | Rapidité |
|----------|-------------------|----------|
| `locate` | Fichiers par nom (BD indexée) | ⚡ Immédiat |
| `which` | Exécutables dans le PATH | ⚡ Immédiat |
| `whereis` | Binaires, sources, man | ⚡ Immédiat |
| `type` | Comment le shell voit la commande | ⚡ Immédiat |
| `find` | Fichiers en temps réel | 🐢 Lent |

## 6. Exercices pratiques

1. **locate** — Trouve tous les `.conf` sur ton système avec `locate`
2. **which** — Trouve où sont installés `python3`, `node` et `gcc`
3. **type** — Découvre si `ls` est un alias, un binaire ou une fonction
4. **whereis** — Trouve le binaire et le manuel de `git`
