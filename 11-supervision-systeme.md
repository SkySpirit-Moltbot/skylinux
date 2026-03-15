# Leçon 11 : Surveillance et supervision système

Dans cette leçon, tu vas maîtriser tous les outils de surveillance Linux : CPU, mémoire, disque, processus et services. Indispensable pour diagnostiquer les problèmes.

---

## 1. Surveillance CPU

### Commande top

```bash
top                  # Vue en temps réel
top -u david         # Filtrer par utilisateur
top -p 1234          # Surveiller un processus spécifique
top -1               # Rafraîchir chaque seconde
```

### Comprendre la sortie de top

```
top - 10:30:15 up  5:42,  1 user,  load average: 0.52, 0.58, 0.59
Tasks: 245 total,   1 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.3 us,  2.1 sy,  0.0 ni, 92.1 id,  0.0 wa,  0.0 hi,  0.6 si,  0.0 st
MiB Mem :  7938.5 total,  2345.2 free,  4120.0 used,  1473.3 buff/cache
MiB Swap:  2048.0 total,  1024.0 free,  1024.0 used.  5800.0 avail Mem
```

### Commandes interactives de top

| Touche | Description |
|--------|-------------|
| `q` | Quitter |
| `M` | Trier par mémoire |
| `P` | Trier par CPU |
| `k` | Tuer un processus |
| `r` | Modifier la priorité (renice) |
| `1` | Afficher tous les CPUs |
| `f` | Changer les colonnes |
| `x` | Surbrillance colonne tri |

### Load Average

Le **load average** indique la charge système sur 1, 5 et 15 minutes.

| Load | 1 cœur | 4 cœurs | Interprétation |
|------|--------|----------|---------------|
| 1.0 | 100% | 25% | 1 processus en cours |
| 4.0 | 400% | 100% | Système à pleine capacité |
| 8.0 | 800% | 200% | Surcharge (processus en attente) |

---

## 2. Surveillance mémoire

### free - Mémoire vive

```bash
free                # En octets
free -h             # Format lisible (Ko, Mo, Go)
free -m             # En mégaoctets
free -g             # En gigaoctets
free -s 1           # Rafraîchir chaque seconde
```

### Comprendre la sortie

```
              total        used        free      shared  buff/cache   available
Mem:        8.0Gi       4.1Gi       2.3Gi       150Mi       1.5Gi       3.5Gi
Swap:       2.0Gi       512Mi       1.5Gi
```

| Colonne | Description |
|---------|-------------|
| **total** | Mémoire totale |
| **used** | Mémoire utilisée (vraiment) |
| **free** | Mémoire totally libre |
| **buff/cache** | Mémoire pour les buffers/disque |
| **available** | Mémoire disponible pour les apps |
| **Swap** | Mémoire virtuelle sur disque |

### Calcul du pourcentage

```bash
# Calculer le pourcentage utilisé
free | grep Mem | awk '{printf("%.1f\n", $3/$2 * 100)}'
```

---

## 3. Surveillance disque

### df - Espace disque

```bash
df                  # En octets
df -h               # Format lisible
df -H               # FormatIEC (1000 au lieu de 1024)
df -T               # Avec type de système de fichiers
df -i               # Inodes au lieu de blocs
```

### Analyser l'espace

```bash
# Partition la plus pleine
df -h | grep -v tmpfs | sort -k5 -h | tail -5

# Espace par type de filesystem
df -Th | grep -v tmpfs
```

### du - Taille des dossiers

```bash
du -sh dossier/           # Taille totale
du -h --max-depth=1       # Sous-dossiers (1 niveau)
du -h --max-depth=2       # Sous-dossiers (2 niveaux)
du -ah dossier/           # Avec fichiers cachés
du -d 1 -h               # Profondeur 1
du -sh */                 # Tous les sous-dossiers
```

### ncdu - Interface interactive

```bash
# Installer
sudo apt install ncdu

# Utiliser
ncdu                    # Répertoire courant
ncdu /home             # Dossier spécifique
```

---

## 4. Surveillance processus

### ps - Liste des processus

