# Leçon 67 : locate, which, whereis et type — Rechercher efficacement

### 1. locate — Recherche ultra-rapide par base de données

locate ne cherche pas directement sur le disque. Il utilise une base de données pré-construite, ce qui le rend extrêmement rapide. La base est mise à jour périodiquement (généralement via un cron).

### 2. which — Trouver la commande exécutée

which recherche l'emplacement d'une commande dans les répertoires du PATH. Idéal pour savoir quel exécutable sera utilisé.

### 3. whereis — Trouver binaire, source et manuel

whereis va plus loin que which : il localise le binaire, le code source et la page man d'une commande.

### 4. type — Identifier le type de commande

type est intégré au shell Bash. Il montre comment une commande sera interprétée : alias, fonction, builtin ou binaire externe.

### Points clés à retenir

locate utilise une base de données → très rapide, mais moins précis qu'un find en temps réel

which cherche dans le PATH → idéal pour les binaires exécutables

whereis donne binaire + manuel + sources → utile pour le développement

type est intégré au shell → révèle les alias, fonctions et builtins

Mise à jour de la base locate : sudo updatedb (ou via cron automatique)

