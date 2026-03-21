# Leçon 28 : Les variables d'environnement sous Linux

Dans cette leçon, tu vas découvrir les variables d'environnement sous Linux. Ce sont des valeurs dynamiques qui influencent le comportement du système et des applications. Les comprendre te permettra de configurer ton environnement, débugger des problèmes et écrire des scripts plus robustes.

---

## 1. Qu'est-ce qu'une variable d'environnement ?

Une **variable d'environnement** est une valeur clé/valeur qui influence le comportement des processus sur le système. Elles sont définies au niveau du système ou de l'utilisateur et sont accessibles par tous les programmes.

Quand tu ouvres un terminal, celui-ci inherits un ensemble de variables d'environnement qui définissent :
- Ton nom d'utilisateur (`USER`)
- Ton dossier personnel (`HOME`)
- Le chemin des exécutables (`PATH`)
- La langue du système (`LANG`)
- Et des centaines d'autres paramètres

```bash
# Voir toutes les variables d'environnement
printenv
```

Ce résultat peut être très long — il y a des dizaines de variables définies sur un système standard.

---

## 2. Afficher les variables

### printenv - Lister toutes les variables

```bash
printenv
```

Affiche la liste complète des variables d'environnement avec leurs valeurs.

```bash
HOME=/home/david
USER=david
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=fr_CH.UTF-8
SHELL=/bin/bash
TERM=xterm-256color
```

### echo - Afficher une variable précise

```bash
# Afficher le dossier personnel de l'utilisateur
echo $HOME

# Afficher le nom d'utilisateur
echo $USER

# Afficher le chemin des exécutables
echo $PATH

# Afficher le type de terminal
echo $TERM

# Afficher le shell par défaut
echo $SHELL
```

> 💡 Le signe `$` devant le nom de la variable indique à Bash qu'il faut lire la valeur de cette variable.

### env - Afficher et modifier l'environnement

```bash
# Afficher toutes les variables (identique à printenv)
env

# Lancer une commande avec un environnement vide
env -i /bin/bash
# Ici, aucune variable n'est héritée — environnement vide
```

---

## 3. Créer une variable temporaire

### Syntaxe de base

```bash
# Créer une variable (valable seulement dans le terminal actuel)
MA_VARIABLE="Bonjour le monde"

# L'afficher
echo $MA_VARIABLE
# Résultat : Bonjour le monde
```

> ⚠️ Par défaut, une variable créée ainsi est **temporaire**. Elle n'existe que dans le terminal où tu l'as créée. Ferme ce terminal et la variable disparaît.

### Règles de nommage

- Le nom ne peut contenir que des lettres, des chiffres et le tiret bas `_`
- Le nom ne peut pas commencer par un chiffre
- Les noms sont **sensibles à la casse** : `MA_VARIABLE` et `ma_variable` sont deux variables différentes

```bash
# Noms valides
MON_PROJET="Linux"
ma_variable=123
VAR_2="test"

# Noms invalides (donneraient une erreur)
# 2VARIABLE="test"     → ne peut pas commencer par un chiffre
# ma-variable="test"   → le tiret n'est pas autorisé
```

### export - Rendre une variable accessible aux sous-processus

```bash
# Créer une variable
MESSAGE="Configuration terminée"

# L'afficher dans le terminal actuel
echo $MESSAGE

# Lancer un script qui essaie d'afficher cette variable
bash -c 'echo $MESSAGE'
# → affiche "Configuration terminée" si la variable a été exportée
```

Par défaut, une variable n'est **pas transmise** aux programmes que tu lances. Pour ça, il faut l'exporter.

```bash
# Sans export — le sous-shell ne voit pas la variable
MA_VAR="secret"
bash -c 'echo $MA_VAR'
# → n'affiche rien

# Avec export — le sous-shell voit la variable
export MA_VAR="secret"
bash -c 'echo $MA_VAR'
# → affiche "secret"
```

---

## 4. Créer une variable permanente

Les variables temporaires disparaissent quand tu fermes le terminal. Pour les rendre permanentes, tu dois les enregistrer dans un fichier de configuration.

