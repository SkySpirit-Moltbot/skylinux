# Leçon 39 : LVM - Gestion des Volumes Logiques

Dans cette leçon, tu vas découvrir **LVM** (Logical Volume Manager), un système puissant de gestion des disques sous Linux. LVM te permet de créer, redimensionner et gérer des volumes logiques de manière flexible — sans avoir à repartitionner ton disque. C'est indispensable pour tout administrateur qui gère des serveurs ou des espaces de stockage évolutifs.

---

## 1. Pourquoi LVM ?

Avec les partitions classiques, tu rencontres vite des limitations :

- **Une partition pleine ?** Il faut repartitionner, formater, restaurer.
- **Besoin de plus d'espace sur /home ?** Tu dois modifier la structure du disque.
- **Plusieurs disques ?** Gérer chaque disque séparément devient complexe.

**LVM résout tout ça** en introduisant une couche d'abstraction entre les disques physiques et les systèmes de fichiers.

### Les concepts clés de LVM

```
┌─────────────────────────────────────────┐
│           Volume Logique (LV)           │
│         /home, /var, /data, etc.        │
├─────────────────────────────────────────┤
│        Groupe de Volumes (VG)            │
│    Regroupe plusieurs PV = un pool      │
├──────────────────┬──────────────────────┤
│  Disque Physique │  Disque Physique     │
│      (PV)        │       (PV)           │
│   /dev/sdb1      │    /dev/sdc1         │
└──────────────────┴──────────────────────┘
```

- **Physical Volume (PV)** : partition ou disque physique préparé pour LVM
- **Volume Group (VG)** : pool de stockage formé par un ou plusieurs PV
- **Logical Volume (LV)** : espace logique créé dans un VG, qu'on formate et monte

---

## 2. Créer et organiser avec LVM

### Préparer un disque physique (PV)

```bash
# Voir les disques disponibles
lsblk

# Créer une partition Linux (type 8e pour LVM)
sudo fdisk /dev/sdb
# Taper : n (nouvelle partition), p (primaire), 1, Entrée, Entrée, t, 8e, w

# Créer le Physical Volume
sudo pvcreate /dev/sdb1

# Vérifier
sudo pvs
sudo pvdisplay
```

### Créer un Volume Group (VG)

```bash
# Créer un VG avec un ou plusieurs PV
sudo vgcreate mon_vg /dev/sdb1

# Ajouter un autre disque au VG
sudo vgextend mon_vg /dev/sdc1

# Voir les VG
sudo vgs
sudo vgdisplay mon_vg
```

### Créer un Volume Logique (LV)

```bash
# Créer un LV de 10 Go dans le VG
sudo lvcreate -L 10G -n donnees mon_vg

# Ou créer un LV qui utilise tout l'espace disponible
sudo lvcreate -l 100%FREE -n donnees mon_vg

# Voir les LV
sudo lvs
sudo lvdisplay
```

### Formater et monter

```bash
# Formater en ext4
sudo mkfs.ext4 /dev/mon_vg/donnees

# Monter temporairement
sudo mkdir /mnt/donnees
sudo mount /dev/mon_vg/donnees /mnt/donnees

# Vérifier
df -h /mnt/donnees
```

### Montage automatique (fstab)

```bash
# Ajouter au fichier /etc/fstab
echo '/dev/mon_vg/donnees /mnt/donnees ext4 defaults 0 2' | sudo tee -a /etc/fstab

# OU utiliser l'UUID (plus fiable)
sudo blkid /dev/mon_vg/donnees
# Ajouter : UUID=<uuid> /mnt/donnees ext4 defaults 0 2
```

---

## 3. Redimensionner un volume logique

C'est **la force de LVM** : agrandir ou réduire un volume à chaud !

### Agrandir un LV (à chaud, sans démonter)

```bash
# 1. Vérifier l'espace disponible dans le VG
sudo vgs

# 2. Agrandir le LV de 5 Go supplémentaires
sudo lvextend -L +5G /dev/mon_vg/donnees

# 3. Agrandir le système de fichiers (très important !)
# Pour ext4 :
sudo resize2fs /dev/mon_vg/donnees

# Pour xfs (on ne peut qu'agrandir, pas réduire) :
sudo xfs_growfs /mnt/donnees

# 4. Vérifier
df -h /mnt/donnees
```

### Réduire un LV (nécessite de démonter)

```bash
# 1. Démonter
sudo umount /mnt/donnees

# 2. Vérifier le système de fichiers (important !)
sudo e2fsck -f /dev/mon_vg/donnees

# 3. Réduire le système de fichiers à 8 Go
sudo resize2fs /dev/mon_vg/donnees 8G

# 4. Réduire le LV
sudo lvreduce -L 8G /dev/mon_vg/donnees

# 5. Remonter
sudo mount /dev/mon_vg/donnees /mnt/donnees
```

> ⚠️ **Attention** : Réduire un volume peut causer une perte de données. Sauvegarde toujours avant !

---

## 4. Ajouter un nouveau disque à LVM

```bash
# 1. Préparer le nouveau disque
sudo pvcreate /dev/sdd1

# 2. L'ajouter au VG existant
sudo vgextend mon_vg /dev/sdd1

# 3. Utiliser l'espace pour agrandir un LV
sudo lvextend -L +20G /dev/mon_vg/donnees
sudo resize2fs /dev/mon_vg/donnees

# Vérifier
sudo pvs
sudo vgs
```

