# Leçon 40 : Les minuteurs systemd (timers)

Dans cette leçon, tu vas découvrir les **minuteurs systemd** (systemd timers), une alternative moderne et puissante à cron pour planifier des tâches. Intégrés à systemd, ils offrent plus de fonctionnalités : suivi dans journalctl, activation à chaud, support des événements système, et bien plus.

---

## 1. Pourquoi passer aux minuteurs systemd ?

**cron** fait le job depuis des décennies. Mais il a ses limites :
- Pas de log natif (tout va dans `cron` ou `syslog`)
- Pas de dépendances entre tâches
- Pas de reprise automatique après veille/hibernation
- Difficile à déboguer

**systemd timers** résolvent tout ça :
- ✅ Logs centralisés dans `journalctl`
- ✅ Démon au repos jusqu'au déclenchement (moins de ressources)
- ✅ Reprennent après une veille/hibernation
- ✅ Contrôle fin : max retries, randomised delay, etc.

---

## 2. Le principe : deux fichiers unit

Un minuteur systemd fonctionne toujours par **paire** :

```
tache.service   → Le script/la commande à exécuter
tache.timer     → Le déclencheur (quand et comment)
```

```
┌──────────────────────────────────────────────┐
│  tache.timer (minuteur)                     │
│    └─ active → déclenche → tache.service    │
│                                              │
│  tache.service (service)                    │
│    └─ exécute → ta commande/script          │
└──────────────────────────────────────────────┘
```

---

## 3. Créer un minuteur simple

### Étape 1 : Créer le service

```bash
sudo nano /etc/systemd/system/ma-tache.service
```

```ini
[Unit]
Description=Ma première tâche planifiée

[Service]
Type=oneshot
ExecStart=/home/user/scripts/backup.sh
```

`Type=oneshot` = le service s'exécute une fois et se termine.

### Étape 2 : Créer le minuteur

```bash
sudo nano /etc/systemd/system/ma-tache.timer
```

```ini
[Unit]
Description=Mon minuteur quotidien

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

**Explications des options :**
- `OnCalendar=daily` → s'exécute une fois par jour (à minuit)
- `Persistent=true` → rattrape les exécutions manquées si le PC était éteint

### Étape 3 : Activer et démarrer

```bash
# Recharger systemd pour voir les nouvelles unités
sudo systemctl daemon-reload

# Activer le minuteur (démarre au boot)
sudo systemctl enable ma-tache.timer

# Démarrer immédiatement
sudo systemctl start ma-tache.timer

# Vérifier que le minuteur est actif
sudo systemctl status ma-tache.timer
```

---

## 4. Les calendriers disponibles

### Formats courants

```ini
OnCalendar=daily        # Une fois par jour à minuit
OnCalendar=hourly      # Toutes les heures
OnCalendar=minutely    # Chaque minute
OnCalendar=weekly      # Une fois par semaine

OnCalendar=*-*-* 04:00:00     # Chaque jour à 4h du matin
OnCalendar=*-*-01 00:00:00   # Premier du mois à minuit
OnCalendar=Mon *-*-* 09:00:00 # Chaque lundi à 9h
OnCalendar=*-*-25 12:00:00    # Le 25 du mois à midi
OnCalendar=Sat,Sun *-*-* 10:00:00  # Weekends à 10h
```

### Syntaxe étendue

```ini
OnCalendar=*-*-* *:00:00           # Toutes les heures pile
OnCalendar=*-*-* *:00/15:00        # Toutes les 15 minutes
OnCalendar=*-*-03..09 18:00:00     # Du 3 au 9 du mois à 18h
OnCalendar=hourly::00               # Toutes les heures
OnCalendar=*:0/5                   # Toutes les 5 minutes
```

### Vérifier les calendriers

```bash
# Voir quand un calendrier sera déclenché
systemd-analyze calendar "daily"
systemd-analyze calendar "Mon *-*-* 09:00:00"
```

---

## 5. Minuteur avec intervalle (au lieu de calendrier)

```ini
[Timer]
# Exécute 1h après le démarrage, puis toutes les 24h
OnBootSec=1h
OnUnitActiveSec=24h
```

```
OnBootSec=1h      → 1h après le démarrage
OnUnitActiveSec=24h  → puis toutes les 24h après la dernière exécution
```

```ini
[Timer]
# Exécute 5 minutes après le démarrage
OnBootSec=5min
# Puis toutes les 12 heures
OnUnitActiveSec=12h
```

---

## 6. Débogage et surveillance

### Voir les minuteurs actifs

```bash
# Lister tous les minuteurs
systemctl list-timers --all

