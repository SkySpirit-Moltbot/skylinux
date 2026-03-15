# Leçon 10 : Variables d'environnement et scripts Bash

Dans cette leçon, tu vas maîtriser les variables d'environnement et créer tes premiers scripts Bash pour automatiser des tâches.

---

## 1. Variables d'environnement

### Qu'est-ce qu'une variable d'environnement ?

Une variable d'environnement est une paire **nom=valeur** que le système et les programmes utilisent pour configurer leur comportement. Elles sont héritées par tous les processus enfants.

### Commandes de base

```bash
# Lister toutes les variables
env
printenv

# Voir une variable spécifique
echo $HOME
echo $PATH
echo $USER

# Définir une variable (session actuelle)
MA_VARIABLE="Bonjour"
echo $MA_VARIABLE

# Exporter une variable (pour les sous-processus)
export MA_VARIABLE
# ou
export MA_VARIABLE="Bonjour"
```

### Portée des variables

```bash
# Variable locale (processus courant uniquement)
MA_VAR="valeur"

# Variable exportée (héritée par les enfants)
export MA_VAR="valeur"

# Variable persistante (à ajouter dans ~/.bashrc ou ~/.profile)
echo 'export MA_VAR="valeur"' >> ~/.bashrc
source ~/.bashrc  # Recharger
```

---

## 2. Variables système importantes

| Variable | Description | Exemple |
|----------|-------------|---------|
| `$HOME` | Répertoire personnel | `/home/david` |
| `$USER` | Nom d'utilisateur | `david` |
| `$PATH` | Chemins des commandes | `/usr/local/bin:/usr/bin` |
| `$PWD` | Répertoire courant | `/home/david` |
| `$SHELL` | Shell par défaut | `/bin/bash` |
| `$LANG` | Langue | `fr_CH.UTF-8` |
| `$TERM` | Type de terminal | `xterm-256color` |
| `$HOSTNAME` | Nom de la machine | `raspberrypi` |
| `$DISPLAY` | Écran X11 | `:0` |
| `$EDITOR` | Éditeur par défaut | `nano` |

### Modifier le PATH

```bash
# Ajouter un répertoire au PATH
export PATH=$PATH:/nouveau/chemin

# PATH temporaire
export PATH="/home/david/scripts:$PATH"

# PATH permanent (ajouter à ~/.bashrc)
echo 'export PATH="$PATH:/home/david/scripts"' >> ~/.bashrc
```

---

## 3. Introduction aux scripts Bash

### Créer un script

```bash
nano mon_script.sh
```

### Structure de base

```bash
#!/bin/bash
# Commentaire : ce script fait quelque chose

echo "Hello World !"
```

### Rendre exécutable

```bash
chmod +x mon_script.sh
./mon_script.sh
```

> ⚠️ **Important** : Le shebang `#!/bin/bash` indique quel interpréteur utiliser.

---

## 4. Variables dans les scripts

### Variables utilisateur

```bash
#!/bin/bash

NOM="David"
echo "Bonjour $NOM !"

# Avec read
echo -n "Ton prénom: "
read prenom
echo "Salut $prenom !"

#read avec prompt
read -p "Ton âge: " age
echo "Tu as $age ans"
```

### Variables spéciales

| Variable | Description |
|----------|-------------|
| `$0` | Nom du script |
| `$1`, `$2`, ... | Arguments positionnels |
| `$#` | Nombre d'arguments |
| `$@` | Tous les arguments |
| `$?` | Code de retour de la dernière commande |
| `$$` | PID du script |
| `$!` | PID du dernier processus en arrière-plan |

### Exemple avec arguments

```bash
#!/bin/bash

echo "Script: $0"
echo "Premier argument: $1"
echo "Deuxième argument: $2"
echo "Nombre d'arguments: $#"
echo "Tous les arguments: $@"
```

---

## 5. Conditions (if/else)

### Syntaxe

```bash
if [ condition ]; then
    # commandes
elif [ condition ]; then
    # commandes
else
    # commandes
fi
```

### Comparaisons de nombres

```bash
if [ $a -eq $b ]; then    # Égal
if [ $a -ne $b ]; then    # Différent
if [ $a -gt $b ]; then    # Plus grand
if [ $a -ge $b ]; then    # Plus grand ou égal
if [ $a -lt $b ]; then    # Plus petit
if [ $a -le $b ]; then    # Plus petit ou égal
```

### Comparaisons de chaînes

```bash
if [ "$a" = "$b" ]; then    # Égal
if [ "$a" != "$b" ]; then   # Différent
if [ -z "$a" ]; then       # Vide
if [ -n "$a" ]; then       # Non vide
```

### Tests sur fichiers

