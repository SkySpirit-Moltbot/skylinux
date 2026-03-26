# Leçon 34 : Surveillance et optimisation des performances système

Dans cette leçon, tu vas apprendre à diagnostiquer les goulots d'étranglement et à optimiser les performances de ton système Linux. Nous verrons les outils de benchmark, les techniques de tuning système, et les bonnes pratiques pour garder ta machine réactive.

---

## 1. Installer les outils de benchmark

Avant de commencer, installe les paquets nécessaires :

```bash
sudo apt update
sudo apt install sysstat stress sysbench tuned -y
```
- sysstat — outils iostat, mpstat, pidstat
- stress — pour simuler de la charge
- sysbench — benchmark CPU, mémoire, fichiers
- tuned — daemon d'optimisation automatique

---

## 2. Identifier les goulots d'étranglement

### Top — triage par ressource

```bash
# Afficher par utilisation mémoire (tapez M)
top -o %MEM
# Afficher par temps CPU (tapez P)
top -o %CPU
```

### Iostat — statistiques disque

```bash
# Statistiques d'utilisation disque (2 secondes, 3 fois)
iostat -x 2 3
# Uniquement le périphérique sda, rapports étendus
iostat -x sda 1 5
```

### Mpstat — statistiques CPU

```bash
# Stats CPU par cœur, intervalle de 1 seconde
mpstat -P ALL 1 3
# Affichage en temps réel toutes les secondes
mpstat 1
```

### Pidstat — stats par processus

```bash
# Surveiller les 5 premiers processus par utilisation CPU
pidstat -p $(pgrep -d',' | tr ',' ' ') -u 1 1 | head -20
# Surveiller les E/S disque d'un processus (remplace 1234 par le PID)
pidstat -d 1 1 -p 1234
```

---

## 3. Benchmarks avec sysbench

### Test CPU

```bash
# Test CPU : calculer les nombres premiers pendant 10 secondes
sysbench cpu --cpu-max-prime=20000 --time=10 run
```

### Test mémoire

```bash
# Test mémoire : opérations de lecture pendant 10 secondes
sysbench memory --time=10 --memory-block-size=1M --memory-total-size=10G run
```

### Test fichiers (disque)

```bash
# Préparer le fichier de test (2 Go)
sysbench fileio --file-total-size=2G --file-test-mode=rndrw prepare
# Lancer le benchmark lecture/écriture aléatoire
sysbench fileio --file-total-size=2G --file-test-mode=rndrw --time=30 run
# Nettoyer les fichiers de test
sysbench fileio cleanup
```

---

## 4. Tuning système avec sysctl

sysctl permet de modifier les paramètres du noyau Linux à chaud. Ces paramètres contrôlent la mémoire, le réseau, les fichiersystems et bien plus encore.

### Paramètres réseau

```bash
# Voir la valeur actuelle d'un paramètre
sysctl net.ipv4.tcp_fin_timeout
# Modifier un paramètre temporairement (jusqu'au prochain reboot)
sudo sysctl -w net.ipv4.tcp_fin_timeout=15
```

### Rendre les changements permanents

```bash
# Créer un fichier de configuration personnalisé
sudo nano /etc/sysctl.d/99-custom.conf
# Contenu du fichier :
# Optimisation réseau
net.ipv4.tcp_fin_timeout = 15
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 2048
# Optimisation mémoire (réduire la swapiness si assez de RAM)
vm.swappiness = 10
vm.dirty_ratio = 15
# Appliquer sans redémarrer
sudo sysctl -p /etc/sysctl.d/99-custom.conf
```

### Paramètres clés à connaître
| Paramètre | Description | Valeur typique |
| --- | --- | --- |
| vm.swappiness | Propension à utiliser la swap (0-100) | 10-60 |
| vm.dirty_ratio | % RAM avant écriture forcée sur disque | 15-40 |
| net.core.somaxconn | Connexions simultanées en attente | 1024 |
| net.ipv4.tcp_fin_timeout | Durée attente fermeture connexion TCP | 15-60 |
| fs.file-max | Nombre max de fichiers ouverts système | 2097152 |