# Résultat :
NEXT                         LEFT          LAST                         PASSED       UNIT                    ACTIVATES
lun. 2026-03-30 09:00:00 CET  42min gauche  dim. 2026-03-29 09:00:00 CET  23h ago   mon-backup.timer        mon-backup.service
```

### Voir les logs d'un service

```bash
# Logs du service
sudo journalctl -u ma-tache.service

# Logs du minuteur
sudo journalctl -u ma-tache.timer

# Suivre en temps réel
sudo journalctl -f -u ma-tache.service
```

### Exécuter manuellement

```bash
# Lancer le service maintenant (sans attendre le minuteur)
sudo systemctl start ma-tache.service

# Forcer le minuteur à s'exécuter maintenant
sudo systemctl start ma-tache.timer
```

---

## 7. Exemple complet : backup automatique

### Script de backup

```bash
mkdir -p ~/scripts
nano ~/scripts/backup.sh
```

```bash
#!/bin/bash
# backup.sh - Backup quotidien du home

DATE=$(date +%Y-%m-%d)
BACKUP_DIR=/home/user/backups
SOURCE=/home/user/documents

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup-$DATE.tar.gz" "$SOURCE"

# Garder que les 7 derniers backups
ls -t "$BACKUP_DIR"/backup-*.tar.gz | tail -n +8 | xargs rm -f 2>/dev/null

echo "$(date) : Backup effectué avec succès" >> /var/log/backup.log
```

```bash
chmod +x ~/scripts/backup.sh
```

### Service

```bash
sudo nano /etc/systemd/system/backup.service
```

```ini
[Unit]
Description=Backup quotidien du répertoire documents
After=network.target

[Service]
Type=oneshot
ExecStart=/home/user/scripts/backup.sh
User=user
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Minuteur (quotidien à 3h du matin)

```bash
sudo nano /etc/systemd/system/backup.timer
```

```ini
[Unit]
Description=Minuteur de backup quotidien

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=30min

[Install]
WantedBy=timers.target
```

`RandomizedDelaySec=30min` = ajoute un délai aléatoire jusqu'à 30 min pour éviter que tous les minuteurs s'exécutent en même temps.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
```

---

## 8. Gestion avancée : avec état (persistant)

### Service de type "notify" (plus complexe)

Pour un script qui surveille un processus :

```ini
[Unit]
Description=Monitor de surveillance

[Service]
Type=notify
ExecStart=/home/user/scripts/monitor.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Minuteur avec contraintes

```ini
[Unit]
Description=Mission critique

[Timer]
# S'exécute toutes les 6h
OnUnitActiveSec=6h
# Ne s'exécute PAS si sur batterie (laptop)
ConditionACPower=true
# Décalage aléatoire max 5 min pour éviter les conflits
RandomizedDelaySec=5min

[Install]
WantedBy=timers.target
```

---

## 9. Comparatif cron vs systemd timers