```bash
ps              # Basique
ps aux          # Tous les utilisateurs
ps -ef          # Format étendu
ps -eo pid,ppid,%mem,%cpu,cmd  # Colonnes personnalisées
ps --sort=-%cpu | head -10    # Top CPU
ps --sort=-%mem | head -10    # Top mémoire
```

### Rechercher un processus

```bash
ps aux | grep firefox              # Trouver firefox
pgrep -a firefox                   # Juste les PIDs
pidof firefox                      # PID principal
pstree                             # Vue arborescence
```

### Stat d'un processus

```bash
# Ressources utilisées
pidstat -p 1234 1

# Fichiers ouverts
lsof -p 1234

# Connexions réseau
ss -tp | grep 1234
```

---

## 5. Tuer et gérer les processus

### kill - Envoyer un signal

```bash
kill 1234                    # SIGTERM (propre)
kill -15 1234                # Identique
kill -9 1234                 # SIGKILL (forcement)
kill -SIGTERM -1234          # Groupe de processus
```

###killall et pkill

```bash
killall firefox              # Par nom
pkill firefox                 # Par pattern
pkill -9 -f "python script" # Forcé avec pattern
```

### Modifier la priorité

```bash
nice -n 10 commande          # Priorité basse
renice 5 -p 1234            # Changer priorité
renice -5 -p 1234           # Priorité haute (root)
renice 0 -u david           # Tous les processus d'un user
```

---

## 6. Surveillance réseau

### Commandes utiles

```bash
# Connexions actives
ss -tuln                    # TCP/UDP en écoute
ss -tnp                     # Connexions établies
ss -tp | grep ESTAB         # Connections actives

# Statistiques réseau
netstat -s                   # Stats complètes
netstat -i                   # Stats par interface

# Monitoring temps réel
nload                       # Bande passante
iftop                       # Connexions par hôte
bmon                        # Surveillance graphique
```

---

## 7. Surveillance des services (systemd)

### systemctl

```bash
# État d'un service
systemctl status nginx

# Services actifs
systemctl list-units --type=service --state=running

# Services échoués
systemctl --failed

# Logs d'un service
journalctl -u nginx -n 50
journalctl -u nginx -f
```

---

## 8. Métriques système avancées

### vmstat - Statistiques virtuelles

```bash
vmstat 1                    # Rafraîchir chaque seconde
vmstat -S M 1               # En Mo
vmstat 1 5                  # 5 snapshots
```

### iostat - Statistiques I/O

```bash
# Installer
sudo apt install sysstat

# Utiliser
iostat -x 1                 # Stats détaillées
iostat -dxh 1              # Disques en format lisible
```

### sar - System Activity Reporter

```bash
sar -u 1 10                 # CPU chaque seconde, 10 fois
sar -r 1 10                 # Mémoire
sar -d 1 10                 # Disque
sar -n DEV 1 10             # Réseau
```

---

## 9. Scripts de surveillance

### Script d'alerte disque

```bash
#!/bin/bash

DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $DISK_USAGE -gt 90 ]; then
    echo "ALERTE: Disque à ${DISK_USAGE}%" | mail -s "Alerte Disque" admin@email.com
fi
```

### Script d'alerte mémoire

```bash
#!/bin/bash

MEM_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100)}')

if [ $MEM_USAGE -gt 85 ]; then
    logger "Alerte: Mémoire à ${MEM_USAGE}%"
fi
```

### Surveillance continue

```bash
#!/bin/bash

while true; do
    clear
    echo "=== $(date) ==="
    echo ""
    echo "--- CPU ---"
    top -bn1 | head -5
    echo ""
    echo "--- Mémoire ---"
    free -h
    echo ""
    echo "--- Disque ---"
    df -h / | tail -1
    sleep 5
done
```

---

## 10. Tableau résumé

| Commande | Description |
|----------|-------------|
| `top` | Surveillance CPU/mémoire temps réel |
| `htop` | top avec interface améliorée |
| `free` | Mémoire RAM |
| `df` | Espace disque |
| `du` | Taille dossiers |
| `ps` | Liste processus |
| `kill` | Terminer processus |
| `ss` | Connexions réseau |
| `systemctl` | Gérer services |
| `journalctl` | Logs systemd |

---

Maîtrise ces outils pour devenir un pro de la supervision Linux ! 📊