# Leçon 4 : Processus et Services

Un processus est un programme en cours d'exécution. Dans cette leçon, tu vas maîtriser la gestion des processus sous Linux : voir, surveiller, gérer les priorités et contrôler les services.

---

## 1. Comprendre les processus

### Qu'est-ce qu'un processus ?

Un processus est une instance d'un programme en cours d'exécution. Chaque processus possède :
- Un **PID** unique (Process ID)
- Un **PPID** (Parent PID - processus qui l'a lancé)
- Un utilisateur propriétaire
- Des ressources (CPU, mémoire, fichiers ouverts)

### Types de processus

| Type | Description |
|------|-------------|
| **Processus interactif** | Démarré par l'utilisateur, attaché au terminal |
| **Daemon** | Service en arrière-plan, au démarrage du système |
| **Processus enfant** | Créé par un autre processus (fork) |
| **Processus zombie** | Processus terminé mais pas encore nettoyé par le parent |
| **Processus orphelin** | Processus dont le parent est mort |

---

## 2. Voir les processus

### Commande PS

```bash
ps                    # Vos processus du terminal courant
ps -e                 # Tous les processus du système
ps aux                # Format BSD (tous utilisateurs)
ps -ef                # Format UNIX (plus détaillé)
ps -eo pid,ppid,user,cmd,%cpu,%mem  # Colonnes personnalisées
```

### Comprendre la sortie de `ps aux`

```
USER       PID  %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
david     1234  10.5  5.2  524288 102400 ?       S    10:00   2:30 firefox
```

| Colonne | Signification |
|---------|---------------|
| USER | Propriétaire du processus |
| PID | Numéro unique du processus |
| %CPU | Pourcentage CPU utilisé |
| %MEM | Pourcentage mémoire utilisée |
| VSZ | Taille virtuelle (Ko) |
| RSS | Mémoire résidente (Ko) |
| TTY | Terminal associé (? = pas de terminal) |
| STAT | État du processus |
| START | Heure de démarrage |
| TIME | Temps CPU累计 |
| COMMAND | Commande exécutée |

### États des processus (colonne STAT)

| État | Signification |
|------|---------------|
| `R` | Running (en cours d'exécution) |
| `S` | Sleeping (en attente) |
| `D` | Disk sleep (IO) |
| `Z` | Zombie (terminé mais non nettoyé) |
| `T` | Stopped (arrêté) |
| `I` | Idle (inactif) |

### Commandes TOP et HTOP

```bash
# top - surveiller les processus en temps réel
top                  # Vue basique
top -u david         # Processus d'un utilisateur
top -p 1234          # Surveiller un processus spécifique
# Touches interactives:
#   q = quitter
#   M = trier par mémoire
#   P = trier par CPU
#   k = tuer un processus
#   r = changer la priorité (nice)

# htop - version améliorée (doit être installé)
htop                  # Plus visuel et ergonomique
htop -u david         # Filtrer par utilisateur
htop -p 1234,5678     # Surveiller plusieurs PIDs
```

---

## 3. Rechercher des processus

### grep et ps

```bash
ps aux | grep firefox        # Trouver firefox
ps aux | grep -v grep       # Exclure grep lui-même
ps aux | grep -i chrome     # Insensible à la casse
```

### pgrep - recherche simplifiée

```bash
pgrep firefox               # Retourne juste les PIDs
pgrep -a firefox           # Avec la commande complète
pgrep -u david chrome      # Processus d'un utilisateur
pgrep -f "python.*script"  # Recherche dans les arguments
pgrep -n firefox           # Le plus récent
pgrep -o firefox           # Le plus ancien
```

### pidof - trouver par nom de programme

```bash
pidof firefox              # Retourne tous les PIDs
pidof -s firefox           # Un seul PID (le plus ancien)
```

---

## 4. Signaux et gestion des processus

### La commande KILL

```bash
kill <PID>                 # Envoyer signal TERM (15)
kill -L                    # Liste des signaux disponibles
kill -SIGTERM 1234         # Signal terme (propre)
kill -SIGKILL 1234         # Signal KILL (forcement)
kill -STOP 1234            # Suspendre le processus
kill -CONT 1234            # Reprendre le processus
```

### Les signaux importants

| Signal | Numéro | Description | Usage normal |
|--------|--------|-------------|--------------|
| SIGTERM | 15 | Terminaison normale | `kill 1234` |
| SIGKILL | 9 | Terminaison forcée | `kill -9 1234` |
| SIGSTOP | 19 | Suspendre | `kill -STOP 1234` |
| SIGCONT | 18 | Reprendre | `kill -CONT 1234` |
| SIGHUP | 1 | Hangup (reload) | `kill -HUP 1234` |
| SIGINT | 2 | Interruption (Ctrl+C) | `kill -INT 1234` |

###killall - tuer par nom

```bash
killall firefox            # Tuer tous les firefox
killall -i firefox        # Mode interactif
killall -9 firefox        # Forcé
killall -u david chrome   # Tous les进程 d'un utilisateur
```

### pkill - tuer avec pattern

```bash
pkill firefox              # Tuer par nom
pkill -f "python"         # Par argument
pkill -u david            # Tous les进程 d'un utilisateur
pkill -9 -f "zombie"      # Forcé avec pattern
```

---

## 5. Contrôle des tâches (Job Control)

### Commandes de job

```bash
# Lancer en arrière-plan
commande &                 # & à la fin

# Contrôler les jobs
jobs                      # Liste des jobs
fg %1                     # Mettre au premier plan
bg %1                     # Reprendre en arrière-plan

# Suspendre (Ctrl+Z dans le terminal)
Ctrl+Z                    # Suspendre le进程 actuel

# Tuer le job actuel
Ctrl+C                    # Interruption
```

### Exemple pratique

```bash
# 1. Lancer une commande longue
sleep 100 &

# 2. Voir les jobs
jobs
# [1]+  Running                 sleep 100 &

# 3. Suspendre (Ctrl+Z)
# [1]+  Stopped                 sleep 100

# 4. Relancer en arrière-plan
bg %1

# 5. Tuer le job
kill %1
# ou
kill $(jobs -p)
```

---

## 6. Priorités et Nice

### Comprendre les priorités

Linux attribue une priorité -20 (plus prioritaire) à +19 (moins prioritaire).

### nice - lancer avec priorité

```bash
nice -n 10 commande        # Priorité basse (10)
nice -n -5 commande       # Priorité haute (-5, nécessite root)
nice --10 commande         # Équivalent à -n -10
nice commande              # Priorité par défaut (0)
```

### renice - changer la priorité

```bash
renice 10 -p 1234          # Mettre priorité 10
renice -5 -p 1234          # Mettre priorité -5 (root uniquement)
renice 5 -u david          # Tous les进程 de david à priorité 5
```

### htop pour gérer les priorités

```bash
htop
# Appuyer sur 'r' puis sélectionner le processus
```

---

## 7. Services et Daemons (systemd)

### Introduction à systemd

systemd est le système d'initialisation moderne de Linux. Il gère les services (daemons).

### Commandes systemctl

```bash
# Status et informations
systemctl status nginx           # Statut du service
systemctl is-active nginx        # Actif ? (active/inactive)
systemctl is-enabled nginx       # Au démarrage ? (enabled/disabled)
systemctl list-units --type=service  # Tous les services
systemctl list-unit-files        # Tous les services configurés

# Gestion
systemctl start nginx            # Démarrer
systemctl stop nginx            # Arrêter
systemctl restart nginx         # Redémarrer
systemctl reload nginx          # Recharger config
systemctl reload-or-restart nginx  # Recharger ou redémarrer
systemctl enable nginx          # Activer au boot
systemctl disable nginx         # Désactiver au boot
systemctl mask nginx            # Masquer (empêcher lancement)
systemctl unmask nginx          # Démasquer

# Journal
journalctl -u nginx             # Logs du service
journalctl -u nginx -f          # Logs en temps réel
journalctl --since "1 hour ago"  # Logs dernière heure
```

### Exemples pratiques

```bash
# Voir tous les services actifs
systemctl list-units --type=service --state=running

# Voir les services qui ont échoué
systemctl --failed

# Statut détaillé avec logs
systemctl status nginx -l

# Redémarrer un service qui a échoué
systemctl restart nginx
```

---

## 8. Surveillance avancée

### Commandes utiles

```bash
# voir les ressources
free -h                  # Mémoire
df -h                    # Disque
uptime                   # Charge système

# Surveillance réseau des processus
lsof -p 1234             # Fichiers ouverts par processus
lsof -i                  # Connexions réseau
ss -tulnp               # Ports en écoute

# Statistiques temps réel
vmstat 1                 # Statistiques système
iostat -x 1              # I/O disque
```

---

## 9. Exercices pratiques

### Exercice 1 : Surveillance
```bash
# Ouvrir htop et observer les processus
htop

# Identifier les processus qui utilisent le plus de CPU
# Taper 'P' pour trier par CPU
```

### Exercice 2 : Gestion de processus
```bash
# Créer un processus
sleep 60 &

# Trouver son PID
pgrep -a sleep

# Le tuer
kill <PID>

# Vérifier
pgrep sleep
```

### Exercice 3 : Service nginx
```bash
# Installer nginx
sudo apt install nginx

# Démarrer le service
sudo systemctl start nginx

# Vérifier le statut
sudo systemctl status nginx

# Arrêter
sudo systemctl stop nginx
```

---

## 10. Tableau résumé

| Commande | Description |
|----------|-------------|
| `ps aux` | Liste des processus |
| `top` | Moniteur temps réel |
| `htop` | Moniteur amélioré |
| `pgrep` | Rechercher par nom |
| `kill` | Envoyer un signal |
| `pkill` | Tuer par nom |
| `jobs` | Liste des jobs |
| `fg/bg` | Premier/arrière-plan |
| `nice` | Lancer avec priorité |
| `renice` | Changer priorité |
| `systemctl` | Gérer les services |

---

Maîtrise ces commandes pour devenir un pro de l'administration Linux ! 💪