### ~/.bashrc - Configuration par utilisateur

Le fichier `~/.bashrc` est exécuté chaque fois que tu ouvres un nouveau terminal Bash. C'est l'endroit idéal pour définir tes variables personnelles.

```bash
# Éditer le fichier ~/.bashrc
nano ~/.bashrc

# Ajouter cette ligne à la fin du fichier
export MON_PROJET="/home/david/projets/linux"
export NOTES_DIR="$HOME/Notes"
export EDITOR="nano"
```

Après avoir ajouté ces lignes, recharge la configuration :

```bash
# Recharger ~/.bashrc sans fermer le terminal
source ~/.bashrc

# Ou utiliser la commande alternative
. ~/.bashrc
```

Vérifie que les variables sont bien définies :

```bash
echo $MON_PROJET
# → /home/david/projets/linux

echo $NOTES_DIR
# → /home/david/Notes

echo $EDITOR
# → nano
```

### /etc/environment - Variables système globales

Pour définir une variable accessible à **tous les utilisateurs** du système, utilise `/etc/environment`.

```bash
sudo nano /etc/environment
```

Ce fichier contient une variable par ligne, sans syntaxe shell :

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
HTTPS_PROXY="http://proxy.example.com:8080"
```

> ⚠️ Modifie ce fichier avec précaution. Une erreur peut perturber tout le système.

### /etc/profile.d/ - Scripts de démarrage système

Le dossier `/etc/profile.d/` contient des scripts qui sont exécutés lors de la connexion de chaque utilisateur. C'est une méthode propre pour ajouter des variables système.

```bash
# Créer un script pour ta variable
sudo nano /etc/profile.d/mes_variables.sh
```

```bash
#!/bin/bash
# Variables d'environnement personnalisées pour tous les utilisateurs

export MON_PROJET="/opt/mes-projets"
export DATA_DIR="/srv/data"
```

```bash
# Rendre le script exécutable
sudo chmod +x /etc/profile.d/mes_variables.sh
```

---

## 5. La variable PATH

La variable `PATH` est l'une des plus importantes. Elle indique à Linux où chercher les programmes quand tu tapes une commande.

### Comprendre le PATH

```bash
echo $PATH
# → /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Chaque répertoire est séparé par deux-points `:`. Quand tu tapes `ls`, le système cherche `ls` dans chacun de ces répertoires, dans l'ordre.

```bash
# Où se trouve la commande ls ?
which ls
# → /usr/bin/ls

# Où se trouve la commande python ?
which python3
# → /usr/bin/python3
```

### Ajouter un répertoire au PATH

Si tu installes un programme dans un dossier personnalisé, tu peux l'ajouter au PATH :

```bash
# Ajouter un dossier personnel au PATH (temporaire)
export PATH="$PATH:/home/david/mes-scripts"

# Vérifier
echo $PATH
# → /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/david/mes-scripts
```

Pour rendre cette modification permanente, ajoute la ligne dans `~/.bashrc` :

```bash
# À ajouter dans ~/.bashrc
export PATH="$PATH:/home/david/mes-scripts"
```

### PATH et sécurité

> ⚠️ **Attention** : ne mets jamais le répertoire courant `.` dans ton PATH de façon permanente. Quelqu'un pourrait créer un programme malveillant nommé `ls` dans ce répertoire et tu l'exécuterais involontairement.

```bash
# DANGEREUX — ne fais pas ça
export PATH=".:$PATH"

# Instead, lance les programmes du répertoire courant explicitement
./mon_script.sh
```

---

## 6. Les variables spéciales les plus utiles

| Variable | Description | Exemple |
|----------|-------------|---------|
| `$HOME` | Dossier personnel de l'utilisateur | `/home/david` |
| `$USER` | Nom de l'utilisateur | `david` |
| `$PATH` | Chemins des exécutables | `/usr/bin:/bin` |
| `$SHELL` | Shell par défaut | `/bin/bash` |
| `$LANG` | Langue et encodage | `fr_CH.UTF-8` |
| `$PWD` | Répertoire courant | `/home/david/Documents` |
| `$HOSTNAME` | Nom de la machine | `moltbot` |
| `$TERM` | Type de terminal | `xterm-256color` |
| `$?` | Code de retour de la dernière commande | `0` (succès) |
| `$$` | PID du processus courant | `12345` |
| `$!` | PID du dernier processus lancé en arrière-plan | `12346` |
| `$RANDOM` | Nombre aléatoire | `4823` |

