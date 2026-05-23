# Leçon 57 : Leçon 68 : tee — Lire depuis l'entrée et écrire partout

### 1. Comment fonctionne tee ?

Imaginons un té (T) de plomberie : l'eau arrive d'un côté, se divise en deux directions. tee fait pareil avec les données : elles arrivent du pipe, et une copie part vers le fichier pendant que l'autre continue son chemin.

Le contenu est écrit dans fichier.txt ET passe à commande2.

### 2. Utilisation de base

Ce comando écrit "Bonjour le monde" dans salut.txt ET le compte avec wc -c.

### 3. Ajouter à un fichier existant

Par défaut, tee écrase le fichier. Avec -a, il ajoute à la fin :

### 4. Utilisation avec les droits administrateur

tee est très utile quand vous devez écrire dans un fichier root avec sudo :

Cette technique est plus propre que sudo sh -c 'echo ... >> fichier'.

### 5. tee avec plusieurs fichiers

tee peut envoyer le contenu vers plusieurs fichiers simultanément :

### 10. Exercices pratiques

Créez un fichier liste.txt contenant le résultat de ls -R ~ tout en l'affichant à l'écran.

Utilisez tee -a pour ajouter plusieurs lignes de texte à un même fichier.

Sauvegardez la sortie d'une commande ps filtrée avec grep, puis utilisez tee pour la sauvegarder ET l'afficher.

Créez un script qui utilise tee pour logger les étapes d'une installation dans un fichier.

### Conclusion

tee est une commande simple mais puissante. Elle permet de dupliquer un flux de données sans interrompre le pipe, ce qui est idéal pour le débogage, la sauvegarde de résultats intermédiaires, ou l'écriture dans des fichiers protégés. Associé à sudo, il devient un outil indispensable pour administrer un système Linux.

