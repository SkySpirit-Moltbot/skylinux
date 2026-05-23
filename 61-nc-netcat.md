# Leçon 61 : nc — Netcat, le couteau suisse du réseau

### Introduction

nc (Netcat) est souvent qualifié de "couteau suisse du réseau". Il permet d'ouvrir des connexions TCP/UDP, d'écouter sur des ports, de transferred des données, et même de créer des tunnels rapides. C'est un outil indispensable pour le diagnostic réseau, le transfère de fichiers, et les tests de connectivité.

### Test de connectivité simple

La forme la plus élémentaire de nc : vérifier qu'un port est accessible sur un hôte distant.

Les flags -z désactivent la connexion sortante (mode scan) et -v active le mode verbose.

### Transfert de fichiers

nc permet de transfèrer des fichiers entre deux machines sans outil supplémentaire.

### Chat simple entre deux machines

Tout texte tapé d'un côté apparaît de l'autre côté. Pour quitter, Ctrl+C.

### Proxy simple avec nc

Rediriger le trafic d'un port vers un autre hôte/port.

### Commandes pour le remote shell (attention sécurité !)

nc permet aussi de créer un shell distant (equivaut à un reverse shell). À utiliser uniquement dans des environnements contrôlés et avec autorisation.

Note : toutes les versions de nc ne supportent pas le flag -e (c'est le cas d'openbsd-nc). Pour ces versions, utilisez un pipe :

### Version GNU vs OpenBSD

Il existe deux versions principales de nc :

OpenBSD netcat (installÃ© par defaut sur Ubuntu/Debian) — plus moderne, avec support de -c, -e, et autres options avancees.

GNU netcat — alternative plus ancienne, moins d'options disponibles.

### Bonnes pratiques

Utilisez nc en environnement lab ou avec autorisation pour les exercices reseau.

Pour les tunnels et shells distances en production, preferez SSH (lecon 44) qui offre le chiffrement.

Specifyz toujours un -w (timeout) pour eviter que les connexions restent ouvertes indefiniment.

Combinez nc avec tar, gzip, ou d'autres outils pour des transferts robustes.

### Résumé

nc -zv host port = tester la connectivite vers un port

nc -l -p port = ecouter sur un port

nc host port = se connecter en client

nc -l -p port > fichier + nc host port  = transfert de fichier

tar cf - | nc host port = transfert de repertoire

nc -l -p port -k = rester en ecoute apres deconnexion

-u = mode UDP, -w = timeout, -z = mode scan

