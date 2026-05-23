# Leçon 65 : head et tail — Visualiser le début et la fin des fichiers

### 📖 head — Afficher le début d'un fichier

La commande head affiche par défaut les 10 premières lignes d'un fichier. C'est très pratique pour prévisualiser un fichier sans charger l'intégralité de son contenu.

Cet exemple affiche les 10 premières lignes de fichier.txt.

Pour afficher les 20 premières lignes, on utilise l'option -n suivie du nombre souhaité. On peut aussi écrire simplement head -20 fichier.txt.

head peut traiter plusieurs fichiers à la fois. Il affichera alors un en-tête avec le nom du fichier avant chaque section.

Comme beaucoup de commandes Linux, head fonctionne parfaitement avec les pipes. Ici, on affiche les 50 premières lignes du résultat de cat.

### 📖 tail — Afficher la fin d'un fichier

La commande tail fait l'inverse de head : elle affiche les dernières lignes d'un fichier. C'est l'outil idéal pour consulter les logs en temps réel ou voir les dernières entrées d'un fichier.

Par défaut, tail affiche les 10 dernières lignes de fichier.txt.

Pour voir les 30 dernières lignes, utilisez l'option -n 30 ou simplement -30.

L'option -f (follow) est particulièrement utile pour monitorer les logs. Le terminal continuera à afficher les nouvelles lignes au fur et à mesure qu'elles sont ajoutées au fichier. Pour arrêter, appuyez sur Ctrl+C.

On peut surveiller plusieurs fichiers simultanément. Les nouvelles lignes de chaque fichier seront affichées avec un en-tête identifiant la source.

Avec +100, tail affichera tout à partir de la ligne 100 jusqu'à la fin du fichier.

### 🔧 Options avancées

Pour afficher les premiers 500 octets au lieu des premières lignes, utilisez -c. Cela peut être utile pour les fichiers binaires ou les fichiers avec des lignes très longues.

L'option -s permet de spécifier un intervalle en secondes entre chaque vérification. Ici, le fichier sera vérifié toutes les 5 secondes au lieu de lvaleur par défaut (1 seconde).

Pour afficher les lignes 81 à 100, on peut combiner les deux commandes avec un pipe. Ici, head garde les 100 premières lignes, puis tail en extrait les 20 dernières (donc les lignes 81 à 100).

### 💡 Cas d'utilisation courants

Permet de voir rapidement les 50 dernières erreurs dans un log serveur.

Utile pour surveiller les tentatives de connexion sur un serveur Linux.

Permet de vérifier rapidement la structure d'un fichier CSV avant de le traiter.

En combinant tail -f avec grep, on peut filtrer en temps réel pour ne voir que les lignes contenant "ERROR".

Pour obtenir l'avant-dernière ligne, on affiche les 2 dernières puis on garde la première avec head.

### 📝 Exercices pratiques

Essayez d'afficher les 5 premières lignes de votre fichier /etc/passwd. Vous verrez la liste des utilisateurs système.

Affichez les 20 dernières lignes du fichier /var/log/syslog (ou /var/log/messages sur certaines distributions).

Ouvrez un second terminal et lancez la commande suivante pour suivre un log en temps réel :

Revenez à votre premier terminal et tapez une commande (par exemple ls). Vous verrez les nouvelles entrées apparaître dans le second terminal.

Comment afficher les lignes 50 à 75 d'un fichier ?

### 🔗 Commandes liées

cat — Afficher l'intégralité d'un fichier (voir Leçon 2)

less — Afficher un fichier page par page

grep — Rechercher du texte dans un fichier (voir Leçon 50)

wc — Compter les lignes, mots et caractères (voir Leçon 65)

### 📚 Pour aller plus loin

Les commandes head et tail font partie des outils essentiels sous Linux. Leur simplicité cache une grande puissance, surtout quand on les combine avec des pipes et d'autres commandes comme grep ou awk. N'hésitez pas à les intégrer dans vos scripts pour analyser des logs ou extraire des données spécifiques.

Remember: pour les fichiers très volumineux, head et tail sont beaucoup plus rapides que d'ouvrir le fichier entièrement, car ils ne lisent que les parties nécessaires du fichier.