---

## 5. Ordonnanceur I/O et priorité des processus

### Choisir l'ordonnanceur disque

```bash
# Voir l'ordonnanceur actuel d'un disque
cat /sys/block/sda/queue/scheduler
# SSD : utiliser mq-deadline ou none
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
# Disque dur mécanique (HDD) : bfq pour priorité interactive
echo bfq | sudo tee /sys/block/sda/queue/scheduler
```

### Ionice — priorité d'accès disque

```bash
# Voir la classe et priorité I/O d'un processus
ionice -p 1234
# Lancer une commande en classe idle (plus basse priorité)
ionice -c 3 tar -czf backup.tar.gz /home
# Lancer en classe best-effort, priorité 7 (la plus basse)
ionice -c 2 -n 7 rsync -a /home/ /backup/
```

### Nice et renice — priorité CPU

```bash
# Lancer une commande avec priorité réduite (19 = plus basse)
nice -n 19 tar -czf backup.tar.gz /home
# Changer la priorité d'un processus déjà lancé (PID 1234)
sudo renice +10 -p 1234
# Lancer htop pour voir la nice value de chaque processus
htop
```

---

## 6. tuned — optimisation automatique

tuned est un daemon qui applique automatiquement des profils d'optimisation selon le cas d'usage de ta machine.

```bash
# Vérifier le statut de tuned
sudo systemctl status tuned
# Lister les profils disponibles
tuned-adm list
# Activer le profil desktop (équilibre performances/énergie)
sudo tuned-adm profile desktop
# Serveur : profil throughput-performance
sudo tuned-adm profile throughput-performance
# Laptop sur batterie : profil powersave
sudo tuned-adm profile powersave
# Activer au démarrage
sudo systemctl enable tuned
```

---

## 7. Gérer la swap et la mémoire

```bash
# Voir l'utilisation de la swap
free -h
# Voir le swappiness actuel
cat /proc/sys/vm/swappiness
# Réduire le swappiness (machines avec beaucoup de RAM)
sudo sysctl vm.swappiness=10
# Vider le cache (drop caches) — nécessite sudo
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

---

## 8. Optimisation des fichiersystems

```bash
# Voir les options de montage d'une partition
mount | grep ' / '
# Ajouter noatime dans /etc/fstab pour réduire les écritures disque
# Modifier /etc/fstab — exemple pour la partition racine :
# Remplacer :
# UUID=xxxx  /  ext4  defaults  0  1
# Par :
# UUID=xxxx  /  ext4  defaults,noatime  0  1
# Vérifier la fragmentation d'un filesystem ext4
sudo e4defrag /dev/sda1
```

---

## 9. Script de diagnostic rapide

```bash
#!/bin/bash
# Script de diagnostic performances
echo "=== TOP 10 processus par CPU ==="
ps aux --sort=-%cpu | head -11
echo "=== TOP 10 processus par mémoire ==="
ps aux --sort=-%mem | head -11
echo "=== Utilisation mémoire et swap ==="
free -h
echo "=== Espace disque ==="
df -h
echo "=== Load average ==="
uptime
```

---

## 10. Résumé
| Commande | Usage |
| --- | --- |
| iostat -x 1 3 | Statistiques disque (goulot d'étranglement I/O) |
| mpstat -P ALL 1 | Utilisation CPU par cœur |
| pidstat -d 1 | E/S disque par processus |
| sysbench cpu run | Benchmark CPU |
| sysctl -w param=valeur | Modifier un paramètre noyau à chaud |
| /etc/sysctl.d/*.conf | Paramètres permanents du noyau |
| ionice -c 3 cmd | Lancer une commande en basse priorité I/O |
| nice -n 19 cmd | Lancer en basse priorité CPU |
| tuned-adm profile | Optimisation automatique par profil |
| sysctl vm.swappiness | Vérifier/régler l'utilisation de la swap |

---
