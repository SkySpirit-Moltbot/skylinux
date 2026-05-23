# Leçon 30 : Alias et raccourcis personnalisés

Dans cette leçon, tu vas découvrir comment créer tes propres raccourcis de commandes grâce aux alias. Tu verras comment gagner du temps au quotidien en créant des commandes personnalisées pour tes tâches fréquentes.

---

## 1. Qu'est-ce qu'un alias ?

Un **alias** est un raccourci qui remplace une commande longue ou complexe par un mot simple. C'est comme créer ta propre commande.

**Exemples concrets :**
- `ll` au lieu de `ls -la` (lister avec détails)
- `gs` au lieu de `git status`
- `update` au lieu de `sudo apt update && sudo apt upgrade -y`

Les alias rendent ton terminal plus rapide et plus agréable à utiliser.

---

## 2. Créer un alias temporaire

### Syntaxe de base

```bash
alias nom='commande'
```

Le `=` est sans espaces, et la commande est entre guillemets simples ou doubles.

### Exemples

```bash
# Raccourci pour lister les fichiers
alias ll='ls -la'

# Raccourci pour mettre à jour le système
alias update='sudo apt update && sudo apt upgrade -y'

# Raccourci pour Git status
alias gs='git status'

# Raccourci avec options
alias grep='grep --color=auto'
```

### Utiliser un alias

Après l'avoir créé, utilise-le comme une commande normale :

```bash
ll
# Équivalent à : ls -la
```

### Vérifier les alias actifs

```bash
# Voir un alias précis
type ll

# Lister tous les alias actifs
alias
```

Résultat de `alias` :
```
alias ll='ls -la'
alias gs='git status'
alias update='sudo apt update && sudo apt upgrade -y'
```

---

## 3. Alias temporaires vs permanents

### Session actuelle seulement

Les alias créés avec la commande `alias` sont **temporaires** : ils disparaissent quand tu fermes le terminal.

```bash
# Créé maintenant, fonctionne dans cette session
alias ll='ls -la'

# Après fermeture du terminal → disparu
```

### Rendre un alias permanent

Pour qu'un alias survive à la fermeture du terminal, ajoute-le dans un fichier de configuration :

**Pour Bash (le plus courant) :**
```bash
nano ~/.bashrc
```

**Pour Zsh :**
```bash
nano ~/.zshrc
```

Ajoute tes alias à la fin du fichier :

```bash
# Mes alias personnalisés
alias ll='ls -la'
alias gs='git status'
alias update='sudo apt update && sudo apt upgrade -y'
alias c='clear'
```

Sauvegarde puis recharge :

```bash
# Recharger sans redémarrer
source ~/.bashrc
```

---

## 4. Alias avec paramètres (fonctions)

Les alias simples ne permettent pas de paramètres. Pour ça, utilise les **fonctions** :

### Fonction simple

```bash
# Créer une fonction pour chercher un fichier
rechercher() {
    find . -name "$1" 2>/dev/null
}

# Utilisation
rechercher "*.txt"
```

### Fonction avec plusieurs paramètres

```bash
# Créer une fonction pour se connecter en SSH
connect() {
    ssh "$1@$2"
}

# Utilisation
connect user 192.168.1.10
```

### Fonction pour archivage rapide

```bash
# Créer une archive .tar.gz
archiver() {
    tar -czvf "$1.tar.gz" "$1"
}

# Utilisation
archiver mon-dossier
```

### Fonction pour extraer une archive

```bash
extraire() {
    if [ -f "$1" ]; then
        tar -xzvf "$1"
    else
        echo "Fichier non trouvé : $1"
    fi
}

# Utilisation
extraire archive.tar.gz
```

---

## 5. Surcharger une commande existante

Tu peux créer un alias qui remplace une commande système :

```bash
# Remplacer rm par rm -i (confirmation avant suppression)
alias rm='rm -i'

# Remplacer mv par mv -i (confirmation avant écrasement)
alias mv='mv -i'

# Remplacer cp par cp -i (confirmation avant écrasement)
alias cp='cp -i'
```

