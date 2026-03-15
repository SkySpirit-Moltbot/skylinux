# Leçon 16 : Éditeurs de texte en ligne de commande

Dans cette leçon, tu vas maîtriser les deux éditeurs de texte essentiels sous Linux : **Nano** (simple) et **Vim** (puissant). Ces éditeurs sont indispensables pour modifier des fichiers de configuration, écrire des scripts et éditer du code.

---

## 1. Introduction aux éditeurs

### Pourquoi un éditeur en ligne de commande ?

- Modifier des fichiers de configuration système
- Écrire des scripts
- Éditer sur des serveurs distants (SSH)
- Rapidité et efficacité
- Pas besoin d'interface graphique

### Les deux approches

| Nano | Vim |
|------|-----|
| Simple, immédiat | Puissant, nécessite apprentissage |
| Raccourcis affichés | Modes de fonctionnement |
| Idéal débutants | Idéal experts |
| Édition linéaire | Édition structurée |

---

## 2. NANO - L'éditeur simple

### Lancer Nano

```bash
nano                    # Nouveau fichier
nano fichier.txt        # Ouvrir fichier existant
nano -c fichier.txt     # Afficher position curseur
nano -m fichier.txt     # Activer souris
nano +10 fichier.txt    # Aller à la ligne 10
nano -i fichier.txt    # Indentation automatique
```

### Interface Nano

```
 GNU nano 6.2           Modification de fichier.txt                          
^G Aide    ^O Écrire   ^R Lire    ^X Quitter   ^C Position ^_ Recherche
```

Le `^` représente la touche **Ctrl**.

### Raccourcis essentiels

| Raccourci | Action | Description |
|-----------|--------|-------------|
| **Ctrl + O** | Save | Écrire/Sauvegarder |
| **Ctrl + X** | Exit | Quitter |
| **Ctrl + W** | Where | Rechercher |
| **Ctrl + \** | Replace | Rechercher et remplacer |
| **Ctrl + K** | Cut | Couper la ligne |
| **Ctrl + U** | Paste | Coller la ligne |
| **Ctrl + C** | Location | Afficher position |
| **Ctrl + G** | Help | Aide |

### Navigation

| Raccourci | Action |
|-----------|--------|
| Ctrl + A | Début de ligne |
| Ctrl + E | Fin de ligne |
| Ctrl + Y | Page précédente |
| Ctrl + V | Page suivante |
| Ctrl + _ | Aller à une ligne |
| Meta + \ | Aller au début |
| Meta + / | Aller à la fin |

> **Note** : Meta = Alt ou Échap

### Rechercher et remplacer

```bash
# Rechercher
Ctrl + W, taper le mot, Entrée
# Suivant: Ctrl + W puis Entrée

# Rechercher et remplacer
Ctrl + \ , taper recherche, Entrée, taper remplacement, Entrée
# Confirmer: A pour tous, Y pour un par un
```

###nano par défaut

```bash
# Créer ~/.nanorc
set linenumbers      # Numéros de ligne
set mouse           # Support souris
set autoindent      # Indentation auto
set noread          # Fichiers ouverts en lecture seule
```

---

## 3. VIM - L'éditeur puissant

### Vim vs Vi

- **Vi** : Ancêtre, présent sur tous les Unix
- **Vim** : Vi Improved, version améliorée (la plus utilisée)

### Lancer Vim

```bash
vim                     # Vim vide
vim fichier.txt         # Ouvrir fichier
vim +10 fichier.txt     # Ligne 10
vim +/motif fichier     # Rechercher "motif"
vim -R fichier.txt      # Lecture seule
vim -d fichier1.txt fichier2.txt   # Comparer 2 fichiers
```

---

## 4. Les modes de Vim

C'est le concept le plus important à comprendre !

### Les 3 modes principaux

| Mode | Description | Comment y entrer | Comment en sortir |
|------|-------------|------------------|-------------------|
| **NORMAL** | Navigation, commandes | Par défaut | Échap |
| **INSERTION** | Écrire du texte | `i`, `a`, `o` | Échap |
| **COMMANDE** | Commandes avancées | `:` | Échap |

### Mode Normal

C'est le mode par défaut quand vous ouvrez Vim. Ici, chaque touche exécute une commande !

```bash
# Quand vous tapez "x", ça supprime le caractère, ça n'écrit pas "x" !
# C'est normal, c'est le mode NORMAL.
```

