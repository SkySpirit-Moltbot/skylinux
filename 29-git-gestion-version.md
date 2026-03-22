# Leçon 29 : Git - Gestion de version

Dans cette leçon, tu vas découvrir Git, l'outil de gestion de version le plus utilisé au monde. Git permet de suivre les modifications de tes fichiers, de collaborer avec d'autres et de revenir à des versions précédentes. Que tu codes seul ou en équipe, Git est indispensable.

---

## 1. Qu'est-ce que Git ?

**Git** est un système de gestion de version distribué. Il enregistre les modifications de tes fichiers dans un historique et te permet de :
- Suivre chaque changement effectué
- Revenir à une version antérieure
- Travailler sur plusieurs versions (branches) en parallèle
- Collaborer avec d'autres sur le même projet

**Concepts de base :**
- **Repository (dépôt)** : le dossier contenant ton projet et l'historique Git
- **Commit** : une capture (snapshot) de l'état de tes fichiers à un moment donné
- **Branch (branche)** : une ligne de développement indépendante
- **Merge** : la fusion de deux branches

---

## 2. Installation et configuration

### Installation

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install git

# Vérifier l'installation
git --version
```

### Configuration initiale

Avant ta première utilisation, configure ton identité :

```bash
# Ton nom (remplace par ton vrai nom)
git config --global user.name "Ton Nom"

# Ton email (utilise le même que sur GitHub/GitLab)
git config --global user.email "ton.email@example.com"

# Vérifier ta configuration
git config --list
```

### Configuration de l'éditeur

```bash
# Par défaut, Git utilise Vim. Tu peux changer :
git config --global core.editor nano

# couleur dans le terminal
git config --global color.ui auto
```

---

## 3. Créer un dépôt Git

### git init - Initialiser un nouveau dépôt

```bash
# Créer un nouveau projet
mkdir mon-projet
cd mon-projet

# Initialiser Git
git init
```

Résultat :
```
Initialized empty Git repository in /home/david/mon-projet/.git/
```

Un dossier `.git/` a été créé. C'est le cœur de Git — il contient tout l'historique.

### git clone - Cloner un dépôt existant

Si tu veux travailler sur un projet existant (sur GitHub par exemple) :

```bash
# Cloner un dépôt public
git clone https://github.com/someuser/some-repo.git

# Cloner dans un dossier spécifique
git clone https://github.com/someuser/some-repo.git mon-dossier
```

---

## 4. Les états d'un fichier

Dans Git, chaque fichier peut être dans l'un de ces états :

| État | Description |
|------|-------------|
| **Modified** | Fichier modifié mais pas encore indexé |
| **Staged** | Fichier indexé, prêt à être commité |
| **Committed** | Fichier enregistré dans l'historique |

```
┌──────────────┐    edit     ┌──────────────┐   add    ┌──────────────┐   commit    ┌──────────────┐
│   Untracked  │ ─────────►  │   Modified    │ ───────► │    Staged    │ ─────────►  │  Committed   │
│  (non suivi) │             │  (modifié)    │          │   (indexé)   │             │  (enregistré)│
└──────────────┘             └──────────────┘          └──────────────┘             └──────────────┘
```

---

## 5. Les commandes de base

### git status - État du dépôt

```bash
git status
```

Affiche quels fichiers sont modifiés, stagés ou commité.

```bash
On branch master
Changes not staged for commit:
  modified:   readme.txt

Untracked files:
  nouveau.txt
```

### git add - Indexer un fichier

```bash
# Indexer un fichier précis
git add readme.txt

# Indexer tous les fichiers modifiés
git add .

# Indexer tous les fichiers
git add -A
```

### git commit - Enregistrer les modifications

```bash
# Commiter avec un message (OBLIGATOIRE)
git commit -m "Ajout du fichier readme"

# Indexer ET commiter en une commande
git commit -am "Correction d'un bug"
```

> ⚠️ L'option `-am` ne fonctionne que pour les fichiers déjà suivis. Les nouveaux fichiers doivent être ajoutés avec `git add` d'abord.

---

## 6. L'historique des commits

### git log - Voir l'historique

```bash
# Voir l'historique complet
git log