---

## 5. Supprimer un volume logique

```bash
# 1. Démonter
sudo umount /mnt/donnees

# 2. Supprimer le LV
sudo lvremove /dev/mon_vg/donnees
# Confirmer avec 'y'

# Supprimer le VG
sudo vgremove mon_vg

# Supprimer le PV
sudo pvremove /dev/sdb1
```

---

## 6. Snapshots LVM

LVM permet de créer des **snapshots** — des copies instantanées d'un volume à un instant T. Très utile pour les sauvegardes ou les tests.

```bash
# Créer un snapshot de 5 Go (doit être assez grand pour les modifications)
sudo lvcreate -L 5G -s -n snapshot_donnees /dev/mon_vg/donnees

# Monter le snapshot pour y accéder
sudo mkdir /mnt/snapshot
sudo mount /dev/mon_vg/snapshot_donnees /mnt/snapshot

# Une fois terminé, supprimer le snapshot
sudo umount /mnt/snapshot
sudo lvremove /dev/mon_vg/snapshot_donnees
```

---

## 7. Exemple concret : Migrer /home vers LVM

```bash
# 1. Créer un nouveau LV pour /home
sudo lvcreate -L 50G -n home mon_vg

# 2. Formater
sudo mkfs.ext4 /dev/mon_vg/home

# 3. Copier les données
sudo mkdir /mnt/newhome
sudo mount /dev/mon_vg/home /mnt/newhome
sudo rsync -av /home/ /mnt/newhome/

# 4. Modifier /etc/fstab pour pointer vers le nouveau volume
# Remplacer la ligne /home par :
# /dev/mon_vg/home /home ext4 defaults 0 2

# 5. Redémarrer ou remonter
sudo umount /home
sudo mount /home

# 6. Vérifier
df -h /home
```

---

## 8. Commandes essentielles à retenir

| Commande | Rôle |
|----------|------|
| `pvcreate /dev/sdX1` | Préparer une partition pour LVM |
| `pvs` | Lister les Physical Volumes |
| `vgcreate nom /dev/sdX1` | Créer un Volume Group |
| `vgs` | Lister les Volume Groups |
| `vgextend nom /dev/sdY1` | Ajouter un PV à un VG |
| `lvcreate -L 10G -n nom vg` | Créer un Logical Volume |
| `lvs` | Lister les Logical Volumes |
| `lvextend -L +5G /dev/vg/lv` | Agrandir un LV |
| `lvreduce -L 8G /dev/vg/lv` | Réduire un LV |
| `resize2fs /dev/vg/lv` | Ajuster le filesystem après resize |
| `lvremove /dev/vg/lv` | Supprimer un LV |
| `lvdisplay` | Détails complets d'un LV |

---

## 9. Exercice pratique

**But** : Créer un environnement LVM complet et manipuler les volumes.

```bash
# 1. Crée deux fichiers de 500 Mo pour simuler des disques
dd if=/dev/zero of=/tmp/disque1 bs=1M count=500 oflag=direct
dd if=/dev/zero of=/tmp/disque2 bs=1M count=500 oflag=direct

# 2. Configure les en loop devices
sudo losetup -fP /tmp/disque1
sudo losetup -fP /tmp/disque2
# Note les noms (ex: /dev/loop0, /dev/loop1)

# 3. Crée les PV (remplace sda1 par ton loop)
sudo pvcreate /dev/loop0
sudo pvcreate /dev/loop1

# 4. Crée un VG
sudo vgcreate mon_test_vg /dev/loop0

# 5. Ajoute le second disque au VG
sudo vgextend mon_test_vg /dev/loop1

# 6. Crée un LV de 300 Mo
sudo lvcreate -L 300M -n test_lv mon_test_vg

# 7. Formate et monte
sudo mkfs.ext4 /dev/mon_test_vg/test_lv
sudo mkdir /mnt/test_lvm
sudo mount /dev/mon_test_vg/test_lv /mnt/test_lvm

# 8. Vérifie l'espace
df -h /mnt/test_lvm

# 9. Agrandis de 100 Mo
sudo lvextend -L +100M /dev/mon_test_vg/test_lv
sudo resize2fs /dev/mon_test_vg/test_lv
df -h /mnt/test_lvm

# 10. Nettoie
sudo umount /mnt/test_lvm
sudo lvremove /dev/mon_test_vg/test_lv
sudo vgremove mon_test_vg
sudo pvremove /dev/loop0 /dev/loop1
sudo losetup -D
rm /tmp/disque1 /tmp/disque2
```

---

## Résumé

- **LVM** ajoute une couche d'abstraction entre les disques physiques et les systèmes de fichiers.
- **PV** (Physical Volume) = partition/disque préparé pour LVM.
- **VG** (Volume Group) = pool de stockage combinant plusieurs PV.
- **LV** (Logical Volume) = espace logique dans un VG, qu'on formate et monte.
- **lvextend** + **resize2fs** = agrandir un volume à chaud, sans interruption.
- **Snapshots** = copies instantanées idéales pour les sauvegardes.
- LVM est standard sur la plupart des distributions Linux serveur.

LVM te donne une flexibilité incomparable pour gérer ton stockage. Une fois habitué, tu ne reviendras plus aux partitions fixes !
