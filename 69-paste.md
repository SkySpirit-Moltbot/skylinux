# Leçon 69 : paste — Fusionner des lignes de fichiers

### Introduction

paste est une commande qui fusionne les lignes de plusieurs fichiers, en les plaçant côte à côte et en les séparant par des tabulations. Contrairement à cat qui affiche les fichiers bout à bout, paste les place en colonnes parallèles. C'est l'outil idéal pour combiner des données tabulaires ou créer des tableaux à partir de plusieurs sources.

### Points clés à retenir

paste fichier1 fichier2 → fusionne ligne par ligne avec tabulation

-d'séparateur' → change le délimiteur entre les colonnes

-s → place toutes les lignes sur une seule ligne

Idéal pour créer des tableaux CSV ou TSV

Combinez avec cut, awk, seq pour des usages avancés

paste = colonnes parallèles, join = fusion sur clé commune

