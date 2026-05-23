# Leçon 63 : tr — Transformez du texte facilement

### Syntaxe de base

tr ne lit pas de fichiers directement — il travaille sur l'entrée standard. Pour traiter un fichier, vous utiliserez donc un tube ou une redirection :

### Les classes de caractères

Au lieu de taper tous les caractères, tr reconnaît des classes prédéfinies très pratiques :

### Convertir majuscules et minuscules

C'est l'utilisation la plus courante de tr. Pour mettre tout en majuscules :

Résultat : BONJOUR LE MONDE

Pour mettre tout en minuscules, utilisez les classes pour plus de robustesse :

Résultat : bonjour le monde

### Supprimer des caractères

L'option -d (delete) supprime tous les caractères spécifiés de l'entrée :

Résultat : Mon mot de passe est Pass!

Résultat : texteavecespaces

### Compresser et squeeze

L'option -s (squeeze) remplace les occurrences répétées par une seule. Très utile pour compacter les espaces :

Résultat : texte avec beaucoup d'espaces

### Remplacer des caractères précis

Pour remplacer un caractère par un autre, donnez les deux ensembles dans le même ordre :

Résultat : nom-fichier-test

Résultat : B.n.j.r

### Transformer en colonnes (utiliser avec cut)

tr combine très bien avec cut (vu à la leçon 53) pour transformer du texte tabulé :

### Supprimer les retours chariot Windows (CRLF → LF)

Un problème très courant : les fichiers texte créés sous Windows finissent par \r\n au lieu de \n. tr résout ça en une commande :

### Compter les caractères ou lignes

tr peut servir à compter des éléments en combinant avec wc :

Résultat : 3

### Mode translate (sans -d ni -s)

Sans options, tr remplace chaque caractère de l'ensemble 1 par le caractère correspondant de l'ensemble 2 — c'est le mode "translate" classique :

Résultat : frperg zrfxfgr (ROT13)

### Combiner tr avec des groupes

Vous pouvez spécifier des plages de caractères directement avec les crochets :

Résultat : abc123def456

### Exercices pratiques

Transforme un fichier texte pour qu'il soit entièrement en majuscules : cat fichier.txt | tr '[:lower:]' '[:upper:]'

Supprime tous les espaces d'un texte : echo "un texte avec des espaces" | tr -d ' '

Remplace tous les tirets bas (_) par des points dans un nom de fichier.

Transforme un fichier CSV (séparateur ;) en TSV (séparateur tabulation).

Nettoie un fichier Windows en supprimant les retours chariot \r.

Compresse les espaces multiples en un seul espace : tr -s ' '

Utilise tr avec cut pour extraire une colonne et la convertir en majuscules.

Compte le nombre de caractères uniques différents dans un fichier : cat fichier.txt | tr -d '\n' | grep -o '.' | sort -u | wc -l

### Résumé

tr est un outil simple mais puissant pour manipuler du texte caractère par caractère. Combiné avec d'autres commandes via des pipes, il devient un allié précieux pour le nettoyage et la transformation de données.

