# Leçon 19 : Sauvegardes et restauration

Dans cette leçon, tu vas maîtriser toutes les stratégies et outils de sauvegarde sous Linux. La perte de données peut arriver à tout moment — une bonne sauvegarde peut tout sauver !

---

## 1. Stratégies de sauvegarde

### La règle 3-2-1

| Règle | Description |
|-------|-------------|
| **3 copies** | Données originales + 2 sauvegardes |
| **2 supports** | Disque différent, supportcloud |
| **1 hors site** | Copie géographique différente |

### Types de sauvegardes

| Type | Description | Avantage | Inconvénient |
|------|-------------|----------|--------------|
| **Complète** | Tout copier | Restaurer simple | Temps, espace |
| **Incrémentale** | Modifiés depuis dernière | Rapide, petit | Restauration longue |
| **Différentielle** | Modifiés depuis complète | Compromis | Moyen |
| **Mirror** | Clone exact | Simple | Risque d'effacement erreurs |

---

## 2. TAR - Archivage de base

### Créer des sauvegardes

```bash
# Archive gzip (rapide)
tar -czvf backup.tar.gz dossier/

# Archive bzip2 (meilleure compression)
tar -cjvf backup.tar.bz2 dossier/

# Archive xz (meilleure encore)
tar -cJvf backup.tar.xz dossier/

# Avec date automatique
tar -czvf backup-$(date +%Y%m%d).tar.gz dossier/

# Exclure des dossiers
tar -czvf backup.tar.gz /home/ \
    --exclude='*.log' \
    --exclude='.cache' \
    --exclude='node_modules'
```

### Lister le contenu

```bash
tar -tvf backup.tar.gz           # Détails
tar -tf backup.tar.gz            # Simplement noms
tar -tf backup.tar.gz | wc -l    # Compter fichiers
```

### Extraire/Restaurer

```bash
# Extraire tout
tar -xzvf backup.tar.gz
tar -xjf backup.tar.bz2
tar -xJf backup.tar.xz

# Extraire dans un dossier spécifique
tar -xzvf backup.tar.gz -C /tmp/restauration/

# Extraire un fichier spécifique
tar -xzvf backup.tar.gz -C /tmp chemin/fichier.txt

# Mode interactif
tar -xzvf backup.tar.gz --checkpoint=1
```

---

## 3. RSYNC - Synchronisation

### Commandes de base

```bash
# Sync locale
rsync -av source/ destination/

# Avec options courantes
rsync -avz source/ destination/    # z = compression
rsync -av --delete source/ dest/   # Supprimer si absent source
rsync -av --exclude='*.log' src/ dst/  # Exclure
rsync -av --exclude-from='exclusions.txt' src/ dst/

# dry-run (simulation)
rsync -avn source/ destination/

# Progress et stats
rsync -av --progress source/ destination/
rsync -av --stats source/ destination/
```

### RSYNC distant (SSH)

```bash
# Vers serveur distant
rsync -avz -e ssh dossier/ user@serveur:/backup/

# Depuis serveur distant
rsync -avz -e ssh user@serveur:/backup/ dossier-local/

# Port SSH personnalisé
rsync -avz -e 'ssh -p 2222' dossier/ user@serveur:/backup/
```

### Sauvegarde incrémentale

```bash
#!/bin/bash
# Script backup incrémental

BACKUP_DIR="/backup"
SOURCE="/home"
DATE=$(date +%Y%m%d)

# Première sauvegarde complète
if [ ! -d "$BACKUP_DIR/full" ]; then
    rsync -av $SOURCE/ $BACKUP_DIR/full/
fi

# Sauvegardes incrémentales
rsync -av --delete --link-dest=$BACKUP_DIR/full $SOURCE/ $BACKUP_DIR/incr-$DATE/

# Mettre à jour le lien "latest"
rm -f $BACKUP_DIR/latest
ln -s $BACKUP_DIR/incr-$DATE $BACKUP_DIR/latest
```

---

## 4. Restic - Backup moderne (recommandé)

### Installation

```bash
# Download depuis GitHub
sudo wget https://github.com/restic/restic/releases/latest/download/restic_linux_amd64 -O /usr/local/bin/restic
sudo chmod +x /usr/local/bin/restic

#Ou via package manager
sudo apt install restic
```

### Configuration initiale

```bash
# Initialiser un dépôt
restic -r /backup/myrepo init

# Avec mot de passe
restic -r /backup/myrepo init --password-command "echo monmotdepasse"

# Repository cloud (S3)
restic -r s3:s3.amazonaws.com/bucketname init
```

### Commandes Restic

```bash
# Sauvegarder
restic -r /backup/myrepo backup /home
restic -r /backup/myrepo backup /home --exclude='*.log'

# Lister les snapshots
restic -r /backup/myrepo snapshots

# Restaurer
restic -r /backup/myrepo restore latest --target /restoration/

# Restaurer fichier spécifique
restic -r /backup/myrepo restore latest --path /home/fichier.txt --target /tmp/

# Supprimer anciens snapshots (garde 7 jours)
restic -r /backup/myrepo forget --keep-daily 7 --prune

# Vérifier intégrité
restic -r /backup/myrepo check
```

