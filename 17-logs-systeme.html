# Leçon 17 : Les logs système

Dans cette leçon, tu vas maîtriser les logs sous Linux. Les logs sont essentiels pour le dépannage, la sécurité et la surveillance système.

---

## 1. Introduction aux logs

### Qu'est-ce qu'un log ?

Un **log** (journal) est un fichier qui enregistre les événements du système. C'est indispensable pour :
- Diagnostiquer les problèmes
- Surveiller la sécurité
- Comprendre le comportement du système
- Auditer les activités

### Emplacement des logs

| Répertoire | Description |
|------------|-------------|
| `/var/log/` | Logs système principaux |
| `/var/log/syslog` | Messages système généraux |
| `/var/log/auth.log` | Authentification (Debian/Ubuntu) |
| `/var/log/secure` | Authentification (RHEL/CentOS) |
| `/var/log/kern.log` | Messages du noyau |
| `/var/log/dmesg` | Messages au démarrage |
| `/var/log/messages` | Messages généraux (RHEL) |

---

## 2. Commandes de base

### tail - Suivre les logs

```bash
# Dernières lignes
tail /var/log/syslog

# Suivre en temps réel
tail -f /var/log/syslog

# Avec nombre de lignes
tail -n 50 /var/log/syslog
tail -f -n 50 /var/log/syslog
```

### head - Début des logs

```bash
head /var/log/syslog
head -n 20 /var/log/syslog
```

### cat - Tout afficher

```bash
cat /var/log/syslog
```

### less - Naviguer

```bash
less /var/log/syslog
# Touches: /rechercher, n=suivant, p=précédent, q=quitter
```

---

## 3. grep et logs

### Rechercher dans les logs

```bash
# Rechercher un terme
grep "erreur" /var/log/syslog

# Insensible à la casse
grep -i "error" /var/log/syslog

# Afficher le contexte
grep -C 3 "erreur" /var/log/syslog

# Compter les occurrences
grep -c "failed" /var/log/auth.log
```

### Recherches avancées

```bash
# Expressions régulières
grep -E "error|warning|critical" /var/log/syslog

# Plusieurs fichiers
grep -r "motif" /var/log/

# Inverser (lignes sans)
grep -v "debug" /var/log/syslog
```

---

## 4. Journalctl - Le système de logs moderne

systemd utilise **journald** comme système de logs centralisé.

### Commandes de base

```bash
# Voir tous les logs
journalctl

# Logs d'aujourd'hui
journalctl --since today

# Période précise
journalctl --since "2024-01-01" --until "2024-01-02"

# Dernières entrées
journalctl -n 50
journalctl -n 100 --no-pager

# Suivre en temps réel
journalctl -f
```

### Filtrer par service

```bash
# Logs d'un service
journalctl -u nginx
journalctl -u ssh

# Logs depuis le démarrage
journalctl -b

# Logs du boot précédent
journalctl -b -1

# Priorité (0=emergency à 7=debug)
journalctl -p err
journalctl -p warning
```

### Options avancées

```bash
# Format lisible
journalctl --no-pager

# Format JSON
journalctl -o json

# Taille
journalctl --disk-usage

# Nettoyer
journalctl --vacuum-size=100M
journalctl --vacuum-time=2weeks
```

---

## 5. dmesg - Logs du noyau

### Commandes de base

```bash
# Tous les messages du noyau
dmesg

# Suivre en temps réel
dmesg -w

# Avec horodatage lisible
dmesg -T

# Filtrer par niveau
dmesg -l err
dmesg -l warn
dmesg -l info
```

### Rechercher

```bash
# Rechercher un terme
dmesg | grep -i error
dmesg | grep -i usb
dmesg | grep -i network
```

---

## 6. Logs d'authentification

### Fichiers clés

```bash
# Debian/Ubuntu
/var/log/auth.log

# RHEL/CentOS
/var/log/secure
```

### Recherches utiles

