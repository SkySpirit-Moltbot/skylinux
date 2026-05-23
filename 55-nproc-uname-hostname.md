# Leçon 55 : nproc, uname et hostname — Identifier le système

### nproc — Nombre de processeurs

nproc affiche le nombre d'unités de traitement disponibles. Très utile pour optimiser les performances ou comprendre les capacités de votre serveur.

Déterminer le nombre de jobs parallèles pour make -j

Configurer des conteneurs Docker avec --cpus

Évaluer les performances d'un serveur

### uname — Informations sur le noyau

uname affiche des informations détaillées sur le système d'exploitation et le noyau Linux.

### hostname — Nom de la machine

hostname gère le nom d'hôte de votre machine. Il existe trois types de noms :

Nom statique — défini dans /etc/hostname, persiste au redémarrage

Nom transitoire — modifié en mémoire, perdu au reboot

Nom "pretty" — nom lisible pour l'affichage (ex: "PC de David")

### Exercices pratiques

Informations de base — Exécute uname -a et identifie chaque champ.

Nom d'hôte — Affiche ton nom de machine, puis le domaine avec hostname -d.

Script diagnostic — Écris un script qui affiche le nombre de cœurs et l'architecture CPU.

Planification — Utilise nproc pour déterminer le nombre optimal de jobs de compilation.

