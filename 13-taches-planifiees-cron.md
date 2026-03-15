# Leçon 13 : Tâches planifiées avec Cron

Cron est le planificateur de tâches de Linux. Dans cette leçon, tu vas maîtriser cron pour automatiser tes tâches.

---

## 1. Comprendre Cron

### Qu'est-ce que Cron ?

Cron est un **daemon** qui exécute des commandes à des moments précis. Il est indispensable pour :
- Sauvegardes automatiques
- Nettoyage de fichiers
- Scripts de maintenance
- Tâches récurrentes

### Le fichier Crontab

Chaque utilisateur a son propre fichier **crontab** contenant les tâches planifiées.

---

## 2. Commandes de base

```bash
crontab -l                # Lister les tâches
crontab -e                # Éditer les tâches
crontab -r                # Supprimer toutes les tâches
crontab -i                # Confirmation avant suppression
crontab -u utilisateur -l # Voir les tâches d'un autre utilisateur (root)
```

---

## 3. Format d'une tâche Cron

```
┌───────────── Minute (0 - 59)
│ ┌───────────── Heure (0 - 23)
│ │ ┌───────────── Jour du mois (1 - 31)
│ │ │ ┌───────────── Mois (1 - 12)
│ │ │ │ ┌───────────── Jour de la semaine (0 - 7)
│ │ │ │ │             (0 et 7 = dimanche)
│ │ │ │ │
* * * * * commande à exécuter
```

### Symboles spéciaux

| Symbole | Signification |
|---------|---------------|
| `*` | N'importe quelle valeur |
| `,` | Liste de valeurs (1,3,5) |
| `-` | Intervalle (1-5) |
| `/` | Intervalle régulier (*/15 = toutes les 15) |

---

## 4. Exemples pratiques

### Planifications courantes

| Expression | Signification |
|------------|---------------|
| `0 * * * *` | Chaque heure |
| `0 0 * * *` | Chaque jour à minuit |
| `0 9 * * 1-5` | Jour ouvrable à 9h |
| `0 9 * * *` | Chaque jour à 9h |
| `*/15 * * * *` | Toutes les 15 minutes |
| `*/5 * * * *` | Toutes les 5 minutes |
| `0 0 1 * *` | Premier du mois à minuit |
| `0 2 * * 0` | Chaque dimanche à 2h |
| `30 4 1,15 * *` | 1er et 15 du mois à 4h30 |

### Exemples concrets

```bash
# Sauvegarde quotidienne à 18h
0 18 * * * rsync -av ~/Documents/ /media/backup/

# Nettoyage des fichiers temporaires chaque semaine
0 3 * * 0 find /tmp -type f -mtime +7 -delete

# Surveillance du disque chaque matin à 7h
0 7 * * * df -h >> ~/disk_usage.log

# Redémarrer un service chaque nuit
0 4 * * * sudo systemctl restart nginx

# Script Python chaque heure
0 * * * * /usr/bin/python3 /home/user/script.py

# Vérification DNS chaque jour à 8h
0 8 * * * ping -c 1 google.com || echo "Pas de réseau" | mail -s "Alerte" user@email.com
```

---

## 5. Variables d'environnement dans Cron

### Problème courant

Cron utilise un **environnement minimal**. Tes variables ($PATH, $HOME) peuvent ne pas fonctionner.

### Solution

```bash
# Définir les variables dans la crontab
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/utilisateur

# Ensuite les tâches...
0 9 * * * /home/utilisateur/scripts/backup.sh
```

### Rediriger la sortie

```bash
# Ignorer la sortie
0 9 * * * /script.sh > /dev/null 2>&1

# Envoyer vers un log
0 9 * * * /script.sh >> /var/log/scripts.log 2>&1

# Envoyer par email (si configuré)
MAILTO="user@example.com"
0 9 * * * /script.sh
```

---

## 6. Système Cron

### Cron système (/etc/crontab)

```bash
sudo nano /etc/crontab
```

Format légèrement différent :
```
minute hour day month weekday user command
```

Exemple :
```
0 3 * * * root /usr/bin/backup.sh
```

### Répertoires spéciaux

| Répertoire | Fréquence |
|------------|------------|
| `/etc/cron.minutely` | Chaque minute |
| `/etc/cron.hourly` | Chaque heure |
| `/etc/cron.daily` | Chaque jour |
| `/etc/cron.weekly` | Chaque semaine |
| `/etc/cron.monthly` | Chaque mois |

---

## 7. Commandes at (tâches uniques)

Pour une exécution unique, utilise `at` :

```bash
# Planifier une tâche pour demain à 10h
echo "/script.sh" | at 10:00 tomorrow

# Planifier pour dans 2 heures
echo "/script.sh" | at now +2 hours

# Lister les tâches
atq

# Supprimer une tâche
atrm 1
```

---

## 8. anacron - pour ordinateurs non allumés

`anacron` exécute les tâches qui ont raté car l'ordinateur était éteint.

```bash
# Installer
sudo apt install anacron

# Fichier de config
sudo nano /etc/anacrontab
```

---

## 9. Exercices pratiques

### Exercice 1 : Test basique
```bash
crontab -e
# Ajouter:
* * * * * echo "$(date)" >> ~/cron_test.txt
# Attendre 1 minute, vérifier:
cat ~/cron_test.txt
```

### Exercice 2 : Backup automatique
```bash
crontab -e
# Ajouter (chaque jour à 20h):
0 20 * * * rsync -avz ~/Documents/ /media/backup/ >> ~/backup.log 2>&1
```

### Exercice 3 : Nettoyage automatique
```bash
crontab -e
# Chaque dimanche à 3h:
0 3 * * 0 find ~/.cache -type f -mtime +30 -delete
```

---

## 10. Tableau résumé

| Commande | Description |
|----------|-------------|
| `crontab -l` | Lister les tâches |
| `crontab -e` | Éditer les tâches |
| `crontab -r` | Supprimer tout |
| `at` | Tâche unique |

### Format rapide

| Raccourci | Équivalent |
|-----------|------------|
| `@yearly` | `0 0 1 1 *` |
| `@monthly` | `0 0 1 * *` |
| `@weekly` | `0 0 * * 0` |
| `@daily` | `0 0 * * *` |
| `@hourly` | `0 * * * *` |
| `@reboot` | Au démarrage |

---

Cron est ton meilleur ami pour l'automatisation ! Utilise-le sagesse. ⏰