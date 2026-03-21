# Leçon 27 : tmux - Multiplexeur de Terminal

## Qu'est-ce qu'un multiplexeur de terminal ?

Un **multiplexeur de terminal** comme **tmux** te permet de :

- **Gérer plusieurs terminaux** dans une seule fenêtre
- **Détacher et rattacher** des sessions à distance
- **Partager des sessions** entre utilisateurs
- **Conserver tes sessions** même si ta connexion coupe

Sans tmux : si ta connexion SSH coupe, ton travail est perdu.
Avec tmux : tu te rattaches et tout est intact !

## Concepts de base

| Concept | Description |
|---------|-------------|
| **Session** | Une session tmux est un environnement complet de terminaux |
| **Fenêtre (Window)** | Un onglet dans la session (comme les onglets d'un navigateur) |
| **Panneau (Pane)** | Une subdivision de la fenêtre (splits horizontaux/verticaux) |

```
Session tmux
├── Fenêtre 1 (terminal)
│   ├── Panneau gauche
│   └── Panneau droit
├── Fenêtre 2 (logs)
└── Fenêtre 3 (editor)
```

## Commandes de base

### Démarrer tmux

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

### Se détacher et se rattacher

```bash
# Se detacher : Ctrl+b d
# La session continue en arriere-plan !

# Lister les sessions actives
tmux ls

# Se rattacher a une session
tmux attach -t ma_session

# Rattacher ou créer si elle n'existe pas
tmux new -A -s ma_session
```

## Navigation entre panneaux

```bash
# Passer au panneau suivant
Ctrl+b o

# Aller a un panneau précis (avec mouse enabled ou pas)
Ctrl+b ;

# Utiliser la souris (si active)
# Clic directement sur le panneau

# Resize du panneau actif
Ctrl+b Alt+flèche   # Redimensionner
Ctrl+b : resize-pane -D  # Agrandir vers le bas
Ctrl+b : resize-pane -U  # Agrandir vers le haut
Ctrl+b : resize-pane -L  # Agrandir vers la gauche
Ctrl+b : resize-pane -R  # Agrandir vers la droite
```

## Gestion des fenêtres

```bash
# Renommer la fenêtre actuelle
Ctrl+b ,

# Lister les fenêtres
Ctrl+b w

# Aller a la fenêtre 1
Ctrl+b 1

# Déplacer la fenêtre vers la gauche/droite
Ctrl+b : swap-window -t -1   # Échanger avec précédente
Ctrl+b : swap-window -t +1   # Échanger avec suivante
```

## Commandes utiles

```bash
# Depuis le shell (hors tmux)
tmux new-session -d -s nom_session 'commande'  # Créer avec commande auto
tmux send-keys -t nom_session 'ls' Enter       # Envoyer une commande
tmux kill-session -t nom_session               # Tuer une session
tmux kill-server                               # Tuer tmux complètement

# Depuis l'intérieur de tmux (: pour mode commande)
:kill-session     # Tuer la session actuelle
:kill-server      # Tuer toutes les sessions
```

## Personnalisation avec ~/.tmux.conf

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

## Scrolling et copie de texte

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

## Scripts et automatisation

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

## Exercices pratiques

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

## Résumé

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
-战友 (**战友** = "camarade de combat" en chinois - utile quand tu bosses en remote avec des collegues !)

---

*Retour au menu : [README.md](../README.md)*
