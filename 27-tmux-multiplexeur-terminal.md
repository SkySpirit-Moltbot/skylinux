# Leçon 27 : tmux - Multiplexeur de Terminal

Dans cette leçon, tu vas maîtriser tmux, un multiplexeur de terminal qui te permet de gérer plusieurs terminaux dans une seule fenêtre, de détacher et rattacher des sessions à distance, et de conserver ton travail même si ta connexion coupe.

---

## 1. Qu'est-ce qu'un multiplexeur de terminal ?

Un **multiplexeur de terminal** comme **tmux** te permet de :

- **Gérer plusieurs terminaux** dans une seule fenêtre
- **Détacher et rattacher** des sessions à distance
- **Partager des sessions** entre utilisateurs
- **Conserver tes sessions** même si ta connexion coupe

Sans tmux : si ta connexion SSH coupe, ton travail est perdu.
Avec tmux : tu te rattaches et tout est intact !

> **Note :** Si tu utilises **screen** à la place de tmux, le principe est le même. tmux est juste plus moderne et mieux maintenu.

---

## 2. Concepts de base

| Concept | Description |
|---------|-------------|
| **Session** | Une session tmux est un environnement complet de terminaux |
| **Fenêtre (Window)** | Un onglet dans la session (comme les onglets d'un navigateur) |
| **Panneau (Pane)** | Une subdivision de la fenêtre (splits horizontaux ou verticaux) |

```
Session tmux
├── Fenêtre 1 (terminal)
│   ├── Panneau gauche
│   └── Panneau droit
├── Fenêtre 2 (logs)
└── Fenêtre 3 (editor)
```

---

## 3. Commandes de base

### tmux - Démarrer tmux

```bash
# Lancer une nouvelle session (nommee)
tmux new -s ma_session

# Lancer rapidement
tmux
```

### Commandes via Ctrl+b

Le préfixe par défaut est **Ctrl+b**. Ensuite tu tapes la commande :

| Commande | Action |
|----------|--------|
| `Ctrl+b d` | Détacher la session (laisser tourner en arrière-plan) |
| `Ctrl+b c` | Créer une nouvelle fenêtre |
| `Ctrl+b ,` | Renommer la fenêtre actuelle |
| `Ctrl+b %` | Split vertical (gauche/droite) |
| `Ctrl+b "` | Split horizontal (haut/bas) |
| `Ctrl+b o` | Passer au panneau suivant |
| `Ctrl+b x` | Fermer le panneau actuel |
| `Ctrl+b w` | Lister les fenêtres |
| `Ctrl+b n` | Fenêtre suivante |
| `Ctrl+b p` | Fenêtre précédente |
| `Ctrl+b 0-9` | Aller à la fenêtre numéro X |
| `Ctrl+b ?` | Afficher toutes les touches |

---

## 4. Se détacher et se rattacher

### tmux ls - Lister les sessions actives

```bash
# Se detacher : Ctrl+b d
# La session continue en arriere-plan !

# Lister les sessions actives
tmux ls
```

### tmux attach - Se rattacher à une session

```bash
# Se rattacher a une session
tmux attach -t ma_session

# Rattacher ou créer si elle n'existe pas
tmux new -A -s ma_session
```

---

## 5. Navigation entre panneaux

```bash
# Passer au panneau suivant
Ctrl+b o

# Aller a un panneau précis
Ctrl+b ;

# Resize du panneau actif
Ctrl+b Alt+flèche   # Redimensionner
Ctrl+b : resize-pane -D  # Agrandir vers le bas
Ctrl+b : resize-pane -U  # Agrandir vers le haut
Ctrl+b : resize-pane -L  # Agrandir vers la gauche
Ctrl+b : resize-pane -R  # Agrandir vers la droite
```

---

## 6. Gestion des fenêtres

```bash
# Renommer la fenêtre actuelle
Ctrl+b ,

# Lister les fenêtres
Ctrl+b w

# Aller a la fenêtre 1
Ctrl+b 1

# Déplacer la fenêtre vers la gauche ou la droite
Ctrl+b : swap-window -t -1   # Échanger avec précédente
Ctrl+b : swap-window -t +1   # Échanger avec suivante
```

---

## 7. Commandes utiles

### Depuis le shell (hors tmux)

```bash
tmux new-session -d -s nom_session 'commande'  # Créer avec commande auto
tmux send-keys -t nom_session 'ls' Enter       # Envoyer une commande
tmux kill-session -t nom_session               # Tuer une session
tmux kill-server                               # Tuer tmux complètement
```

### Depuis l'intérieur de tmux (: pour mode commande)

```bash
:kill-session     # Tuer la session actuelle
:kill-server      # Tuer toutes les sessions
```

---

## 8. Personnalisation avec ~/.tmux.conf

```bash
# Exemple de configuration ~/.tmux.conf
# Activer la souris
set -g mouse on

# Activer le scroll
set -g history-limit 50000

# Commande plus courte (juste Ctrl+a)
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Numérotation commence a 1 (plus intuitif)
set -g base-index 1
setw -g pane-base-index 1

# Coller depuis le presse-papier systeme
set -g default-command "reattach-to-user-namespace -l bash"
```

Après modification :

```bash
tmux source-file ~/.tmux.conf
```

---

## 9. Scrolling et copie de texte

```bash
# Mode copie (scrollback)
Ctrl+b [

# Naviguer avec flèches / PgUp/PgDown
# Chercher avec / (comme dans less)
# Quitter avec q
```

Pour copier :

1. `Ctrl+b [` pour entrer en mode copie
2. `Space` pour commencer la sélection
3. Déplacer avec les flèches
4. `Enter` pour copier
5. `Ctrl+b ]` pour coller

---

## 10. Scripts et automatisation

```bash
#!/bin/bash
# Script pour creer un environnement de travail

session="dev_work"

# Creer session avec 3 fenêtres
tmux new-session -d -s $session
tmux rename-window -t $session:1 'code'
tmux send-keys -t $session:1 'cd ~/projets && code .' Enter

tmux new-window -t $session -n 'server'
tmux send-keys -t $session:server 'cd ~/projets && npm run dev' Enter

tmux new-window -t $session -n 'logs'
tmux send-keys -t $session:logs 'tail -f ~/projets/logs/app.log' Enter

# Se rattacher
tmux attach -t $session
```

---

## 11. Exercices pratiques

### Exercice 1 : Premier usage de tmux

1. Ouvre un terminal et lance tmux :
```bash
tmux new -s demo
```

2. Tape une commande (ex: `ls`)
3. Détache avec `Ctrl+b d`
4. Vérifie que la session existe toujours :
```bash
tmux ls
```

5. Rattache-toi :
```bash
tmux attach -t demo
```

✅ Tu devrais voir le résultat de `ls` - la session a survécu !

### Exercice 2 : Panneaux et fenêtres

1. Crée une nouvelle session :
```bash
tmux new -s exo2
```

2. Sépare en deux verticalement : `Ctrl+b %`
3. Passe au panneau de droite : `Ctrl+b o`
4. Sépare en deux horizontalement : `Ctrl+b "`
5. Ferme un panneau : `Ctrl+b x`
6. Ajoute une fenêtre : `Ctrl+b c`
7. Bascule entre fenêtres : `Ctrl+b n` puis `Ctrl+b p`
8. Détache : `Ctrl+b d`

### Exercice 3 : Configuration tmux

1. Vérifie si le fichier existe :
```bash
ls ~/.tmux.conf
```

2. Crée-le avec cette configuration minimale :
```bash
cat > ~/.tmux.conf << 'EOF'
# Raccourci prefix: Ctrl+a au lieu de Ctrl+b
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Numérotation a partir de 1
set -g base-index 1

# Souris activee
set -g mouse on
EOF
```

3. Recharge la config :
```bash
tmux source-file ~/.tmux.conf
```

4. Teste : `Ctrl+a d` pour détacher

### Exercice 4 : Script de session de travail

Crée un script `start-work.sh` :

```bash
#!/bin/bash
tmux new-session -d -s travail
tmux rename-window -t travail:1 'Terminal'
tmux new-window -t travail -n 'Web' 'cd ~/Sites && python3 -m http.server 8000'
tmux attach -t travail
```

Teste-le :

```bash
chmod +x start-work.sh
./start-work.sh
```

---

## 12. Résumé

| Commande | Description |
|----------|-------------|
| `tmux new -s nom` | Créer une session |
| `tmux ls` | Lister les sessions |
| `tmux attach -t nom` | Se rattacher |
| `Ctrl+b d` | Détacher |
| `Ctrl+b c` | Nouvelle fenêtre |
| `Ctrl+b %` | Split vertical |
| `Ctrl+b "` | Split horizontal |
| `Ctrl+b w` | Lister fenêtres |
| `Ctrl+b [` | Mode scroll/copie |
| `tmux kill-session -t nom` | Supprimer session |
| `tmux source-file ~/.tmux.conf` | Recharger config |

- **tmux** conserve tes sessions même si ta connexion coupe
- Utilise `Ctrl+b` comme préfixe, puis la commande
- Crée plusieurs **fenêtres** (onglets) et **panneaux** (splits)
- Personnalise avec `~/.tmux.conf`



---

## Complément: Screen (alternative à tmux)

### Introduction

Vous avez découvert tmux dans la leçon 27. screen est le multiplexeur de terminal historique, présent sur почти tous les systèmes Unix bien avant tmux. Si tmux n'est pas installé ou si vous devez travailler sur une machine distante ancienne, screen sera votre allié. Il offre les mêmes fonctions essentielles : maintenir des sessions persistantes, diviser l'écran, et reprendre votre travail après une déconnexion.

### Concepts fondamentaux

screen introduit la notion de session — un processus qui tourne en arrière-plan et qui peut abriter plusieurs fenêtres (window). Chaque fenêtre est un pseudo-terminal (pty). Vous pouvez vous détacher (detach) de la session et la retrouver plus tard, même après vous être déconnecté.

### La logique detach/attach

Le principe central de screen : vous vous attachez (attach) à une session. Vous pouvez vous détacher (detach) pour libérer le terminal. La session continue de tourner en arrière-plan. Plus tard, vous vous rattachez.

### Commandes internes de screen

screen s'utilise avec des combinaisons de touches commençant par Ctrl+A (prefix). Par défaut, Ctrl+A suivi de la commande. tmux utilise Ctrl+B comme préfixe — screen utilise Ctrl+A pour ne pas interférer avec le comportement natif du terminal.

### Mode copie et navigation dans l'historique

Le mode copie permet de naviguer dans le scrollback (l'historique visible de la fenêtre) et de copier du texte :

### Personnaliser avec .screenrc

Le fichier ~/.screenrc configure le comportement par défaut de screen. Voici un exemple complet :

### Surveillance d'activité

Screen peut vous alerter quand une fenêtre affiche quelque chose pendant que vous êtes dans une autre fenêtre — très utile pour les scripts longs ou les téléchargements :

### Loguer une session

Screen peut enregistrer tout ce qui passe dans une fenêtre dans un fichier :

### Envoyer des commandes à une session screen

screen -S session -X commande envoie une commande à une session sans s'attacher :

### Définir un titre de fenêtre dynamiquement

Quand vous lancez un script ou un serveur, un titre explicite aide à s'y retrouver :

### Utilisation avancée : multi-attach

Screen permet à plusieurs terminaux de se rattacher à la même session simultanément (multi-attach) — pratique pour collaborer à distance :

### Résumé

screen -S nom = créer une session nommée

Ctrl+A D = se détacher sans fermer les fenêtres

screen -r = se rattacher à une session

Ctrl+A C = nouvelle fenêtre dans la session

Ctrl+A " = lister et choisir une fenêtre

Ctrl+A S et Ctrl+A | = diviser l'écran

Ctrl+A TAB = naviguer entre les splits

Ctrl+A [ puis Esc = mode copie pour naviguer dans l'historique

Ctrl+A H = activer le logging d'une fenêtre

~/.screenrc = fichier de configuration personnel

screen -dmS nom "cmd" = créer une session détachée qui exécute une commande