**Mouvements de base :**
```bash
h j k l           # Gauche, Bas, Haut, Droite (ou flèches)
w                 # Mot suivant
b                 # Mot précédent
e                 # Fin du mot
0                 # Début de ligne
$                 # Fin de ligne
gg                # Début du fichier
G                 # Fin du fichier
:n                # Aller à la ligne n
%                 # Aller à l'accolade opposante
```

### Passer en mode Insertion

```bash
i          # Insertion avant le curseur (le plus utilisé)
I          # Insertion début de ligne
a          # Insertion après le curseur
A          # Insertion fin de ligne
o          # Nouvelle ligne dessous
O          # Nouvelle ligne dessus
s          # Supprimer caractère et insérer
S          # Supprimer ligne et insérer
cc         # Supprimer ligne et insérer
```

**Touche Échap** ou **Ctrl + [** pour revenir au mode Normal !

### Mode Commande

En mode Normal, taper `:` pour accéder aux commandes.

```bash
:w             # Enregistrer (write)
:wq            # Enregistrer et quitter
:x             # Enregistrer et quitter (plus court)
:q             # Quitter (si pas de changement)
:q!            # Quitter sans enregistrer
:wqa           # Enregistrer et quitter tous les fichiers
:qa            # Quitter tous les fichiers
```

---

## 5. Commandes du mode Normal

### Suppression et modification

| Commande | Action |
|----------|--------|
| `x` | Supprimer caractère |
| `X` | Supprimer caractère avant |
| `dd` | Supprimer ligne |
| `dw` | Supprimer mot |
| `d$` | Supprimer jusqu'à fin de ligne |
| `d0` | Supprimer jusqu'à début de ligne |
| `D` | Supprimer jusqu'à fin de ligne |
| `cc` | Supprimer ligne et passer en insertion |
| `C` | Supprimer et insérer |
| `r` | Remplacer un caractère |
| `R` | Mode remplacement |
| `~` | Inverser casse |
| `.` | Répéter dernière commande |

### Copier/Coller

| Commande | Action |
|----------|--------|
| `yy` | Copier ligne (yank) |
| `yw` | Copier mot |
| `y$` | Copier jusqu'à fin de ligne |
| `p` | Coller après curseur |
| `P` | Coller avant curseur |
| `"+y` | Copier vers presse-papiers système |
| `"+p` | Coller depuis presse-papiers système |

### Annuler/Rétablir

| Commande | Action |
|----------|--------|
| `u` | Annuler (undo) |
| Ctrl + R | Rétablir (redo) |
| `U` | Annuler tout sur la ligne |

### Recherche

| Commande | Action |
|----------|--------|
| `/motif` | Rechercher en avant |
| `?motif` | Rechercher en arrière |
| `n` | Occurrence suivante |
| `N` | Occurrence précédente |
| `*` | Rechercher mot sous curseur |
| `#` | Rechercher mot sous curseur (arrière) |

---

## 6. Commandes du mode Commande

### Enregistrement et sauvegarde

```bash
:w             # Enregistrer
:w fichier     # Enregistrer sous
:wq            # Enregistrer et quitter
:x             # Enregistrer et quitter
:q             # Quitter
:q!            # Quitter sans enregistrer
:wqa           # Enregistrer et quitter tout
:qa            # Quitter tout
:qa!           # Forcer quitter tout
```

### Rechercher et remplacer

```bash
:/motif        # Rechercher
:%s/old/new/   # Remplacer premiere occurrence
:%s/old/new/g  # Remplacer toutes les occurrences
:%s/old/new/gc # Confirmer chaque remplacement
:s/old/new/    # Ligne actuelle seulement
:5,10s/old/new/g  # Lignes 5 à 10
```

### Édition avancée

```bash
:set nu         # Afficher numéros de ligne
:set nonu       # Masquer numéros
:set hlsearch   # Surligner recherches
:set incsearch  # Recherche incrémentale
:set syntax on  # Coloration syntaxique
:set tabstop=4  # Taille tabulation
:set expandtab  # Espaces au lieu de tab
```

---

## 7. Sélection visuelle

### Mode Visuel

```bash
v           # Mode visuel (caractère)
V           # Mode visuel (ligne)
Ctrl + V    # Mode visuel (bloc)
```

### Avec sélection

```bash
y           # Copier (yank)
d           # Supprimer
c           # Supprimer et insérer
>           # Indenter à droite
<           # Indenter à gauche
!           # Filtrer avec commande externe
```

---

## 8. Fenêtres et splits

### Splits horizontaux et verticaux

```bash
:split           # Split horizontal
:vsplit          # Split vertical
Ctrl + w + h     # Allergauche
Ctrl + w + j     # Allerbas
Ctrl + w + k     # Alleren haut
Ctrl + w + l     # Allerdroite
Ctrl + w + w     # Passer à la fenêtre suivante
Ctrl + w + =     # Égaliser les fenêtres
Ctrl + w + _     # Maximiser horizontale
Ctrl + w + |    # Maximiser verticale
:close           # Fermer la fenêtre
```

---

## 9. Macros

### Enregistrer et exécuter

```bash
# Commencer l'enregistrement (registre a)
qa

# Faire des actions
I# <Esc>

# Arrêter l'enregistrement
q

# Exécuter la macro
@a

# Exécuter 5 fois
5@a
```

---

## 10. Fichiers de configuration Vim

### ~/.vimrc basique

```syntax
" Mon fichier .vimrc

" Basique
set number          " Numéros de ligne
set relativenumber  " Numéros relatifs
set cursorline     " Surbrillance ligne
set showcmd         " Commande en cours

" Indentation
set autoindent     " Indentation auto
set smartindent    " Indentation intelligente
set shiftwidth=4   " Taille indentation
set tabstop=4      " Taille tab

" Recherche
set ignorecase     " Ignorer casse
set smartcase      " Casse si majuscule
set hlsearch       " Surligner recherche
set incsearch      " Recherche incrémentale

" Couleurs
syntax on          " Coloration syntaxique
colorscheme default

" Divers
set mouse=a        " Support souris
set backspace=2    " Backspace fonctionne
```

---

## 11. vimtutor - Le meilleur moyen d'apprendre

```bash
# Lancer le tutorial interactif
vimtutor

# Version française (si disponible)
vimtutor fr
```

C'est un tutorial de 30 minutes directement dans le terminal. **HIGHEMENT recommandé !**

---

## 12. Exercices pratiques

### Exercice 1 : Nano basique
```bash
# Créer un fichier
nano test.txt

# Écrire du texte
# Utiliser Ctrl+O pour sauvegarder
# Utiliser Ctrl+X pour quitter

# Vérifier
cat test.txt
```

### Exercice 2 : Vim premier pas
```bash
# Ouvrir vim
vim

# Passer en mode insertion (i)
# Écrire "Bonjour"
# Échap pour revenir en mode normal
# :wq pour sauvegarder et quitter
```

### Exercice 3 : Vim avancé
```bash
# Ouvrir un fichier
vim fichier.txt

# Naviguer: gg (début), G (fin)
# Supprimer: dd, dw, x
# Copier/Coller: yy, p
# Rechercher: /motif
# Remplacer: :%s/old/new/g
```

### Exercice 4 : vimtutor
```bash
# Faire le tutorial
vimtutor

# Faire les 2 premières leçons
```

---

## 13. Tableau résumé Nano

| Raccourci | Action |
|-----------|--------|
| Ctrl + O | Écrire |
| Ctrl + X | Quitter |
| Ctrl + W | Rechercher |
| Ctrl + K | Couper ligne |
| Ctrl + U | Coller |

---

## 14. Tableau résumé Vim

### Modes

| Mode | Description |
|------|-------------|
| Normal | Par défaut, commandes |
| Insertion | Écrire du texte |
| Visuel | Sélection |
| Commande | :commandes |

### Touches essentielles

| Touche | Action |
|--------|--------|
| `i` | Mode insertion |
| Échap | Retour mode normal |
| `:wq` | Enregistrer et quitter |
| `dd` | Supprimer ligne |
| `yy` | Copier ligne |
| `p` | Coller |
| `/` | Rechercher |
| `u` | Annuler |
| Ctrl + R | Rétablir |

---

## 15. Quand utiliser quoi ?

| Situation | Éditeur recommandé |
|-----------|-------------------|
| Édition rapide | Nano |
|Débutant | Nano |
| Fichier config système | Nano ou Vim |
| Programmation | Vim (avec plugins) |
| Gros fichiers | Vim |
| Édition sur serveur | Vim |
| Apprentisage | vimtutor |

---

Maîtrise ces deux éditeurs et tu pourras éditer n'importe quel fichier sous Linux ! ✍️