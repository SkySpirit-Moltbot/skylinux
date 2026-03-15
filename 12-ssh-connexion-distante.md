# Leçon 12 : SSH et connexion distante

SSH (Secure Shell) est le protocole indispensable pour administrer des serveurs Linux à distance. Dans cette leçon, tu vas maîtriser SSH, les clés, le transfert de fichiers et les tunnels.

---

## 1. Comprendre SSH

### Qu'est-ce que SSH ?

SSH est un protocole **crypté** pour se connecter à distance à un serveur Linux. Il a remplacé les anciens protocoles insecure (telnet, rsh).

### Caractéristiques

- **Chiffrement** : Toutes les données sont chiffrées
- **Authentification** : Mot de passe ou clés RSA/ED25519
- **Tunnel** : Créer des tunnels sécurisés
- **Transfert** : Fichiers via SCP/SFTP

### Concepts clés

| Terme | Description |
|-------|-------------|
| **SSH** | Protocole |
| **ssh** | Client (commande) |
| **sshd** | Serveur (daemon) |
| **~/.ssh/** | Répertoire de config et clés |

---

## 2. Installation du serveur SSH

### Installer OpenSSH Server

```bash
# Debian/Ubuntu
sudo apt install openssh-server

# Démarrer le service
sudo systemctl start ssh

# Activer au boot
sudo systemctl enable ssh

# Voir le statut
sudo systemctl status ssh
```

### Configuration

```bash
# Fichier de configuration
sudo nano /etc/ssh/sshd_config

# Options importantes
Port 22                    # Changer le port
PermitRootLogin no         # Interdire root
PasswordAuthentication yes # Auth par mot de passe
PubkeyAuthentication yes  # Auth par clé
```

### Redémarrer après modification

```bash
sudo systemctl restart ssh
```

---

## 3. Connexion SSH de base

### Syntaxe simple

```bash
ssh utilisateur@adresse_ip
ssh user@192.168.1.100
ssh user@mondomaine.com
```

### Options courantes

```bash
# Port personnalisé
ssh -p 2222 user@serveur

# Avec clé spécifique
ssh -i ~/.ssh/ma_cle user@serveur

# Mode verbeux (debug)
ssh -v user@serveur

# Forward agent SSH
ssh -A user@serveur
```

### Premier accès

```bash
# Accepter la clé hôte (première connexion)
ssh user@serveur

# Réponses aux questions :
# "Are you sure you want to continue connecting (yes/no)?"
# Taper "yes"
```

---

## 4. Clés SSH - Configuration sécurisée

### Pourquoi utiliser des clés ?

| Mot de passe | Clé SSH |
|--------------|---------|
| Vulnérable aux attaques brute force | Impossibles à pirater |
| À retenir | Stockée localement |
| Transmission sur le réseau | Jamais transmise |

### Générer une clé SSH

```bash
# Clé ED25519 (recommandée - moderne et sécurisée)
ssh-keygen -t ed25519 -C "mon@email.com"

# Clé RSA (legacy)
ssh-keygen -t rsa -b 4096 -C "mon@email.com"

# Avec commentaire personnalisé
ssh-keygen -t ed25519 -C "serveur-maison"
```

### Questions lors de la génération

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase):      # Mot de passe pour protéger la clé
Enter same passphrase again: 
```

> ⚠️ **Conseil** : Utilise une passphrase pour sécuriser ta clé !

### Copier la clé sur le serveur

```bash
# Méthode automatique (recommandée)
ssh-copy-id user@serveur

# Methode manuelle
cat ~/.ssh/id_ed25519.pub | ssh user@serveur "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Ou avec ssh-id
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@serveur
```

### Connexion avec clé

```bash
ssh user@serveur
# Plus de mot de passe demandé !
```

### Agent SSH

```bash
# Démarrer l'agent
eval "$(ssh-agent -s)"

# Ajouter la clé
ssh-add ~/.ssh/id_ed25519

# Ajouter avec passphrase
ssh-add

# Lister les clés chargées
ssh-add -l

# Supprimer toutes les clés
ssh-add -D
```

---

## 5. Fichiers de configuration SSH

### ~/.ssh/config

```bash
nano ~/.ssh/config
```

Contenu :

```
# Serveur personnel
Host maison
    HostName 192.168.1.100
    User pi
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# Serveur cloud
Host cloud
    HostName mondomaine.com
    User admin
    Port 2222
    IdentityFile ~/.ssh/cloud_key

# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_ed25519
```

### Utiliser les alias

```bash
ssh maison        # Au lieu de ssh pi@192.168.1.100
scp fichier maison:/home/pi/
```

### Permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

---

## 6. Transfert de fichiers

### SCP - Copy

```bash
# Copier vers le serveur
scp fichier.txt user@serveur:/home/user/
scp -r dossier/ user@serveur:/home/user/

# Copier depuis le serveur
scp user@serveur:/home/user/fichier.txt ./
scp -r user@serveur:/home/user/dossier/ ./

# Options utiles
scp -P 2222 fichier.txt user@serveur:/dossier/  # Port
scp -C fichier.txt user@serveur:/dossier/      # Compression
scp -v fichier.txt user@serveur:/dossier/      # Verbeux
scp -p fichier.txt user@serveur:/dossier/      # Préserver dates
```

### SFTP - Transfert interactif

```bash
sftp user@serveur

# Commandes SFTP
ls              # Lister
cd dossier      # Changer dossier
pwd             # Dossier actuel
put fichier.txt # Envoyer
get fichier.txt # Télécharger
get -r dossier/ # Télécharger dossier
rm fichier      # Supprimer
mkdir dossier   # Créer dossier
exit            # Quitter
```

### RSYNC - Synchronisation

```bash
# Synchroniser local vers distant
rsync -avz dossier/ user@serveur:/home/user/backup/

# Synchroniser avec suppression
rsync -avz --delete dossier/ user@serveur:/backup/

# Exclure des fichiers
rsync -avz --exclude='*.log' dossier/ user@serveur:/backup/

#dry-run (simulation)
rsync -avzn dossier/ user@serveur:/backup/
```

---

## 7. Port Forwarding (Tunnel SSH)

### Local Port Forwarding

Accéder à un service du serveur comme si localement.

```bash
ssh -L [port_local]:[destination]:[port_destination] user@serveur
```

### Exemples pratiques

```bash
# Accéder au serveur web du serveur (port 80)
ssh -L 8080:localhost:80 user@serveur
# → http://localhost:8080 sur ta machine

# Accéder à MySQL sur le serveur
ssh -L 3306:localhost:3306 user@serveur

# Accéder à un service sur un autre serveur
ssh -L 9000:autre-serveur:80 user@serveur
```

### Remote Port Forwarding

Exposer un service local vers internet via le serveur.

```bash
ssh -R 8080:localhost:80 user@serveur
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Créer un proxy SOCKS
ssh -D 1080 user@serveur

# Configurer le navigateur
# SOCKS Proxy: localhost:1080
```

---

## 8. SSH Bastion (Jump Host)

### Se connecter via un serveur bastion

```bash
# Direct via le bastion
ssh -J user@bastion.com user@serveur-distant

# Avec clé spécifique
ssh -J -i ~/.ssh/bastion_key user@bastion.com user@serveur-interne

# Configuration dans ~/.ssh/config
Host serveur-distant
    HostName 192.168.1.50
    User admin
    ProxyJump user@bastion.com
```

---

## 9. Sécurité SSH

### Meilleures pratiques

```bash
# 1. Désactiver root login
# Dans /etc/ssh/sshd_config:
PermitRootLogin no

# 2. Changer le port par défaut
Port 2222

# 3. Utiliser only key authentication
PasswordAuthentication no

# 4. Limiter les utilisateurs
AllowUsers user1 user2

# 5. Fail2ban (anti-bruteforce)
sudo apt install fail2ban
```

### Authentification à deux facteurs

```bash
# Installer Google Authenticator
sudo apt install libpam-google-authenticator

# Configurer /etc/pam.d/sshd
# Ajouter: auth required pam_google_authenticator.so

# Activer dans /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods password,publickey
```

---

## 10. Exercices pratiques

### Exercice 1 : Configurer clé SSH
```bash
# Générer une clé
ssh-keygen -t ed25519 -C "mon-serveur"

# Copier sur le serveur
ssh-copy-id user@serveur

# Se connecter sans mot de passe
ssh user@serveur
```

### Exercice 2 : Tunnel vers MySQL
```bash
# Créer le tunnel
ssh -L 3306:localhost:3306 user@serveur

# Se connecter localement
mysql -h localhost -u root -p
```

### Exercice 3 : Transfert de backup
```bash
# Créer une archive
tar -czf backup.tar.gz ~/Documents/

# Transférer vers le serveur
scp backup.tar.gz user@serveur:/backup/

# Nettoyer local
rm backup.tar.gz
```

---

## 11. Tableau résumé

| Commande | Description |
|----------|-------------|
| `ssh user@serveur` | Connexion basique |
| `ssh-keygen` | Générer clé |
| `ssh-copy-id` | Copier clé |
| `scp` | Copier fichiers |
| `sftp` | Transfert interactif |
| `rsync` | Synchronisation |
| `ssh -L` | Port forwarding local |
| `ssh -R` | Port forwarding remote |
| `ssh -J` | Jump host |

---

Maîtrise SSH pour administrer tes serveurs comme un pro ! 🔐