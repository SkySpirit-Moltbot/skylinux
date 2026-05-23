# Leçon 50 : Leçon 52 : rsync — Synchronisation de fichiers

### Objectif

Maîtriser rsync pour synchroniser efficacement des fichiers et répertoires en local ou à distance. C'est l'outil de référence pour les sauvegardes et la copie incrémentale.

### Pourquoi rsync ?

Ne copie que les fichiers modifiés (transfert incrémental)

Much faster than cp pour les gros transferts

Compression intégrée pour réduire la bande passante

Supporte SSH pour des transferts sécurisés

Peut reprendre un transfert interrompu

### Les slashs comptent !

Attention à la présence ou l'absence du / final :

### Bonnes pratiques

Toujours faire un dry-run (-n) avant une première synchro

Utiliser -P pour les gros transferts (reprise si coupure)

Protéger les transferts distants avec SSH

Utiliser --delete avec prudence en mode miroir

### Exercices pratiques

Copie locale — Synchronise ton dossier ~/Documents vers /tmp/backup-documents/ en mode verbeux.

Simulation — Utilise -n pour voir ce qui serait copié sans rien modifier.

Exclusion — Synchronise un dossier en excluant tous les fichiers .log et le dossier .git.

Sauvegarde distante — Si tu as accès SSH à une machine, synchronise un petit dossier via SSH.

