# Leçon 62 : curl et wget — Télécharger des fichiers depuis le terminal

### wget — Téléchargement simple et automatique

wget est idéal pour télécharger des fichiers de manière récursive ou en arrière-plan. Il reprend automatiquement un téléchargement interrompu et suit les redirections.

Le fichier sera téléchargé et sauvegardé sous le même nom fichier.tar.gz.

L'option -O permet de spécifier le nom du fichier de sortie.

Si le téléchargement est interrompu, -c reprend là où il s'est arrêté. Très utile pour les gros fichiers !

L'option -b lance le téléchargement en arrière-plan. Tu peux vérifier l'avancement avec :

Cette commande télécharge récursivement tout un site web pour consultation hors ligne.

### curl — Transfert de donnéespolyvalent

curl est plus puissant pour envoyer des données (POST, uploads) et pour visualiser les en-têtes HTTP. Il affiche aussi le résultat dans le terminal par défaut.

Le contenu HTML s'affiche directement dans le terminal (sans sauvegarder).

L'option -O (majuscule) sauvegarde le fichier sous son nom original.

L'option -o (minuscule) permet de choisir le nom de sortie.

L'option -L suit automatiquement les redirections HTTP.

L'option -u permet de s'authentifier avec un nom d'utilisateur et mot de passe.

-X POSTspécifier la méthode et -d envoie les données.

L'option -F envoie un formulaire multipart (utile pour les uploads de fichiers).

L'option -I affiche uniquement les en-têtes de la réponse.

L'option -H permet d'ajouter des en-têtes personnalisés.

### Utiliser curl avec une API JSON

Pour envoyer ou recevoir des données JSON :

### Téléchargement avec vitesse limitée

Pour ne pas saturer la bande passante :

La vitesse est limitée à 200 Ko/s dans ces exemples.

### Vérifier les liens brisés

Avec curl et un peu de script, tu peux vérifier si une liste de liens fonctionne :

Cela affiche le code HTTP de chaque lien dans liens.txt.

### Résumé des options principales

-O fichier : sauvegarder sous un nom différent

-c : reprendre un téléchargement interrompu

-b : lancer en arrière-plan

-q : mode silencieux (sans messages)

--limit-rate=X : limiter la vitesse de téléchargement

--mirror : dupliquer un site entier

-o fichier : sauvegarder sous un nom différent

-O : sauvegarder sous le nom original

-L : suivre les redirections

-I : afficher uniquement les en-têtes

-X POST : envoyer en méthode POST

-d "data" : envoyer des données

-F "fichier=@x" : upload de fichier

-H "En-tête" : ajouter un en-tête personnalisé

-u user:mdp : authentification

--limit-rate X : limiter la vitesse

### Exercices pratiques

Utilise wget pour télécharger un fichier depuis une URL de ton choix.

Utilise curl pour afficher le contenu HTML d'une page web.

Télécharge un fichier archive et décompresse-le en une seule ligne avec pipe.

Utilise curl -I pour voir les en-têtes HTTP d'un site.

Essaie de télécharger un fichier avec wget -c et interrompt-le avec Ctrl+C, puis reprends-le avec la même commande.

