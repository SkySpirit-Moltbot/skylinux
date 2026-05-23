# Leçon 56 : Leçon 67 : xargs — Construire des commandes à partir de résultats

### 1. Comment fonctionne xargs ?

xargs lit des données depuis l'entrée standard (stdin), puis les utilise comme arguments pour exécuter une commande. Sans argument, il exécute echo par défaut.

### 2. Exemples pratiques

Trouver et supprimer des fichiers spécifiques avec find :

Ici, xargs prend chaque résultat de find et le passe comme argument à rm.

Par défaut, xargs utilise les espaces et sauts de ligne comme délimiteurs. Vous pouvez spécifier un autre délimiteur avec -d :

Par défaut, xargs passe autant d'arguments que possible sur une seule ligne. Utilisez -n pour limiter :

### 3. Utilisation avec des espaces et caractères spéciaux

Si un nom de fichier contient des espaces, xargs peut mal l'interpréter. La solution est d'utiliser find -print0 et xargs -0 :

Par défaut, les arguments sont ajoutés à la fin de la commande. Utilisez -I pour spécifier où insérer les arguments :

Le symbole {} est remplacé par chaque argument lu.

### 5. Utilisation avancée

Utilisez -p pour afficher la commande et demander confirmation :

Utilisez -t pour afficher les commandes exécutées (mode verbose) :

Utilisez -s pour limiter la longueur totale de la ligne de commande :

### 8. Exercices pratiques

Trouvez tous les fichiers .log de votre répertoire personnel et affichez leur taille avec ls -lh en utilisant xargs.

Créez une commande qui utilise find et xargs pour compter le nombre de lignes dans tous les fichiers .txt d'un répertoire.

Utilisez xargs -I pour copier chaque fichier d'un répertoire vers un autre.

Expérimentez avec xargs -p pour voir comment fonctionne la confirmation interactive.

### Conclusion

xargs est un outil essentiel pour tout administrateur Linux. Il permet de chaîner des commandes de manière flexible et puissante, transformant les résultats d'une commande en arguments pour une autre. Combiné avec find et les Pipes, il devient un outil de manipulation de fichiers très puissant.

