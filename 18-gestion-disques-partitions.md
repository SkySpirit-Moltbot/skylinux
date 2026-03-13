# Leçon 18 : Gestion des disques et partitions

## Objectifs
- Comprendre comment Linux gère les disques et partitions
- Apprendre à utiliser les commandes de base pour gérer l'espace disque
- Savoir monter et démonter des systèmes de fichiers

## Introduction

Dans Linux, tout est fichier, y compris les disques et partitions. Ils sont accessibles via le répertoire spécial `/dev/`. Comprendre comment gérer l'espace disque est essentiel pour tout administrateur système.

## Les appareils de stockage dans /dev/

Les disques durs et SSD apparaissent dans `/dev/` :
- `/dev/sda` — Premier disque SATA/SCSI
- `/dev/sdb` — Deuxième disque
- `/dev/nvme0n1` — Premier NVMe
- `/dev/sda1` — Première partition du premier disque

## Commandes essentielles

### df - Espace disque utilisé

Affiche l'espace disque utilisé et disponible :

```bash
# Afficher l'espace disque en format lisible
df -h

# Afficher les inodes
df -i

# Afficher le type de fichiersystems
df -Th
```

Exemples de sortie :
```
Système de fichiers Taille Utilisé Dispo Utili% Monté sur
/dev/sda1              50G    12G    35G   26% /
/dev/sdb1             100G    45G    55G   45% /data
tmpfs                 2,0G       0  2,0G    0% /dev/shm
```

### du - Espace utilisé par les fichiers

Affiche l'espace disque utilisé par les fichiers et répertoires :

```bash
# Espace total du répertoire courant
du -sh .

# Espace de chaque sous-répertoire
du -h --max-depth=1

# Trier par taille
du -h /home | sort -rh

# Afficher uniquement le total
du -sh /var/log
```

### lsblk - Lister les blocs appareils

Affiche les périphériques de stockage :

```bash
# Afficher tous les périphériques
lsblk

# Avec informations supplémentaires
lsblk -f

# Format arbre
lsblk -t
```

### fdisk - Partitionner un disque

Outil classique pour gérer les partitions :

```bash
# Lister les partitions
sudo fdisk -l

# Entrer dans le mode interactif
sudo fdisk /dev/sdb
```

Commandes interactives fdisk :
- `p` — Afficher la table de partitions
- `n` — Créer une nouvelle partition
- `d` — Supprimer une partition
- `w` — Écrire et quitter
- `q` — Quitter sans enregistrer

### parted - Alternative moderne à fdisk

```bash
# Mode interactif
sudo parted /dev/sdb

# Commandes non-interactives
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary ext4 0% 100%
```

## Monter et démonter des systèmes de fichiers

### Montage manuel

```bash
# Monter une partition
sudo mount /dev/sdb1 /mnt/data

# Monter en lecture seule
sudo mount -r /dev/sdb1 /mnt/backup

# Monter avec des options spécifiques
sudo mount -o defaults,noexec /dev/sdb1 /mnt/apps
```

### Démonter un système de fichiers

```bash
# Démonter un point de montage
sudo umount /mnt/data

# Forcer le démontage
sudo umount -f /mnt/data

# Démonter paresseux (quand pas occupé)
sudo umount -l /mnt/data
```

### Le fichier /etc/fstab

Contient les montages automatiques au démarrage :

```
# Format : <périphérique> <point de montage> <type> <options> <dump> <pass>
UUID=12345678-1234-1234-1234-123456789abc /data ext4 defaults 0 2
/dev/sdb1               /backup    ext4    defaults 0 2
```

Pour trouver l'UUID d'une partition :
```bash
sudo blkid
```

## Créer un système de fichiers

```bash
# Format ext4
sudo mkfs.ext4 /dev/sdb1

# Format ext3
sudo mkfs.ext3 /dev/sdb1

# Format XFS
sudo mkfs.xfs /dev/sdb1

# Format VFAT
sudo mkfs.vfat /dev/sdb1
```

## Vérifier l'intégrité d'un système de fichiers

```bash
# Vérifier ext4 (NE JAMAIS faire sur mounted filesystem)
sudo fsck /dev/sdb1

# Avec réparation automatique
sudo fsck -y /dev/sdb1
```

## Exercices pratiques

### Exercice 1 : Explorer l'espace disque
1. Utilisez `df -h` pour voir l'utilisation actuelle
2. Identifiez quel disque contient la partition racine `/`
3. Notez l'espace disponible

### Exercice 2 : Analyser l'utilisation
1. Utilisez `du -sh /home` pour voir l'espace utilisé par votre répertoire personnel
2. Trouvez les 5 plus gros répertoires de votre système avec :
   ```bash
   du -h / | sort -rh | head -n 5
   ```

### Exercice 3 (avancé) : Créer une clé USB bootable
1. Insérez une clé USB et identifiez son périphérique avec `lsblk`
2. Créez une partition avec `fdisk` (attention à bien choisir le bon périphérique !)
3. Formatez-la en ext4 ou FAT32
4. Montez-la et copiez quelques fichiers

⚠️ **Attention** : Manipulez les disques avec précaution. Une erreur peut effacer vos données !

## Résumé

| Commande | Utilité |
|----------|---------|
| `df -h` | Afficher l'espace disque |
| `du -h` | Espace utilisé par les fichiers |
| `lsblk` | Lister les périphériques de stockage |
| `fdisk` | Gérer les partitions |
| `mount` | Monter un système de fichiers |
| `umount` | Démonter un système de fichiers |
| `mkfs` | Créer un système de fichiers |
| `blkid` | Afficher les UUID des partitions |

La gestion des disques est fondamentale. Always backup vos données avant de modifier les partitions !