# Leçon 55 : nproc, uname et hostname — Identifier le système

Trois commandes simples pour connaître les caractéristiques de ta machine.

## 1. nproc — Nombre de processeurs

```bash
# Nombre de cœurs disponibles
nproc
# Exemple : 4

# Utile pour make -j$(nproc) : compiler sur tous les cœurs
make -j$(nproc)
```

## 2. uname — Infos système

```bash
# Nom du noyau
uname
# → Linux

# Tout savoir d'un coup
uname -a
# → Linux molbot 6.1.0-rpi-2712 #1 SMP PREEMPT arm64 GNU/Linux

# Options détaillées
uname -s    # Nom du système (Linux)
uname -n    # Nom d'hôte (hostname)
uname -r    # Version du noyau (6.1.0)
uname -m    # Architecture (arm64, x86_64)
uname -p    # Type de processeur
uname -o    # Système d'exploitation (GNU/Linux)
```

## 3. hostname — Nom de la machine

```bash
# Afficher le nom d'hôte
hostname
# → molbot

# Afficher le nom complet (FQDN)
hostname -f

# Changer temporairement (root)
sudo hostname nouveau-nom

# Adresse IP associée au hostname
hostname -I
# → 192.168.1.119
```

## 4. Bonus : infos plus détaillées

```bash
# Version de la distribution
lsb_release -a
cat /etc/os-release

# Architecture détaillée
lscpu | head -10

# Mémoire
free -h

# Modèle du matériel (Raspberry Pi, VM, etc.)
cat /proc/device-tree/model 2>/dev/null
cat /sys/class/dmi/id/product_name 2>/dev/null
```

## 5. Exercices pratiques

1. **Identité** — Lance `uname -a` et identifie l'architecture de ta machine
2. **Cœurs** — Vérifie le nombre de cœurs avec `nproc`
3. **Hostname** — Affiche ton hostname et son adresse IP avec `hostname -I`
