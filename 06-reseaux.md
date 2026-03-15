# Leçon 6 : Réseaux de base

Dans cette leçon, tu vas maîtriser les fondamentaux du réseau sous Linux : configuration IP, diagnostic, SSH, et transfert de fichiers.

---

## 1. Adresses IP

### IPv4 vs IPv6

| Type | Format | Exemple |
|------|--------|---------|
| **IPv4** | 4 nombres (0-255) | 192.168.1.100 |
| **IPv6** | 8 groupes hexadécimaux | 2001:0db8::1 |

### IP publique vs privée

- **IP publique** : Adresse visible sur Internet (attribuée par le FAI)
- **IP privée** : Adresse locale (192.168.x.x, 10.x.x.x, 172.16-31.x.x)

---

## 2. Commandes de configuration IP

### Voir les adresses IP

```bash
ip addr                 # Méthode moderne
ip addr show eth0      # Une interface spécifique
ip -4 addr             # IPv4 seulement
ip -6 addr             # IPv6 seulement

# Méthode classique (deprecated mais encore là)
ifconfig
ifconfig -a
```

### Paramètres d'une interface

```bash
ip link show           # Liste des interfaces
ip link set eth0 up   # Activer interface
ip link set eth0 down # Désactiver

# Ajouter une IP
ip addr add 192.168.1.100/24 dev eth0

# Supprimer une IP
ip addr del 192.168.1.100/24 dev eth0
```

### Table de routage

```bash
ip route               # Routes actuelles
ip route show
ip route add default via 192.168.1.1  # Passerelle par défaut
```

---

## 3. Diagnostic réseau

### Ping - Tester la connectivité

```bash
ping google.com              # Ping infini
ping -c 4 google.com         # 4 pings seulement
ping -i 0.2 google.com       # Intervalle de 0.2s
ping -w 5 google.com         # Timeout 5 secondes

# Types de ping
ping -4 google.com           # IPv4 seulement
ping -6 google.com           # IPv6 seulement
```

### Traceroute - Chemin jusqu'à la destination

```bash
traceroute google.com        # Linux (utilise UDP)
traceroute -I google.com    # ICMP
traceroute -n google.com    # Sans résolution DNS
mtr google.com               # Ping + traceroute en temps réel
```

### Connexions réseau

```bash
# Commandes modernes (ss)
ss -tuln                   # TCP/UDP en écoute
ss -tuln -p                # Avec processus
ss -tan                    # Toutes connexions TCP
ss -tnp | grep ESTAB       # Connexions établies

# Commandes classiques (net-tools)
netstat -tuln              # Ports en écoute
netstat -rn                # Table de routage
netstat -i                 # Stats interfaces
```

### DNS

```bash
# Serveurs DNS utilisés
cat /etc/resolv.conf
resolvectl status

# Tester DNS
nslookup google.com
dig google.com
host google.com
```

### IP publique

```bash
curl ifconfig.me
curl icanhazip.com
wget -qO- ifconfig.me
```

---

## 4. Configuration réseau

### Fichiers de configuration (Debian/Ubuntu)

```bash
# Configuration interfaces
sudo nano /etc/network/interfaces

# Configuration DNS
sudo nano /etc/resolv.conf
```

### Exemple /etc/network/interfaces

```
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

### Redémarrer le réseau

```bash
sudo systemctl restart networking
# ou
sudo /etc/init.d/networking restart
```

---

## 5. Le fichier /etc/hosts

Le fichier hosts permet de résoudre les noms localement.

```bash
sudo nano /etc/hosts
```

Contenu :

```
127.0.0.1       localhost
127.0.1.1       raspberrypi

# Cartes alias
192.168.1.1     mon-routeur.local
192.168.1.10    serveur.local
192.168.1.20    nas.local

# Bloquer un site
127.0.0.1       facebook.com
127.0.0.1       www.facebook.com
```

---

## 6. SSH - Connexion à distance

### Installer le serveur

```bash
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

### Se connecter

```bash
ssh utilisateur@adresse_ip
ssh -p 2222 utilisateur@ip    # Port personnalisé
ssh -i ~/.ssh/cle_privee user@ip  # Avec clé SSH
```

### Sécurisation SSH

```bash
# Modifier le port (dans /etc/ssh/sshd_config)
sudo nano /etc/ssh/sshd_config
# Changer "Port 22" en "Port 2222"

# Redémarrer SSH
sudo systemctl restart ssh
```

### Clés SSH

```bash
# Générer une clé
ssh-keygen -t ed25519 -C "mon@email.com"

# Copier la clé sur le serveur
ssh-copy-id utilisateur@serveur

# Ou manuellement
cat ~/.ssh/id_ed25519.pub | ssh user@serveur "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

---

## 7. Transfert de fichiers

### SCP - Copie sécurisée

```bash
# Copier vers le serveur
scp fichier.txt user@serveur:/home/user/
scp -r dossier/ user@serveur:/home/user/

# Copier depuis le serveur
scp user@serveur:/home/user/fichier.txt ./

# Options utiles
scp -P 2222 fichier.txt user@serveur:/dossier/  # Port
scp -v fichier.txt user@serveur:/dossier/       # Verbeux
scp -C fichier.txt user@serveur:/dossier/       # Compression
```

### SFTP - Transfert interactif

```bash
sftp user@serveur
# Commandes: ls, cd, put, get, rm, mkdir, etc.
```

### RSYNC - Synchronisation

```bash
# Synchroniser un dossier
rsync -av dossier/ user@serveur:/home/user/backup/

# Synchronisation avec compression et suppression
rsync -avz --delete dossier/ user@serveur:/home/user/backup/

# Exclure des fichiers
rsync -av --exclude='*.log' dossier/ user@serveur:/backup/
```

---

## 8. Commandes firewall (UFW)

### UFW (Uncomplicated Firewall)

```bash
# Activer
sudo ufw enable

# Désactiver
sudo ufw disable

# Statut
sudo ufw status

# Autoriser SSH
sudo ufw allow ssh
sudo ufw allow 22/tcp

# Autoriser un port
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8080/tcp

# Bloquer
sudo ufw deny 80/tcp

# Supprimer une règle
sudo ufw delete allow 80/tcp
```

---

## 9. Exercices pratiques

### Exercice 1 : Vérifier la connectivité
```bash
ip addr
ping -c 3 8.8.8.8
traceroute google.com
```

### Exercice 2 : Configurer une IP statique
```bash
sudo nano /etc/network/interfaces
# Ajouter la configuration statique
sudo systemctl restart networking
```

### Exercice 3 : Transférer un fichier
```bash
# Créer un fichier test
echo "Test" > test.txt
# Le copier sur le serveur
scp test.txt user@serveur:/tmp/
```

---

## 10. Tableau résumé

| Commande | Description |
|----------|-------------|
| `ip addr` | Voir les IPs |
| `ping` | Tester connectivité |
| `traceroute` | Chemin jusqu'au serveur |
| `ss` | Connexions réseau |
| `nslookup/dig` | Requêtes DNS |
| `ssh` | Connexion à distance |
| `scp` | Copier via SSH |
| `sftp` | Transfert interactif |
| `rsync` | Synchronisation |
| `ufw` | Firewall |

---

Maîtrise ces commandes pour administrer le réseau sous Linux ! 🌐