| Fonctionnalité | cron | systemd timers |
|---|---|---|
| Configuration | `crontab -e` | Fichiers `.service` + `.timer` dans `/etc/systemd/system/` |
| Logs | Fichier externe (cron, syslog) | `journalctl -u unit` |
| Reprise après veille | ❌ | ✅ (avec `Persistent=true`) |
| Décalage aléatoire | ❌ | ✅ (`RandomizedDelaySec`) |
| Débogage | Difficile | Facile (`systemctl status`) |
| Dépendances | Manuelles (dans le script) | Via `[Unit]` directives |
| Activation par événement | ❌ | ✅ (via `OnCalendar` + `OnBootSec`) |

---

## 10. Commandes de référence

```bash
# Recharger après modification
sudo systemctl daemon-reload

# Activer (au démarrage)
sudo systemctl enable unit.timer

# Démarrer maintenant
sudo systemctl start unit.timer

# Arrêter
sudo systemctl stop unit.timer

# Désactiver
sudo systemctl disable unit.timer

# Voir le statut
systemctl status unit.timer

# Lister les minuteurs actifs
systemctl list-timers --all

# Voir les prochaines exécutions
systemctl list-timers --all --no-pager

# Logs
journalctl -u unit.service
journalctl -u unit.timer -f

# Tester le service seul
sudo systemctl start unit.service

# Vérifier la validité d'un calendrier
systemd-analyze calendar "*-*-* 03:00:00"
```

---

## 11. Exercice pratique

**Objectif :** Créer un minuteur qui affiche un message dans les logs toutes les 5 minutes.

**Étape 1 : Crée le script**

```bash
mkdir -p ~/scripts
nano ~/scripts/log-message.sh
```

```bash
#!/bin/bash
echo "$(date) : Le minuteur fonctionne ! ID du système : $(hostname)"
```

```bash
chmod +x ~/scripts/log-message.sh
```

**Étape 2 : Crée le service**

```bash
sudo nano /etc/systemd/system/log-message.service
```

```ini
[Unit]
Description=Message de test pour minuteur systemd

[Service]
Type=oneshot
ExecStart=/home/user/scripts/log-message.sh
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Étape 3 : Crée le minuteur (toutes les 5 minutes)**

```bash
sudo nano /etc/systemd/system/log-message.timer
```

```ini
[Unit]
Description=Minuteur de test - toutes les 5 minutes

[Timer]
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target
```

**Étape 4 : Active et vérifie**

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now log-message.timer
sudo systemctl status log-message.timer
```

**Étape 5 : Vérifie les logs**

```bash
journalctl -u log-message.service -f
# (attends 5 minutes ou force l'exécution)
sudo systemctl start log-message.service
journalctl -u log-message.service --no-pager
```

**Étape 6 : Nettoie (une fois l'exercice terminé)**

```bash
sudo systemctl stop log-message.timer
sudo systemctl disable log-message.timer
sudo rm /etc/systemd/system/log-message.timer
sudo rm /etc/systemd/system/log-message.service
sudo systemctl daemon-reload
```

✅ Tu sais maintenant créer et gérer des minuteurs systemd !

---

## Résumé

| Concept | Description |
|---------|-------------|
| `.service` | Définit la commande à exécuter (`ExecStart`) |
| `.timer` | Définit QUAND exécuter (`OnCalendar`, `OnBootSec`) |
| `OnCalendar` | Planification par calendrier (daily, hourly, date précise) |
| `OnBootSec` / `OnUnitActiveSec` | Planification par intervalle depuis boot/dernière exécution |
| `Persistent=true` | Rattrape les exécutions manquées |
| `RandomizedDelaySec` | Décalage aléatoire pour espacer les tâches |
| `systemctl list-timers` | Voir tous les minuteurs et prochaines exécutions |
| `journalctl -u unit` | Voir les logs d'un service |

**La règle d'or :** Si tu utilises déjà cron, les minuteurs systemd valent le détour pour les tâches critiques ou sur laptop (veille/hibernation). Pour les tâches simples, cron reste très bien.

---

*Dans la prochaine leçon, nous continuerons à explorer les outils système essentiels pour aller plus loin avec Linux.*
