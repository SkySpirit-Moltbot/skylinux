# Leçon 18 : Gestion des disques et partitions

Dans cette leçon, tu vas maîtriser la gestion des disques et partitions sous Linux : création de partitions, systèmes de fichiers, montage, et surveillance de l'espace disque.

---

## 1. Comprendre le stockage sous Linux

### Nomenclature des disques

| Périphérique | Description |
|--------------|-------------|
| `/dev/sda` | Premier disque SATA/SCSI |
| `/dev/sdb` | Deuxième disque |
| `/dev/nvme0n1` | Premier NVMe (SSD moderne) |
| `/dev/sda1` | Première partition du disque sda |
| `/dev/nvme0n1p1` | Première partition du NVMe |

### Types de partitions

| Type | Description |
|------|-------------|
| **MBR** | Ancien format, max 2To, 4 partitions primaires |
| **GPT** | Format moderne, tables<Guid, partitions illimitées |

---

## 2. Commandes de surveillance

### df - Espace disque

```bash
df -h                    # Format lisible (Ko, Mo, Go)
df -H                    # Format IEC (1000 au lieu de 1024)
df -T                    # Avec type de filesystem
df -i                    # Inodes au lieu de blocs
df -x tmpfs              # Exclure les tmpfs
df --output=source,size,used,avail,pcent  # Colonnes personnalisées

# Exemple de sortie
df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   45G   55G  45% /
/dev/sdb1       500G  200G  300G  40% /data
tmpfs           2.0G     0  2.0G   0% /dev/shm
```

### du - Espace utilisé

```bash
du -sh dossier/                  # Taille totale
du -h --max-depth=1             # Sous-dossiers 1 niveau
du -h --max-depth=2             # Sous-dossiers 2 niveaux
du -ah dossier/                  # Tous fichiers + cachés
du -sh */                        # Tous les sous-dossiers
du -h | sort -rh | head -10     # Top 10

# Exclure un pattern
du -h --exclude='*.log' dossier/
```

### lsblk - Blocs appareils

```bash
lsblk                    # Liste simple
lsblk -f                 # Avec filesystem
lsblk -m                 # Permissions et owner
lsblk -t                 # Format tableau
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT  # Colonnes personnalisées
```

---

## 3. Partitionner un disque

### fdisk - Outil classique

```bash
# Lister toutes les partitions
sudo fdisk -l
sudo fdisk -l /dev/sda

# Entrer dans le mode interactif
sudo fdisk /dev/sdb
```

**Commandes interactives fdisk :**

| Commande | Description |
|----------|-------------|
| `p` | Afficher la table de partitions |
| `n` | Nouvelle partition |
| `d` | Supprimer une partition |
| `t` | Changer le type de partition |
| `l` | Lister les types disponibles |
| `w` | Écrire et quitter |
| `q` | Quitter sans enregistrer |
| `m` | Aide |

### parted - Alternative moderne

```bash
# Mode interactif
sudo parted /dev/sdb

# Commandes non-interactives
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary ext4 0% 100%
sudo parted /dev/sdb mkpart primary linux-swap 80% 100%
sudo parted /dev/sdb rm 1
sudo parted /dev/sdb print
```

### gdisk - Pour GPT

```bash
sudo gdisk /dev/sdb
# Similaire à fdisk mais pour tables GPT
```

---

## 4. Systèmes de fichiers

### Créer un filesystem

```bash
# ext4 (le plus courant)
sudo mkfs.ext4 /dev/sdb1
sudo mkfs.ext4 -L "MonDisque" /dev/sdb1  # Avec label

# ext3
sudo mkfs.ext3 /dev/sdb1

# XFS (haute performance)
sudo mkfs.xfs /dev/sdb1

# Btrfs (moderne, copy-on-write)
sudo mkfs.btrfs /dev/sdb1

# VFAT (Windows)
sudo mkfs.vfat /dev/sdb1

# NTFS (，需 installer ntfs-3g)
sudo mkfs.ntfs /dev/sdb1

# Swap
sudo mkswap /dev/sda2
sudo swapon /dev/sda2
```

### Options de mkfs.ext4

```bash
# Paramètres avancés
sudo mkfs.ext4 -m 0 -b 4096 -E stride=32,stripe-width=64 /dev/sdb1

# -m 0 : Réserver 0% pour root (au lieu de 5%)
# -b 4096 : Taille de bloc
# -E : Paramètres RAID pour SSD
```

---

## 5. Monter et démonter

### Montage manuel

```bash
# Monter une partition
sudo mount /dev/sdb1 /mnt/data

# Monter en lecture seule
sudo mount -r /dev/sdb1 /mnt/backup

# Monter avec options
sudo mount -o defaults,noexec,nosuid /dev/sdb1 /mnt/apps

# Monter par UUID
sudo mount UUID="123-456" /mnt/data

# Monter par label
sudo mount LABEL="MonDisque" /mnt/data
```

### Options de montage courantes

| Option | Description |
|--------|-------------|
| `defaults` | rw, suid, dev, exec, auto, nouser, async |
| `ro` | Lecture seule |
| `rw` | Lecture/Écriture |
| `noexec` | Pas d'exécution de binaires |
| `nosuid` | Ignorer setuid/setgid |
| `nodev` | Pas de fichiers spéciaux |
| `nosymfollow` | Ne pas suivre les liens symboliques |
| `noatime` | Ne pas mettre à jour l'accès |
| `nodiratime` | Ne pas mettre à jour l'accès aux répertoires |
| `nofail` | Ne pas échouer si absent |