---

## 5. Borg Backup

### Installation

```bash
sudo apt install borgbackup
```

### Utilisation

```bash
# Initialiser
borg init --encryption=repokey /backup/borg_repo

# Créer sauvegarde
borg create /backup/borg_repo::archive-$(date +%Y%m%d) /home

# Lister
borg list /backup/borg_repo

# Restaurer
borg extract /backup/borg_repo::archive-20240314 /restoration/

# Nettoyage (garde 7 quotidiens, 4 hebdomadaires)
borg prune /backup/borg_repo --keep-daily=7 --keep-weekly=4
```

---

## 6. Scripts de sauvegarde automatisés

### Script complet avec rotation

```bash
#!/bin/bash

# ========== Configuration ==========
SOURCE="/home"
DESTINATION="/backup"
RETENTION_JOURS=7
LOGFILE="/var/log/backup.log"

# ========== Fonctions ==========
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOGFILE
}

# ========== Début ==========
log "=== Début de la sauvegarde ==="

# Créer le dossier de destination
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$DESTINATION/backup-$DATE"
mkdir -p $BACKUP_PATH

# ========== Sauvegarde ==========
if rsync -av --delete \
    --exclude='.cache' \
    --exclude='.local/share/Trash' \
    --exclude='node_modules' \
    --exclude='*.log' \
    "$SOURCE/" "$BACKUP_PATH/" 2>&1 | tee -a $LOGFILE; then
    
    log "Sauvegarde terminée avec succès"
    
    # Créer lien symbolique latest
    rm -f "$DESTINATION/latest"
    ln -s "$BACKUP_PATH" "$DESTINATION/latest"
    
else
    log "ERREUR lors de la sauvegarde"
    exit 1
fi

# ========== Rotation ==========
log "Nettoyage des anciennes sauvegardes..."
find $DESTINATION -maxdepth 1 -type d -name "backup-*" -mtime +$RETENTION_JOURS -exec rm -rf {} \; 2>&1 | tee -a $LOGFILE

log "=== Sauvegarde terminée ==="
```

### Script avec notification Telegram

```bash
#!/bin/bash

# ... (code de backup) ...

if [ $? -eq 0 ]; then
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=✅ Backup terminé avec succès"
else
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=❌ ERREUR backup"
fi
```

---

## 7. Planification avec Cron

### Exemples cron

```bash
# Ajouter au crontab
crontab -e

# Sauvegarde quotidienne à 3h du matin
0 3 * * * /home/user/scripts/backup.sh

# Toutes les 6 heures
0 */6 * * * /home/user/scripts/backup.sh

# Tous les dimanches à 2h (complète)
0 2 * * 0 /home/user/scripts/backup-full.sh

# Tous les jours à midi (incrémentale)
0 12 * * * /home/user/scripts/backup-incr.sh
```

---

## 8. Restauration

### Depuis TAR

```bash
# Restaurer tout
tar -xzvf backup.tar.gz -C /

# Fichier spécifique
tar -xzvf backup.tar.gz -C /tmp home/user/fichier.txt

# Vérifier avant
tar -tzvf backup.tar.gz | grep fichier
```

### Depuis RSYNC

```bash
# Sens inverse !
rsync -av /backup/ /home/
```

### Depuis Restic

```bash
# Dernier snapshot
restic -r /backup/myrepo restore latest --target /restoration/

# Snapshot spécifique
restic -r /backup/myrepo restore <snapshot-id> --target /restoration/
```

---

## 9. Services Cloud

### rclone - Cloud sync

```bash
# Configurer
rclone config

# Sync vers cloud
rclone sync /local backup-remote:backup

# Lister remote
rclone listremotes

# Vérifier size
rclone size backup-remote:backup
```

### Backblaze, Wasabi, etc.

```bash
# Avec rclone
rclone sync /home wasabi:mon-backup

# Avec restic + S3
restic -r s3:s3.eu-central-003.backblazeb2.com/bucket backup /home
```

---

## 10. Checklist bonnes pratiques

- [ ] **Automatiser** — Cron ou systemd timer
- [ ] **Vérifier** — Tester restauration régulièrement
- [ ] **Chiffrer** — Données sensibles (GPG, VeraCrypt)
- [ ] **Hors site** — Copie cloud ou autre machine
- [ ] **Monitoring** — Alertes si échec
- [ ] **Rotation** — Supprimer anciens backups
- [ ] **Documenter** — Procédure de restauration
- [ ] **Tester** — Restoration complète trimestrielle

---

## 11. Tableau résumé

| Outil | Usage | Type |
|-------|-------|------|
| `tar` | Archives locales | Manuel |
| `rsync` | Sync incrémentale | Flexible |
| `restic` | Backup moderne | Automatisé |
| `borg` | Dédupliqué | Avancé |
| `rclone` | Cloud sync | Cloud |

---

Maîtrise les sauvegardes pour protéger tes données ! 💾