> ⚠️ Utilise ces alias de sécurité avec précaution. Sur un serveur où tu n'as pas l'habitude, `rm` pourrait ne pas avoir `-i` et une suppression serait définitive.

---

## 6. Alias pour l'historique

```bash
# Relancer la dernière commande
alias r='!!'

# Relancer la dernière commande sudo
alias s='sudo !!'

# Afficher l'historique
alias h='history'
```

---

## 7. Supprimer un alias

### Supprimer temporairement

```bash
# Supprimer un alias dans la session actuelle
unalias ll

# Supprimer tous les alias
unalias -a
```

### Cacher une commande (forcer l'original)

Si tu as un alias qui masque une commande, utilise `\`:

```bash
# Exécute la commande originale, pas l'alias
\rm fichier.txt
```

Le backslash `\ ` devant ignore les alias.

---

## 8. Exemples pratiques complets

### Configuration ~/.bashrc

```bash
nano ~/.bashrc
```

Ajoute cette section à la fin :

```bash
# ========================
# Mes alias personnalisés
# ========================

# Raccourcis système
alias c='clear'
alias h='history'
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'

# Sécurité - confirmation avant actions irréversibles
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'

# Git
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'

# Système
alias update='sudo apt update && sudo apt upgrade -y'
alias restart='sudo systemctl restart'
alias status='sudo systemctl status'

# Réseau
alias ip='ip -c'
alias ports='sudo netstat -tulpn'
alias ping='ping -c 5'

# ========================
# Mes fonctions personnalisées
# ========================

# Créer un dossier et y entrer
cdl() {
    mkdir -p "$1" && cd "$1"
}

# Extraire une archive
extraire() {
    tar -xzvf "$1"
}

# Archivage rapide
archiver() {
    tar -czvf "$1.tar.gz" "$1"
}