# Affichage condensé sur une ligne
git log --oneline

# Voir les 5 derniers commits
git log -5

# Affichage avec graphe des branches
git log --oneline --all --graph
```

Exemple de sortie `--oneline` :
```
a1b2c3d Fix navigation bug
e4f5g6h Add user profile page
i7j8k9l Initial commit
```

Chaque commit a un identifiant court (ex: `a1b2c3d`).

### git show - Détails d'un commit

```bash
# Voir les détails d'un commit
git show a1b2c3d

# Voir seulement le message
git log -1 --format="%B" a1b2c3d
```

---

## 7. Les branches

Les branches permettent de travailler sur des fonctionnalités isolées sans perturber le code principal.

### git branch - Lister et créer des branches

```bash
# Lister les branches (celle avec * est la branche active)
git branch

# Créer une nouvelle branche
git branch ma-fonctionnalite

# Créer et basculer sur la nouvelle branche
git checkout -b ma-fonctionnalite

# Raccourci moderne (Git 2.23+)
git switch -c ma-fonctionnalite
```

### git checkout / git switch - Changer de branche

```bash
# Basculer sur une branche existante
git checkout master
git switch master

# Revenir à la branche principale (souvent master ou main)
```

### git merge - Fusionner des branches

```bash
# 1. Basculer sur la branche principale
git checkout master

# 2. Fusionner la branche secondaire
git merge ma-fonctionnalite
```

### git branch -d - Supprimer une branche

```bash
# Supprimer une branche (après fusion)
git branch -d ma-fonctionnalite

# Supprimer de force (même si pas fusionnée)
git branch -D ma-fonctionnalite
```

---

## 8. Annuler des modifications

### git checkout - Annuler les modifications non commitées

```bash
# Annuler les modifications d'un fichier
git checkout -- fichier.txt

# Syntaxe moderne
git restore fichier.txt
```

### git reset - Annuler l'indexation

```bash
# Retirer un fichier de l'index (sans supprimer les modifications)
git reset fichier.txt

# Retirer TOUT de l'index
git reset
```

### git revert - Annuler un commit (en créant un nouveau commit)

```bash
# Annuler le dernier commit (crée un nouveau commit)
git revert HEAD

# Annuler un commit spécifique
git revert a1b2c3d
```

> 💡 `git revert` est **sûr** car il ne réécrit pas l'historique. Il crée un nouveau commit qui "défait" les modifications.

### git reset - Revenir à un commit précédent

```bash
# Revenir au dernier commit (garde les modifications staged)
git reset --soft HEAD~1

# Revenir au dernier commit (garde les modifications, enlève du staging)
git reset --mixed HEAD~1

# Revenir au dernier commit (SUPPRIME les modifications !)
git reset --hard HEAD~1
```

> ⚠️ `--hard` est dangereux : il supprime définitivement les modifications. Utilise-le avec prudence.

---

## 9. Travailler avec un remote (GitHub/GitLab)

### git remote - Gérer les dépôts distants

```bash
# Voir les dépôts distants
git remote -v

# Ajouter un remote
git remote add origin https://github.com/user/repo.git

# Renommer le remote
git remote rename origin github

# Supprimer un remote
git remote remove origin
```

### git push - Envoyer sur le remote

```bash
# Envoyer la branche master sur origin
git push origin master

# Raccourci (si origin et master sont les valeurs par défaut)
git push

# Premier push avec création de la branche distante
git push -u origin ma-branche
```

### git pull - Récupérer les modifications

```bash
# Récupérer et fusionner les modifications distantes
git pull

# Récupérer sans fusionner (voir ce qui va changer)
git fetch
```

### git fetch vs git pull

| Commande | Récupère | Fusionne |
|----------|----------|----------|
| `git fetch` | ✅ | ❌ |
| `git pull` | ✅ | ✅ |

`fetch` te permet de voir ce qui a changé avant de fusionner.

---

## 10. Ignorer des fichiers (.gitignore)

Le fichier `.gitignore` indique à Git quels fichiers ne doivent pas être suivis.

### Créer un .gitignore

```bash
nano .gitignore
```

### Exemple de .gitignore classique

```gitignore
# Fichiers temporaires
*.tmp
*.log