```bash
if [ -f "$fichier" ]; then    # Fichier régulier
if [ -d "$dossier" ]; then   # Répertoire
if [ -e "$fichier" ]; then   # Existe
if [ -r "$fichier" ]; then   # Lisible
if [ -w "$fichier" ]; then   # Écriture
if [ -x "$fichier" ]; then   # Exécutable
if [ -s "$fichier" ]; then   # Non vide
```

### Exemple complet

```bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <nom>"
    exit 1
fi

NOM=$1

if [ -f "$NOM.txt" ]; then
    echo "Le fichier $NOM.txt existe"
else
    echo "Le fichier $NOM.txt n'existe pas"
    echo "Je le crée..."
    touch "$NOM.txt"
fi
```

---

## 6. Boucles

### Boucle for classique

```bash
for i in 1 2 3 4 5; do
    echo "Compteur: $i"
done

# Parcourir un dossier
for fichier in *.txt; do
    echo "Fichier: $fichier"
done

# Suite numérique
for i in {1..10}; do
    echo $i
done
```

### Boucle for C-style

```bash
for ((i=0; i<10; i++)); do
    echo "i = $i"
done
```

### Boucle while

```bash
compteur=1
while [ $compteur -le 5 ]; do
    echo "Compteur: $compteur"
    compteur=$((compteur + 1))
done
```

### Boucle until

```bash
compteur=1
until [ $compteur -gt 5 ]; do
    echo "Compteur: $compteur"
    compteur=$((compteur + 1))
done
```

---

## 7. Case (switch)

```bash
#!/bin/bash

echo "Choisis une option: "
read option

case $option in
    1)
        echo "Tu as choisi 1"
        ;;
    2)
        echo "Tu as choisi 2"
        ;;
    3)
        echo "Tu as choisi 3"
        ;;
    *)
        echo "Choix invalide"
        ;;
esac
```

---

## 8. Fonctions

### Définir une fonction

```bash
# Fonction sans paramètre
dire_bonjour() {
    echo "Bonjour !"
}

# Appeler
dire_bonjour
```

### Fonction avec paramètres

```bash
dire_bonjour_a() {
    echo "Bonjour $1 !"  # $1 = premier argument
}

dire_bonjour_a "David"
```

### Fonction avec retour

```bash
additionner() {
    resultat=$(($1 + $2))
    echo $resultat
}

somme=$(additionner 5 3)
echo "5 + 3 = $somme"
```

---

## 9. Tableaux

### Déclaration

```bash
# Tableau simple
tableau=(valeur1 valeur2 valeur3)

# Tableau avec indices
tableau[0]="premier"
tableau[1]="deuxième"
```

### Accéder aux éléments

```bash
echo ${tableau[0]}      # Premier élément
echo ${tableau[@]}      # Tous les éléments
echo ${#tableau[@]}     # Nombre d'éléments
```

### Parcourir un tableau

```bash
for element in "${tableau[@]}"; do
    echo $element
done
```

---

## 10. Exercices pratiques

### Exercice 1 : Script de backup
```bash
#!/bin/bash
# Backup automatique

DEST="$HOME/backup_$(date +%Y%m%d)"
mkdir -p $DEST
cp -r ~/Documents/* $DEST/
echo "Backup créé dans $DEST"
```

### Exercice 2 : Vérification système
```bash
#!/bin/bash

echo "=== État du système ==="
echo "Uptime: $(uptime)"
echo "Mémoire: $(free -h | grep Mem)"
echo "Disque: $(df -h / | tail -1)"
```

### Exercice 3 : Menu interactif
```bash
#!/bin/bash

echo "1. Afficher la date"
echo "2. Afficher qui est connecté"
echo "3. Afficher l'espace disque"

read -p "Choix: " choix

case $choix in
    1) date ;;
    2) who ;;
    3) df -h ;;
    *) echo "Choix invalide" ;;
esac
```

---

## 11. Trucs et Astuces

```bash
# Debug un script
bash -x script.sh

# Ignorer les erreurs
commande || true

# Valeur par défaut
echo ${VAR:-"défaut"}

# Assigner si vide
echo ${VAR:="défaut"}

# Opérations mathématiques
result=$((5 + 3))    # Addition
result=$((10 / 2))  # Division
result=$((10 % 3))  # Modulo
```

---

## 12. Résumé

| Concept | Commande/Syntaxe |
|---------|------------------|
| Variable | `VAR="valeur"` |
| Accéder | `$VAR` |
| Exporter | `export VAR` |
| Condition | `if [ $a -eq $b ]; then ... fi` |
| Boucle for | `for i in 1 2 3; do ... done` |
| Boucle while | `while [ condition ]; do ... done` |
| Fonction | `nom() { ... }` |
| Argument | `$1`, `$2`, `$@` |

---

Maîtrise ces bases et tu pourras créer des scripts puissants pour automatiser tes tâches Linux ! 🚀