# Leçon 51 : Leçon 53 : cut — Extraire des colonnes de texte

### Introduction

La commande cut permet d'extraire des colonnes ou des portions de texte depuis un fichier ou une entrée standard. C'est l'outil idéal pour manipuler des données structurées par délimiteur (CSV, fichiers de logs, /etc/passwd, etc.).

### Exemples concrets

Imaginons un fichier users.txt avec le format nom:email:ville :

Pour extraire uniquement les noms (1er champ) :

Pour obtenir nom et email (champs 1 et 2) :

Du champ 2 jusqu'à la fin :

Extraire les 5 premiers caractères de chaque ligne :

Le fichier /etc/passwd utilise : comme délimiteur. Pour extraire uniquement les noms d'utilisateur :

Pour obtenir uniquement les répertoires personnels (champ 6) :

Combiner cut avec d'autres commandes :

cut peut lire depuis un tube sans fichier :

### Cas pratiques

Cette commande extrait la première colonne (IP), compte les occurrences et trie par fréquence.

Pour afficher tout SAUF les champs 2 et 3 :

### Combiner avec d'autres outils

cut s'intègre parfaitement dans des pipelines pour manipuler du texte structuré :

cat fichier.csv | cut -d',' -f2 | sort | uniq — Extrait une colonne, trie et dédoublonne

ps aux | cut -d' ' -f1,11 | grep utilisateur — Extrait colonnes et filtre

cut -d':' -f1,5 /etc/passwd | head -10 — Affiche utilisateurs et shells