# Dossiers de cache
__pycache__/
*.pyc
node_modules/

# Fichiers secrets
.env
*.pem

# OS
.DS_Store
Thumbs.db
```

### Cas d'usage : Python

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
.env

# IDE
.vscode/
.idea/

# Logs
*.log
```

### Cas d'usage : Node.js

```gitignore
node_modules/
package-lock.json
.env
dist/
build/
```

---

## 11. Résumé des commandes

| Commande | Description |
|----------|-------------|
| `git init` | Créer un nouveau dépôt |
| `git clone url` | Cloner un dépôt existant |
| `git status` | Voir l'état du dépôt |
| `git add fichier` | Indexer un fichier |
| `git commit -m "msg"` | Enregistrer les modifications |
| `git log` | Voir l'historique |
| `git log --oneline` | Historique condensé |
| `git branch` | Lister les branches |
| `git branch nom` | Créer une branche |
| `git checkout branche` | Basculer sur une branche |
| `git switch branche` | Basculer (syntaxe moderne) |
| `git merge branche` | Fusionner une branche |
| `git push` | Envoyer sur le remote |
| `git pull` | Récupérer depuis le remote |
| `git fetch` | Récupérer sans fusionner |
| `git restore fichier` | Annuler les modifications |
| `git revert commit` | Annuler un commit |
| `git reset --hard` | Revenir à un commit (⚠️ destructif) |

---

## 12. Exercice pratique

### Exercice : Ton premier projet Git

**Objectif** : Créer un projet avec Git, faire des modifications et les pousser sur GitHub.

**Étape 1 : Création du projet**

```bash
mkdir projet-test
cd projet-test
git init
git config user.name "Ton Nom"
git config user.email "ton.email@example.com"
```

**Étape 2 : Premier commit**

```bash
echo "# Mon Projet" > README.md
git add README.md
git commit -m "Premier commit : ajout du README"
```

**Étape 3 : Modifier et suivre les changements**

```bash
# Modifier le README
echo "Description de mon projet" >> README.md

# Vérifier l'état
git status

# Indexer et commiter
git add .
git commit -m "Ajout de la description"
```

**Étape 4 : Voir l'historique**

```bash
git log --oneline
```

**Étape 5 : Créer une branche**

```bash
# Créer une branche pour une fonctionnalité
git checkout -b feature-calculatrice

# Ajouter un fichier
echo "print('Calculatrice')" > calculatrice.py
git add .
git commit -m "Ajout de la calculatrice"

# Revenir sur master
git checkout master
```

**Étape 6 : Simuler un conflit de fusion**

```bash
# Merger la feature sur master
git merge feature-calculatrice
```

**Étape 7 : Annuler une erreur (optionnel)**

```bash
# Si tu veux revenir au dernier commit propre
git log --oneline
# Note le hash du commit propre
git reset --hard HEAD~1
```

✅ Tu connais maintenant les bases de Git !

---

## 13. Bonnes pratiques

- **Commits atomiques** : un commit = une modification logique
- **Messages de commit clairs** : décris ce qui a changé, pas comment
- **Braches courtes** : fusionne fréquemment pour éviter les conflits
- **.gitignore** : configure-le dès le début du projet
- **Ne jamais commiter de secrets** : utilise les variables d'environnement

### Format de message de commit recommandé

```
type: Description courte (max 50 caractères)

Explication plus détaillée si nécessaire.
Décompose en plusieurs lignes si le contexte est important.

Liens: #12, #15
```

Types courants : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Exemples de bons messages

```
feat: Ajout de la connexion utilisateur
fix: Correction du bug de navigation sur mobile
docs: Mise à jour du README avec installation
refactor: Simplification de la logique d'authentification
```