### Exemples pratiques

```bash
# Afficher le dossier personnel
echo "Bienvenue, $USER !"
# → Bienvenue, david !

# Connaître le code de retour de la dernière commande
ls /etc
echo "Code de retour : $?"
# → Code de retour : 0 (tout va bien)

ls /etc/fichier-inexistant
echo "Code de retour : $?"
# → Code de retour : 2 (erreur — fichier non trouvé)

# Afficher un nombre aléatoire
echo $RANDOM

# Connaître son PID
echo "Mon PID est : $$"

# Construire un chemin
echo "Ton dossier personnel est : $HOME/Documents"
```

---

## 7. Modifier une variable existante

### Ajouter un élément à une variable

```bash
# Ajouter un chemin à PATH
export PATH="$PATH:/nouveau/chemin"

# Ajouter un élément à une variable PATH déjà existante
export PATH="/home/david/scripts:$PATH"
# → le nouveau chemin est vérifié en premier

# Ajouter à la fin
export PATH="$PATH:/home/david/scripts"
# → le nouveau chemin est vérifié en dernier
```

### Supprimer une variable

```bash
# Supprimer une variable (unexport)
unset MA_VARIABLE

# Vérifier qu'elle n'existe plus
echo $MA_VARIABLE
# → n'affiche rien
```

---

## 8. Scripts et variables d'environnement

Quand tu écris un script Bash, les variables d'environnement jouent un rôle essentiel.

### Hériter de l'environnement parent

Par défaut, un script Bash hérite des variables exportées du terminal qui le lance.

```bash
# Script : mon_script.sh
#!/bin/bash
echo "L'utilisateur est : $USER"
echo "Le HOME est : $HOME"
echo "Le PATH est : $PATH"
```

```bash
chmod +x mon_script.sh
./mon_script.sh
# → affiche les valeurs des variables héritées
```

### Isoler l'environnement dans un script

```bash
# Lancer un script dans un environnement propre
env -i ./mon_script.sh
# → aucune variable n'est héritée
```

### Exporter une variable depuis un script

```bash
#!/bin/bash
# Ce script définit une variable accessible après son exécution

export MA_CONFIG="valeur_configurée"
echo "Configuration chargée"
```

```bash
./script_config.sh
echo $MA_CONFIG
# → affiche "valeur_configurée" (accessible après l'exécution)
```

---

## 9. Variables d'environnement et sécurité

Les variables d'environnement peuvent contenir des informations sensibles. Voici les points importants à connaître.

### Variables potentiellement sensibles

```bash
# Ne jamais afficher ces variables sur un système partagé
echo $SSH_CONNECTION    # IP et ports de connexion SSH
env | grep -i pass      # Rechercher des mots de passe en mémoire
env | grep -i key       # Rechercher des clés API
```

### Variables et sudo

> ⚠️ Par défaut, `sudo` ne transmet pas les variables d'environnement pour des raisons de sécurité. Si tu as besoin d'une variable avec sudo, utilise l'option `-E`.

```bash
# Définir une variable
export MA_VAR="test"

# Avec sudo — la variable n'est pas transmise
sudo env | grep MA_VAR
# → n'affiche rien

# Avec sudo -E — la variable est transmise
sudo -E env | grep MA_VAR
# → affiche MA_VAR=test
```

### Fichier .bash_history et sécurité

```bash
# L'historique des commandes contient souvent des variables sensibles
# Configure ton shell pour ne pas enregistrer certaines commandes

# Dans ~/.bashrc, ajoute :
export HISTIGNORE="export *:set *"
# → les commandes "export ..." et "set ..." ne seront pas enregistrées dans l'historique
```

---

## 10. Exercices pratiques

