# Leçon 42 : Partage de fichiers avec NFS

Dans cette leçon, tu vas découvrir comment partager des fichiers entre machines Linux sur un réseau local grâce à **NFS (Network File System)**. C'est l'équivalent Linux du partage Windows SMB, mais bien plus simple et efficace entre systèmes Unix.

---

## 1. Qu'est-ce que NFS ?

NFS est un protocole de partage de fichiers en réseau. Il permet à une machine (le **serveur**) d'exporter un dossier, et à d'autres machines (**clients**) de le monter localement comme s'il était sur leur propre disque.

**Cas d'usage courants :**

- Partager des fichiers entre serveurs dans un cluster
- Centraliser les données (photos, documents) sur un NAS Linux
- Partager du code et environnement de développement
- Stockage partagé pour machines sans disque (diskless)

> **Note :** NFS est conçu pour les réseaux locaux (LAN). Pour un accès depuis Internet, utilise VPN + NFS ou préfère un protocole sécurisé comme SSHFS/SFTP.

---

## 2. Côté serveur : exporter un dossier

### Étape 1 : Installer le serveur NFS

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install nfs-kernel-server

# Fedora / CentOS / RHEL
sudo dnf install nfs-utils
```

### Étape 2 : Créer le dossier à partager

```bash
sudo mkdir -p /srv/nfs/partage
sudo chown nobody:nogroup /srv/nfs/partage
sudo chmod 755 /srv/nfs/partage
```

### Étape 3 : Configurer les exports

Le fichier `/etc/exports` définit quels dossiers sont partagés et à qui :

```bash
sudo nano /etc/exports
```

Ajouter une ligne par partage :

```
# Format : dossier_client  IP_client(options)
# Exemple : partage accessible en lecture/écriture pour 192.168.1.0/24
/srv/nfs/partage   192.168.1.0/24(rw,sync,no_subtree_check)
```

**Options principales :**

- `rw` — lecture et écriture (par défaut : read-only)
- `ro` — lecture seule uniquement
- `sync` — écrit sur le disque avant de confirmer (plus sûr)
- `no_subtree_check` — évite des vérifications qui peuvent causer des lenteurs
- `no_root_squash` — root du client a les droits root sur le partage (⚠️ sécurité)

> **⚠️ Sécurité :** Par défaut, `root_squash` est activé : l'utilisateur root du client est converti en `nobody`. C'est bien pour la sécurité. N'utilise `no_root_squash` que dans un réseau de confiance.

### Étape 4 : Redémarrer le service

```bash
# Exporter les partages et redémarrer le service
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
```

### Vérifier les exports actifs

```bash
sudo exportfs -v
```

---

## 3. Côté client : monter le partage NFS

### Étape 1 : Installer le client NFS

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install nfs-common

# Fedora / CentOS / RHEL
sudo dnf install nfs-utils
```

### Étape 2 : Monter le partage manuellement

```bash
# Créer le point de montage local
sudo mkdir -p /mnt/nfs/partage

# Monter le partage NFS
sudo mount 192.168.1.100:/srv/nfs/partage /mnt/nfs/partage
```

Remplace `192.168.1.100` par l'adresse IP réelle de ton serveur NFS.

### Vérifier le montage

```bash
df -h | grep nfs
```

```bash
# Tester l'accès
ls -la /mnt/nfs/partage/
```

### Étape 3 : Montage automatique au boot (fstab)

Pour monter automatiquement au démarrage, ajoute une ligne dans `/etc/fstab` :

```bash
sudo nano /etc/fstab
```

```
# Ajouter cette ligne :
192.168.1.100:/srv/nfs/partage   /mnt/nfs/partage   nfs   defaults,_netdev   0   0
```

`_netdev` = attend que le réseau soit prêt avant de monter (important pour NFS).

---

## 4. Démonter un partage NFS

```bash
# Démonter le partage
sudo umount /mnt/nfs/partage

# Forcer si occupé (si des fichiers sont ouverts)
sudo umount -f /mnt/nfs/partage

# Lazy unmount (détache immédiatement, processus continuent)
sudo umount -l /mnt/nfs/partage
```

---

## 5. Commandes utiles

| Commande | Description |
|----------|-------------|
| `showmount -e localhost` | Lister les exports sur le serveur |
| `showmount -e 192.168.1.100` | Voir les partages NFS d'un serveur distant |
| `mount | grep nfs` | Voir tous les montages NFS actifs |
| `sudo exportfs -v` | Détails des exports actifs (serveur) |
| `sudo exportfs -ra` | Réappliquer tous les exports après modification |

---

## 6. Exercice pratique

**Objectif :** Partager un dossier entre deux machines sur ton réseau local.

**Sur la machine SERVEUR :**

1. Installe `nfs-kernel-server`
2. Crée le dossier `/srv/nfs/public`
3. Ajoute dans `/etc/exports` :
   `/srv/nfs/public   192.168.1.0/24(ro,sync,no_subtree_check)`
4. Redémarre le service : `sudo systemctl restart nfs-kernel-server`
5. Créer un fichier test : `echo "Salut depuis le serveur NFS" | sudo tee /srv/nfs/public/test.txt`

**Sur la machine CLIENT :**

1. Installe `nfs-common`
2. Monte le partage : `sudo mount 192.168.1.XX:/srv/nfs/public /mnt/nfs/public`
3. Vérifie : `cat /mnt/nfs/public/test.txt`
4. Ajoute-le au fstab pour un montage automatique
5. Nettoie : `sudo umount /mnt/nfs/public`

---

## 7. Résumé

| Concept | Récapitulatif |
|---------|---------------|
| NFS | Network File System — partage de fichiers via réseau local |
| Paquet serveur | `nfs-kernel-server` |
| Paquet client | `nfs-common` |
| Config serveur | `/etc/exports` |
| Montage manuel | `mount IPserveur:/dossier /point/montage` |
| Montage auto | Ligne dans `/etc/fstab` avec `_netdev` |
| Options courantes | `rw/ro`, `sync`, `no_subtree_check` |

NFS est un outil essentiel pour tout environnement Linux multi-machines. Simple, rapide et bien intégré — il remplace avantageusement les clés USB pour partager des fichiers entre serveurs !

---

*Dans la prochaine leçon, nous continuerons à explorer les outils système essentiels pour aller plus loin avec Linux.*