# Afficher la taille d'un dossier
taille() {
    du -sh "$1" 2>/dev/null || du -sh ./*
}
```

Recharge ta configuration :

```bash
source ~/.bashrc
```

---

## 9. Hiérarchie des fichiers de configuration Bash

```
/etc/profile          → Config globale pour tous les utilisateurs (lecture seule)
~/.bash_profile       → Config personnelle (exécuté à la connexion)
~/.bashrc             → Config personnelle (exécuté à chaque ouverture de terminal)
~/.bash_logout        → Commandes exécutées à la déconnexion
```

**L'ordre de chargement :**
1. `/etc/profile`
2. `~/.bash_profile` (s'il existe, sinon `~/.bash_login`, sinon `~/.profile`)
3. `~/.bashrc` (souvent chargé depuis `~/.bash_profile`)

---

## 10. Bonnes pratiques

- **Débute par une lettre ou un chiffre**, évite les noms de commandes existantes (`ls`, `cd`, etc.)
- **Utilise des noms mnémotechniques** : `gs` pour git status, `ll` pour ls -la
- **Groupe tes alias** dans `~/.bashrc` avec des commentaires
- **Teste avant de rendre permanent** : crée d'abord un alias temporaire
- **Sauvegarde ta config** : copie ton `~/.bashrc` régulièrement

---

## 11. Résumé des commandes

| Commande | Description |
|----------|-------------|
| `alias nom='cmd'` | Créer un alias temporaire |
| `alias` | Lister tous les alias |
| `unalias nom` | Supprimer un alias |
| `unalias -a` | Supprimer tous les alias |
| `type alias_name` | Voir si c'est un alias et sa définition |
| `\cmd` | Exécuter la commande originale (sans alias) |
| `source ~/.bashrc` | Recharger la configuration |

---

## 12. Exercice pratique

### Exercice : Crée ta boîte à outils

**Objectif** : Configure ton terminal avec tes premiers alias personnalisés.

**Étape 1 : Vérifie les alias existants**

```bash
alias
```

Note les alias par défaut de ton système.

**Étape 2 : Crée un alias simple**

```bash
alias ll='ls -la'
ll
```

**Étape 3 : Crée un alias avec couleur**

```bash
alias ls='ls --color=auto'
ls
```

**Étape 4 : Crée une fonction personnalisée**

```bash
maj() {
    echo "Mise à jour du système..."
    sudo apt update
    sudo apt upgrade -y
    echo "Terminé !"
}

# Teste
maj
```

**Étape 5 : Rends un alias permanent**

```bash
echo "alias c='clear'" >> ~/.bashrc
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc
```

**Étape 6 : Vérifie**

```bash
# Ferme et rouvre le terminal, puis teste
c
ll
```

**Étape 7 : Supprime un alias (test)**

```bash
unalias ll
type ll
# Devrait afficher "not found"
```

✅ Tu sais maintenant personnaliser ton terminal !

---

## 13. Aller plus loin

- **Alias entre machines** : copie ton `~/.bashrc` sur chaque machine via Git
- **Scripts de configuration** : crée un script qui installe ta config sur une nouvelle machine
- **Oh My Zsh** : framework pour Zsh avec des centaines d'alias prêts à l'emploi
- **Autocomplétion** : configure l'autocomplétion pour tes fonctions personnalisées

---

## Complément: Fonctions bash

### Les alias

Un alias est un raccourci qui remplace une commande ou une série de commandes. C'est la méthode la plus simple pour personnaliser votre terminal.

### Créer un alias

Maintenant, taper ll équivaut à taper ls -la.

Crée une commande update qui met à jour le système automatiquement.

Raccourci pour git status.

### Lister et supprimer les alias

Affiche tous les alias actuellement définis.

### Alias avec arguments (limites)

Les alias ne peuvent pas gérer d'arguments directement. Si vous écrivez :

Et que vous tapez gp main, le main sera appendu après la commande complète. Cela fonctionne dans ce cas, mais pour des cas plus complexes, mieux vaut utiliser une fonction.

### Les fonctions Bash

Les fonctions sont plus puissantes que les alias. Elles peuvent accepter des paramètres, utiliser des conditions, des boucles, et返回值.

### Syntaxe des fonctions

Ou avec le mot-clé function (optionnel) :

### Exemples concrets

Utilisation : backup monfichier.txt crée une copie备份 avec la date dans le nom.

Appel : taille_fichier document.pdf

### Fonctions avec valeur de retour (return)

Utilisation :

### Variables dans les fonctions

Le mot-clé local limite la variable à la fonction. Sans cela, la variable serait globale.

### Exemples pratiques

Utilisation : mkcd mon_projet

Utilisation : hc git cherche les commandes git dans l'historique.

### Rendre les alias et fonctions permanents

Par défaut, les alias et fonctions définis dans le terminal sont temporaires. Pour les rendre permanents, ajoutez-les dans un fichier de configuration.

Ajoutez vos alias et fonctions à la fin du fichier.

Ou plus court :

Sur certaines distributions, on peut créer un fichier séparé :

Puis créez ~/.bash_aliases avec vos alias et fonctions.

### Alias système (pour tous les utilisateurs)

Pour des alias visibles par tous les utilisateurs du système, ajoutez-les dans :

Ou dans /etc/profile.d/ pour une organisation plus propre.

### Debugging des fonctions

Pour déboguer une fonction, utilisez set -x :

Les commandes seront affichées avant leur exécution.

### Résumé

Les alias et fonctions transforment votre terminal en outil personnalisé :

alias nom='commande' — crée un raccourci simple

unalias nom — supprime un alias

nom_fonction() { ... } — crée une fonction complexe

Utilisez local pour les variables locales

Placez vos alias/fonctions dans ~/.bashrc pour les rendre permanents

Séparez dans ~/.bash_aliases pour une meilleure organisation
