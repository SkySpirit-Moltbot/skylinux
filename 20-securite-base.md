# Leçon 20 : Sécurité de base sous Linux

La sécurité est un aspect fondamental de l'administration Linux. Dans cette leçon, tu vas maîtriser les commandes et bonnes pratiques essentielles pour protéger ton système.

---

## 1. Surveillance des utilisateurs

### Voir qui est connecté

```bash
# Liste simple des utilisateurs connectés
who

# Détails (idle, process, terminal)
w

# Dernières connexions
last

# Dernière connexion par utilisateur
last -5
lastlog

# Qui est actuellemnt connecté et depuis où
who -H
```

### Analyser les sessions

```bash
# Voir tous les processus d'un utilisateur
ps -u nom_utilisateur

# Tuer une session
pkill -KILL -u nom_utilisateur

# Voir l'activité récente
ac -p                    # Temps de connexion total par utilisateur
```

---

## 2. Gestion des mots de passe

### Commandes de base

```bash
# Changer son mot de passe
passwd

# Changer le mot de passe d'un utilisateur (root)
sudo passwd nom_utilisateur

# Changer avec date d'expiration
sudo passwd -e nom_utilisateur          # Exiger changement au prochain login
sudo passwd -n 30 nom_utilisateur       # Minimum 30 jours avant changement
sudo passwd -x 90 nom_utilisateur       # Maximum 90 jours
sudo passwd -w 7 nom_utilisateur        # Avertissement 7 jours avant expiration

# Verrouiller/déverrouiller
sudo passwd -l nom_utilisateur          # Verrouiller
sudo passwd -u nom_utilisateur          # Déverrouiller

# Statut du mot de passe
sudo passwd -S nom_utilisateur
```

### Politique de mots de passe (PAM)

```bash
# Installer libpam-pwquality
sudo apt install libpam-pwquality

# Configurer (/etc/security/pwquality.conf)
sudo nano /etc/security/pwquality.conf

# Paramètres recommandés:
# minlen = 12
# dcredit = -1 (au moins 1 chiffre)
# ucredit = -1 (au moins 1 majuscule)
# lcredit = -1 (au moins 1 minuscule)
# ocredit = -1 (au moins 1 caractère spécial)
```

---

## 3. Analyse des ports et connexions

### ss - Socket Statistics (moderne)

```bash
# Ports en écoute
ss -tuln
ss -tulnp

# Connexions établies
ss -tn
ss -tnp

# Connexions par état
ss -tan state established

# Statistiques
ss -s

# Filtrer par port
ss -tn sport = :22
ss -tn dport = :80
```

### netstat (legacy)

```bash
# Ports ouverts
netstat -tuln
netstat -tulnp

# Routes
netstat -rn

# Connexions actives
netstat -an
```

### Nmap - Scanner de ports

```bash
# Installer
sudo apt install nmap

# Scanner local
nmap localhost
nmap -sV localhost

# Scanner une IP
nmap 192.168.1.1

# Scanner un réseau
nmap 192.168.1.0/24

# Scan rapide
nmap -F 192.168.1.1
```

---

## 4. Pare-feu UFW

### Installation et activation

```bash
# Installer
sudo apt install ufw

# Statut
sudo ufw status
sudo ufw status numbered

# Activer/désactiver
sudo ufw enable
sudo ufw disable
```

### Règles de base

```bash
# Autoriser par port
sudo ufw allow 22          # SSH
sudo ufw allow 80/tcp       # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 53/udp      # DNS

# Bloquer
sudo ufw deny 23           # Telnet

# Supprimer règles
sudo ufw delete allow 22
sudo ufw delete deny 23

# Autoriser par service
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 'Apache Full'
```

### Règles avancées

```bash
# Autoriser depuis IP spécifique
sudo ufw allow from 192.168.1.100
sudo ufw allow from 192.168.1.0/24 to any port 22

# Autoriser subnet
sudo ufw allow from 10.0.0.0/8

# Limiter les tentatives (protection brute force)
sudo ufw limit ssh

# Ports spécifiques
sudo ufw allow 8000:9000/tcp
```

### Configuration par défaut

```bash
# Politique par défaut
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default allow routed
```

---

## 5. Permissions spéciales

### Les 3 bits spéciaux

| Bit | Description | Effet |
|-----|-------------|-------|
| **SetUID (4000)** | s au lieu de x | Exécuter avec droits owner |
| **SetGID (2000)** | s au lieu de x | Exécuter avec droits groupe |
| **Sticky Bit (1000)** | t | Sauvegarde protégé dans répertoire |

### Commandes

```bash
# Ajouter setuid
chmod u+s fichier
chmod 4755 fichier

# Ajouter setgid
chmod g+s repertoire
chmod 2755 repertoire

# Ajouter sticky bit
chmod +t /tmp
chmod 1777 /tmp

# Voir les fichiers setuid
sudo find / -perm -4000 2>/dev/null
sudo find / -perm -2000 2>/dev/null
```

### Exemples pratiques

```bash
# ping a besoin de setuid (pour accès réseau)
ls -l /bin/ping
# -rwsr-xr-x 1 root root ... /bin/ping

# Répertoire partagé avec sticky bit
ls -ld /tmp
# drwxrwxrwt 10 root root ... /tmp
```

