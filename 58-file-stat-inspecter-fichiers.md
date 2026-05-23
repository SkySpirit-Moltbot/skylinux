# Leçon 58 : Leçon 69 : file et stat — Inspecter les fichiers

### 1. La commande file — Déterminer le type de fichier

file analyze le contenu d'un fichier (pas juste l'extension) et vous dit ce qu'il contient vraiment.

### 2. La commande stat — Métadonnées détaillées

stat affiche des informations complètes sur un fichier : taille, dates, permissions, inode, etc.

### Exercice pratique

Essayez ces commandes sur votre système :

file /bin/ls — Quel type de fichier est l'exécutable ls ?

file /etc/hostname — Vérifiez le type du fichier hostname

stat ~/.bashrc — Quelles sont les permissions de votre fichier bashrc ?

file -i ~/Documents/* — Listez les types MIME de tous vos documents

stat -c '%a %n' /etc/passwd — Affichez les permissions en octal du fichier passwd

### Résumé

Ces deux commandes sont vos meilleures alliées pour inspecter n'importe quel fichier sous Linux. file vous dit "ce que contient le fichier", tandis que stat vous dit "tout ce qu'il faut savoir sur ce fichier".

