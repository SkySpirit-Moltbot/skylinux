# Leçon 52 : Leçon 54 : df et du — Gérer l'espace disque

### Introduction

Deux commandes essentielles pour surveiller l'utilisation de l'espace disque sous Linux : df (disk free) affiche l'espace disponible sur les systèmes de fichiers, tandis que du (disk usage) montre l'espace consommé par les fichiers et répertoires.

### du — Espace utilisé

Les tailles sont en blocs de 1 Ko par défaut.

### Alias utiles à connaître

Ajoute ces alias dans ton ~/.bashrc pour aller plus vite :

Puis recharge : source ~/.bashrc

### Exercices pratiques

État du disque — Exécute df -h et identifie le disque principal ainsi que son pourcentage d'utilisation.

Espace home — Affiche la taille totale de ton répertoire /home avec du -sh.

Top 10 — Trouve les 10 plus gros répertoires de /var avec tri par taille.

Gros fichiers — Utilise find pour lister les fichiers de plus de 50 Mo sur ta machine.

Exploration — Descends dans l'arborescence pour identifier ce qui consomme le plus d'espace chez toi.