---

## 6. Sécurisation SSH

### Configuration sécurisée

```bash
# Éditer la configuration
sudo nano /etc/ssh/sshd_config
```

Modifier ces lignes:

```bash
Port 2222                              # Changer le port
PermitRootLogin no                     # Pas de root
PubkeyAuthentication yes              # Clés uniquement
PasswordAuthentication no             # Pas de mot de passe
PermitEmptyPasswords no                # Pas de mot de passe vide
X11Forwarding no                       # Désactiver X11 si pas besoin
MaxAuthTries 3                         # Tentatives max
ClientAliveInterval 300               # Timeout
ClientAliveCountMax 2                 # Nombre de checks
```

### Générer des clés SSH

```bash
# Clé ED25519 (recommandée)
ssh-keygen -t ed25519 -C "mon@email.com"

# Clé RSA (legacy)
ssh-keygen -t rsa -b 4096 -C "mon@email.com"

# Avec passphrase (fortement recommandé)
# Entrez une passphrase forte quand demandé
```

### Déployer la clé

```bash
# Copie automatique
ssh-copy-id user@serveur

# Ajouter manuellement
cat ~/.ssh/id_ed25519.pub | ssh user@serveur "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

---

## 7. Analyse des logs de sécurité

### Fichiers de logs importants

| Fichier | Description |
|---------|-------------|
| `/var/log/auth.log` | Connexions, sudo |
| `/var/log/syslog` | Messages système |
| `/var/log/kern.log` | Messages du noyau |
| `/var/log/faillog` | Échecs de connexion |
| `/var/log/btmp` | Mauvaises connexions |

### Commandes de analyse

```bash
# Rechercher les échecs
grep "Failed" /var/log/auth.log
grep "Failed" /var/log/auth.log | tail -20

# Rechercher les succès
grep "Accepted" /var/log/auth.log

# Voir les sudo
sudo grep "COMMAND" /var/log/auth.log

# Surveiller en temps réel
sudo tail -f /var/log/auth.log

# Compter les tentatives
grep "Failed password" /var/log/auth.log | wc -l

# Voir qui a utilisé sudo
sudo grep "SESSION" /var/log/auth.log
```

### Utiliser journalctl

```bash
# Logs d'authentification
journalctl -u ssh

# Logs kernel
journalctl -k

#Dernières heures
journalctl --since "1 hour ago"

# Filtrer par priorité
journalctl -p err
```

---

## 8. Détection des intrusion basiques

### Signes d'alerte

```bash
# Fichiers créés récemment
sudo find / -mtime -1 -type f 2>/dev/null

# Fichiers avec setuid root
sudo find / -perm -4000 -type f 2>/dev/null

# Connexions étrange
ss -tnp

# Processus inhabituel
ps auxf

# Utilisateurs suspects
last | head -20
```

### Scripts de surveillance

```bash
#!/bin/bash
# script secu.sh

LOG="/var/log/securite.log"

echo "=== Vérification sécurité $(date) ===" >> $LOG

# Vérifier échecs de connexion
echo "Tentatives échouées:" >> $LOG
grep "Failed" /var/log/auth.log | tail -5 >> $LOG

# Vérifier nouveaux fichiers setuid
echo "Fichiers setuid:" >> $LOG
find / -perm -4000 2>/dev/null >> $LOG

# Vérifier utilisateurs connectés
echo "Utilisateurs:" >> $LOG
who >> $LOG

echo "---" >> $LOG
```

---

## 9. Fail2ban - Protection brute force

### Installation

```bash
sudo apt install fail2ban
```

### Configuration

```bash
# Copier config
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Éditer
sudo nano /etc/fail2ban/jail.local

# Paramètres essentiels
[bantime]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
port = ssh
```

### Commandes

```bash
# Statut
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Bannir/Débannir
sudo fail2ban-client set sshd banip 192.168.1.100
sudo fail2ban-client set sshd unbanip 192.168.1.100

# Redémarrer
sudo systemctl restart fail2ban
```

---

## 10. Checklist sécurité

- [ ] Modifier le port SSH par défaut
- [ ] Désactiver l'authentification root
- [ ] Utiliser clés SSH uniquement
- [ ] Configurer UFW (ports ouverts au minimum)
- [ ] Vérifier régulièrement les logs
- [ ] Installer fail2ban
- [ ] Mettre à jour le système régulièrement
- [ ] Vérifier les permissions setuid
- [ ]Surveiller les utilisateurs connectés
- [ ] Changer les mots de passe régulièrement

---

## 11. Tableau résumé

| Commande | Description |
|----------|-------------|
| `who/w` | Utilisateurs connectés |
| `passwd` | Gérer mots de passe |
| `ss/netstat` | Ports ouverts |
| `ufw` | Pare-feu |
| `chmod u+s` | SetUID |
| `chmod g+s` | SetGID |
| `chmod +t` | Sticky bit |
| `ssh-keygen` | Générer clé SSH |
| `grep auth.log` | Analyser sécurité |
| `fail2ban` | Protéger brute force |

---

Sécurise ton Linux ! 🔐