### Démonter

```bash
# Démonter proprement
sudo umount /mnt/data

# Forcer (peut causer des erreurs)
sudo umount -f /mnt/data

# Lazy unmount (quand pas occupé)
sudo umount -l /mnt/data

# Démonter tous les points de montage d'un périphérique
sudo umount -l /dev/sdb1
```

---

## 6. Configuration automatique (/etc/fstab)

### Format du fichier

```
# <périphérique>  <point de montage>  <type>  <options>         <dump>  <pass>
UUID=xxx          /data                ext4    defaults         0       2
/dev/sdb1         /backup              ext4    nofail,noatime   0       2
tmpfs             /tmp                 tmpfs   defaults         0       0
```

### Trouver UUID et type

```bash
# Lister tous les UUID
sudo blkid

# UUID d'un spécifique
sudo blkid /dev/sda1

# Vérifier le filesystem
sudo file -s /dev/sda1
```

### Options fstab courantes

| Option | Description |
|--------|-------------|
| `defaults` | rw, suid, dev, exec, auto, nouser, async |
| `nofail` | Ne pas bloquer le boot si absent |
| `noatime` | Performance améliorée |
| `nobootwait` | Attendre ou non le montage |

---

## 7. Swap

### Créer du swap

```bash
# Créer un fichier swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Ajouter au fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Commandes swap

```bash
swapon -s                  # Voir le swap actif
sudo swapon /swapfile     # Activer
sudo swapoff /swapfile   # Désactiver
```

---

## 8. Vérification et réparation

### fsck - Vérifier le filesystem

```bash
# Vérifier (NE JAMAIS sur mounted !)
sudo fsck /dev/sdb1

# Avec réparation automatique
sudo fsck -y /dev/sdb1

# Type spécifique
sudo fsck -t ext4 /dev/sdb1

# Forcer même si propre
sudo fsck -f /dev/sdb1
```

> ⚠️ **IMPORTANT** : Ne jamais exécuter fsck sur un filesystem monté !

### tune2fs - Paramètres ext

```bash
# Voir les paramètres
sudo tune2fs -l /dev/sda1

# Changer le label
sudo tune2fs -L "NouveauLabel" /dev/sda1

# Journaling (ajouter si manquant)
sudo tune2fs -O ^has_journal /dev/sda1  # Retirer
sudo tune2fs -O has_journal /dev/sda1    # Ajouter

# Fréquence de vérification
sudo tune2fs -c 30 /dev/sda1  # Tous les 30 mounts
sudo tune2fs -i 30d /dev/sda1 # Tous les 30 jours
```

---

## 9. Gestion LVM (Logical Volume Manager)

### Concepts

- **PV** : Physical Volume (disque physique)
- **VG** : Volume Group (regroupement de PV)
- **LV** : Logical Volume (partition logique)

### Commandes LVM

```bash
# Créer un PV
sudo pvcreate /dev/sdb1

# Créer un VG
sudo vgcreate mon_vg /dev/sdb1

# Créer un LV
sudo lvcreate -L 10G -n mon_lv mon_vg

# Formater le LV
sudo mkfs.ext4 /dev/mon_vg/mon_lv

# Agrandir le LV
sudo lvextend -L +5G /dev/mon_vg/mon_lv
sudo resize2fs /dev/mon_vg/mon_lv

# Réduire le LV (attention !)
sudo resize2fs /dev/mon_vg/mon_lv 5G
sudo lvreduce -L 5G /dev/mon_vg/mon_lv

# État
sudo pvs    # Physical volumes
sudo vgs    # Volume groups
sudo lvs    # Logical volumes
```

---

## 10. SSD et TRIM

### Activer TRIM

```bash
# Vérifier si actif
sudo hdparm -I /dev/sda | grep TRIM

# TRIM manuel
sudo fstrim /

# Activer discard dans fstab
/dev/sda1 / ext4 defaults,discard 0 1
```

---

## 11. Exercices pratiques

### Exercice 1 : Surveillance
```bash
# Voir l'utilisation
df -h

# Les plus gros dossiers
du -sh /* 2>/dev/null | sort -rh | head -10

# Espace inode
df -i
```

### Exercice 2 : Créer une partition
```bash
# Voir les disques
lsblk

# Partitionner (ATTENTION au bon disque !)
sudo fdisk /dev/sdb
# n (nouveau), p (primaire), 1, default, default, w

# Créer filesystem
sudo mkfs.ext4 /dev/sdb1

# Monter
sudo mkdir /mnt/backup
sudo mount /dev/sdb1 /mnt/backup
```

### Exercice 3 : Configuration fstab
```bash
# Trouver UUID
sudo blkid

# Éditer fstab
sudo nano /etc/fstab

# Ajouter ligne:
# UUID=xxx /mnt/data ext4 defaults,nofail 0 2
```

---

## 12. Tableau résumé

| Commande | Description |
|----------|-------------|
| `df -h` | Espace disque |
| `du -sh` | Taille dossiers |
| `lsblk` | Lister blocs |
| `fdisk` | Partitionner (MBR) |
| `parted` | Partitionner (GPT) |
| `mkfs` | Créer filesystem |
| `mount` | Monter |
| `umount` | Démonter |
| `blkid` | UUIDs |
| `fsck` | Vérifier |
| `swapon/swapoff` | Gérer swap |
| `pvs/vgs/lvs` | LVM |

---

Maîtrise la gestion des disques pour administrer Linux comme un pro ! 💾