```bash
# Connexions réussies
grep "session opened" /var/log/auth.log

# Échecs de connexion
grep "Failed password" /var/log/auth.log

# Connexions SSH
grep "sshd" /var/log/auth.log

# Utilisation de sudo
grep "sudo" /var/log/auth.log

# Dernier utilisateur
last
lastlog
```

---

## 7. Logs applicatifs

### Apache/Nginx

```bash
# Apache
/var/log/apache2/access.log
/var/log/apache2/error.log

# Nginx
/var/log/nginx/access.log
/var/log/nginx/error.log
```

### MySQL/MariaDB

```bash
/var/log/mysql/error.log
/var/log/mysql/slow-queries.log
/var/log/mysql/general.log
```

### Autres services

```bash
# Docker
/var/log/docker.log
journalctl -u docker

# Fail2ban
/var/log/fail2ban.log

# Cron
/var/log/cron.log
```

---

## 8. Analyser les logs

### Compter et trier

```bash
# Compter les erreurs
grep -c "error" /var/log/syslog

# Compter par type
grep -oE "error|warning|notice" /var/log/syslog | sort | uniq -c | sort -rn

# Top 10 IPs qui accèdent au serveur
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10
```

### Créer un script de surveillance

```bash
#!/bin/bash

LOG="/var/log/syslog"
ALERTES=0

# Vérifier les erreurs récentes
ERRORS=$(tail -n 100 $LOG | grep -c -i "error")

if [ $ERRORS -gt 10 ]; then
    echo "ALERTE: $ERRORS erreurs dans les dernières 100 lignes"
    #Notifier (email, Slack, etc.)
fi
```

---

## 9. Logrotate - Gestion des logs

### Configuration

```bash
# Fichier de config principal
/etc/logrotate.conf

# Configuration par service
/etc/logrotate.d/nginx
```

### Exemple de configuration

```
/var/log/nginx/*.log {
    daily              # Rotation quotidienne
    missingok          # Pas d'erreur si absent
    rotate 14          # Garder 14 fichiers
    compress           # Compresser les anciens
    delaycompress      # Compresser le lendemain
    notifempty        # Ne pas créer si vide
    create 0640 www-data adm
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null
    endscript
}
```

### Commandes logrotate

```bash
# Tester sans exécuter
logrotate -d /etc/logrotate.conf

# Forcer la rotation
sudo logrotate -f /etc/logrotate.conf
```

---

## 10. Créer son propre système de log

### Script simple

```bash
#!/bin/bash

LOGFILE="/var/log/mon_script.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Démarrage du script" >> $LOGFILE

# Votre logique ici
echo "$(date '+%Y-%m-%d %H:%M:%S') - Opération terminée" >> $LOGFILE
```

### Logger avec syslog

```bash
# Envoyer vers syslog
logger -p user.info "Mon message d'info"
logger -p user.warn "Attention"
logger -p user.err "Erreur"

# Avec tag personnalisé
logger -t "MONAPP" -p user.info "Message"
```

---

## 11. Exercices pratiques

### Exercice 1 : Surveiller les erreurs
```bash
# Rechercher les erreurs dans syslog
grep -i error /var/log/syslog | tail -20

# Errors avec contexte
grep -B2 -A2 "error" /var/log/syslog | head -30
```

### Exercice 2 : Connexions SSH
```bash
# Voir les connexions SSH
grep "sshd" /var/log/auth.log | tail -20

# Compter les échecs
grep "Failed password" /var/log/auth.log | wc -l
```

### Exercice 3 : Surveillance temps réel
```bash
# Suivre les logs en direct
tail -f /var/log/syslog | grep -i error

# Avec journalctl
journalctl -f -u nginx
```

---

## 12. Résumé

| Commande | Description |
|----------|-------------|
| `tail -f` | Suivre en temps réel |
| `grep` | Rechercher |
| `journalctl` | Logs systemd |
| `dmesg` | Logs du noyau |
| `logrotate` | Rotation automatique |
| `logger` | Créer des logs |

---

Maîtrise les logs pour diagnose et sécuriser ton système ! 📋