### Exercice 1 : Découvrir ton environnement

1. Affiche toutes tes variables d'environnement :
```bash
printenv | less
```

2. Recherche ta variable HOME :
```bash
printenv HOME
```

3. Trouve où se trouve la commande `grep` :
```bash
which grep
```

4. Affiche ton type de terminal et ton shell :
```bash
echo "Terminal : $TERM | Shell : $SHELL"
```

✅ Tu connais maintenant ton environnement de base.

---

### Exercice 2 : Créer et exporter une variable

1. Crée une variable sans l'exporter :
```bash
MON_SECRET="mot_de_passe_123"
echo $MON_SECRET
```

2. Lance un sous-shell et vérifie si la variable est visible :
```bash
bash -c 'echo $MON_SECRET'
# → ne devrait rien afficher
```

3. Exporte la variable et refais le test :
```bash
export MON_SECRET="mot_de_passe_123"
bash -c 'echo $MON_SECRET'
# → cette fois, affiche "mot_de_passe_123"
```

4. Supprime la variable :
```bash
unset MON_SECRET
echo $MON_SECRET
# → n'affiche rien
```

✅ Tu sais créer, exporter et supprimer des variables.

---

### Exercice 3 : Variable permanente

1. Ouvre ton fichier `~/.bashrc` :
```bash
nano ~/.bashrc
```

2. Ajoute ces lignes à la fin :
```bash
# Mes variables personnelles
export PROJET_DIR="$HOME/projets"
export SCRIPTS_DIR="$HOME/scripts"
export EDITOR="nano"
```

3. Sauvegarde et ferme le fichier.

4. Recharge la configuration :
```bash
source ~/.bashrc
```

5. Vérifie que les variables existent :
```bash
echo "Projet : $PROJET_DIR"
echo "Scripts : $SCRIPTS_DIR"
echo "Éditeur : $EDITOR"
```

✅ Tes variables sont maintenant permanentes.

---

### Exercice 4 : Modifier le PATH

1. Affiche ton PATH actuel :
```bash
echo $PATH
```

2. Crée un dossier pour tes scripts personnels :
```bash
mkdir -p ~/mes-scripts
```

3. Crée un script de test dans ce dossier :
```bash
echo '#!/bin/bash' > ~/mes-scripts/salut.sh
echo 'echo "Salut depuis ~/mes-scripts !"' >> ~/mes-scripts/salut.sh
chmod +x ~/mes-scripts/salut.sh
```

4. Tente de lancer le script sans modifier le PATH :
```bash
salut.sh
# → commande non trouvée (normal — le dossier n'est pas dans PATH)
```

5. Ajoute le dossier au PATH :
```bash
export PATH="$PATH:$HOME/mes-scripts"
```

6. Lance le script :
```bash
salut.sh
# → affiche "Salut depuis ~/mes-scripts !"
```

7. Rends cette modification permanente (ajoute `export PATH=...` dans `~/.bashrc`).

✅ Tu peux maintenant exécuter tes propres scripts depuis n'importe où.

---

## 11. Résumé

| Commande | Description |
|----------|-------------|
| `printenv` | Lister toutes les variables d'environnement |
| `printenv VAR` | Afficher la valeur d'une variable précise |
| `env` | Afficher l'environnement (identique à printenv) |
| `echo $VAR` | Afficher la valeur d'une variable |
| `export VAR=valeur` | Créer et exporter une variable |
| `export VAR="$VAR:ajout"` | Ajouter un élément à une variable existante |
| `unset VAR` | Supprimer une variable |
| `source ~/.bashrc` | Recharger la configuration Bash |
| `env -i bash` | Lancer un shell avec environnement vide |

- Une variable **sans export** n'est visible que dans le terminal actuel
- Une variable **exportée** est transmise aux sous-processus
- `~/.bashrc` → configuration **par utilisateur** (permanent)
- `/etc/profile.d/` → configuration **système** (tous les utilisateurs)
- `PATH` → indique où le système cherche les programmes
- `$HOME`, `$USER`, `$PATH`, `$SHELL` → variables spéciales les plus utilisées


