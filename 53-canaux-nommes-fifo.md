# Leçon 53 : Leçon 60 : Canaux nommés (Named Pipes / FIFO)

### Qu'est-ce qu'un canal nommé ?

Un canal nommé (named pipe ou FIFO) est un fichier spécial de type p. Contrairement à un pipe anonyme (|) qui n'existe que pendant l'exécution d'un processus, le FIFO existe dans le système de fichiers et peut être utilisé par n'importe quel processus, à n'importe quel moment.

Communication entre processus qui ne sont pas liés par un pipe classique

Un processus écrit, un autre lit, à des moments différents

Débogage : rediriger la sortie d'un programme vers un fichier lisible à distance

Logs en temps réel consultables par plusieurs outils simultanément

Architecture simple sans réseau ni sockets TCP

### Créer et utiliser un canal nommé

Ouvre deux terminaux. Dans le premier :

Dans le second :

Le message apparaît dans le terminal 1. Chaque nouveau message envoyé depuis le terminal 2 sera affiché dans le terminal 1.

### Comportement de lecture et écriture

Les opérations de lecture et d'écriture sur un FIFO sont bloquantes par défaut. Cela signifie :

Un read bloque jusqu'à ce que des données soient disponibles

Un write bloque jusqu'à ce que les données soient lues

C'est ce comportement qui permet de synchroniser deux processus

Si tu veux qu'un processus lise et écrive sur le même FIFO, ouvre-le dans les deux directions :

### Bonnes pratiques

Toujours supprimer les FIFO quand tu n'en as plus besoin : rm ~/mon-fifo

Utiliser des noms explicites : /tmp/serveur-cmds, /tmp/logs-app

Placer les FIFO dans /tmp ou ton dossier personnel (pas dans /dev)

Penser à la gestion du bloquage : utilise timeout si ton lecteur doit mourir proprement

En bash, utiliser while IFS= read -r ligne &lt; "$FIFO" pour lire ligne par ligne

Ne jamais écrire dans un FIFO sans lecteur actif (le write bloquera indéfiniment)

Utiliser un fichier temporaire classique (file()) pour les gros volumes de données

### Résumé

Les canaux nommés sont un outil puissant pour la communication inter-processus sur Linux. Ils permettent de créer des architectures simples sans réseau ni configuration avancée. Maîtrise-les et tu disposeras d'un outil supplémentaire pour structurer tes scripts et automatisations.

