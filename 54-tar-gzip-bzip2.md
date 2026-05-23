# Leçon 54 : 61 - tar, gzip et bzip2 — Archiver et compresser

### 1. tar — assembler sans comprimer

tar ne compresse rien — il empile plusieurs fichiers et dossiers en un seul fichier appelé archive. Par convention, une archive tar à l'extension .tar.

### 2. gzip — compression rapide

gzip compresse un fichier pour réduire sa taille. Le fichier original est remplacé par un fichier .gz. La compression est rapide mais moins efficace que bzip2.

### 3. bzip2 — meilleure compression

bzip2 compresse mieux que gzip mais prend plus de temps. Idéal pour les fichiers volumineux où chaque mégabyte compte.

### 4. Combiner tar + compression

La vraie puissance vient de la combinaison. Tu peux créer une archive tar compressée en une seule commande.

### Résumé

Ces outils forment le socle de toute gestion de fichiers compressés sur Linux. Pratique chaque format jusqu'à connaître instinctively lequel utiliser selon le contexte — sauvegarde rapide, partage multiplateforme, ou archivage à long terme.

