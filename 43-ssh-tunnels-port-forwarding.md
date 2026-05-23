# Leçon 43 : SSH - Tunnels et Port Forwarding

Dans cette leçon, tu vas découvrir comment créer des **tunnels SSH** pour sécuriser tes connexions réseau. Le port forwarding te permet d'accéder à des services distants comme si ils tournaient en local — un outil indispensable pour administrer des serveurs et accéder à des services protégés.

---

## 1. Pourquoi créer un tunnel SSH ?

Par défaut, beaucoup de services (bases de données, interfaces web) écoute uniquement en **localhost** pour des raisons de sécurité. SSH te permet de créer un tunnel chiffré pour y accéder à distance.

### Cas d'usage courants

- Accéder à une interface web d'un serveur qui n'écoute que localement
- Se connecter à une base de données MySQL/PostgreSQL distante
- Contourner un pare-feu restrictif
- Sécuriser une connexion non chiffrée (VNC, HTTP)

---

## 2. Les trois types de tunnels

### 2.1. Tunnel local (-L) : accéder à un service distant depuis ta machine

C'est le plus courant. Tu rediriges un port de **ta machine locale** vers un service sur la **machine distante**.

```bash
# Syntaxe
ssh -L [port_local]:localhost:[port_distant] user@serveur

# Exemple : accéder à une interface web distante sur le port 80
ssh -L 8080:localhost:80 user@serveur-distant

# Maintenant, ouvre http://localhost:8080 sur ta machine
```

Dans cet exemple :
- `8080` = le port sur **ta machine locale** (choisis un port libre)
- `localhost` = le serveur distant vu de lui-même
- `80` = le port du service sur le serveur distant

### 2.2. Tunnel inverse (-R) : exposer un service local vers l'extérieur

Tu rends un port de **ta machine** accessible depuis le **serveur distant**. Pratique pour accéder à ton réseau local depuis l'extérieur.

```bash
# Syntaxe
ssh -R [port_distant]:localhost:[port_local] user@serveur

# Exemple : exposer ton serveur web local (port 3000) sur le port 8080 du serveur distant
ssh -R 8080:localhost:3000 user@serveur-distant

# Depuis le serveur distant : curl http://localhost:8080
```

### 2.3. Tunnel dynamique (-D) : proxy SOCKS

Tu crées un **proxy SOCKS** qui fait passer tout ton trafic par le serveur SSH. C'est comme un VPN simple.

```bash
# Syntaxe
ssh -D [port_local] user@serveur

# Exemple : créer un proxy SOCKS sur le port 1080
ssh -D 1080 user@serveur-distant

# Configurer ton navigateur pour utiliser le proxy SOCKS localhost:1080
```

---

## 3. Options utiles pour les tunnels

### Garder le tunnel ouvert

Par défaut, SSH peut se déconnecter après un temps d'inactivité. Ajoute ces options :

```bash
# -N : n'exécute pas de commande distante (juste le tunnel)
# -f : passe en arrière-plan
# -o ServerAliveInterval=60 : envoie un ping toutes les 60s

ssh -L 8080:localhost:80 -N -f -o ServerAliveInterval=60 user@serveur
```

### Tunnel permanent avec autossh

Pour redémarrer automatiquement le tunnel si la connexion coupe :

```bash
# Installer autossh
sudo apt install autossh

# Créer un tunnel permanent
autossh -M 10984 -L 8080:localhost:80 -N -f user@serveur-distant
```

`-M 10984` = port de monitoring pour vérifier que le tunnel est vivant.

### Spécifier une clé SSH

```bash
ssh -L 8080:localhost:80 -i ~/.ssh/ma_cle_rsa user@serveur-distant
```

---

## 4. Exemples pratiques

### 4.1. Accéder à phpMyAdmin distant

```bash
# Le serveur distant a phpMyAdmin sur le port 80, accessible seulement en localhost
ssh -L 8888:localhost:80 user@serveur-distant
# Dans ton navigateur : http://localhost:8888/phpmyadmin
```

### 4.2. Se connecter à MySQL distant

```bash
# MySQL écoute sur localhost:3306 du serveur distant
ssh -L 3307:localhost:3306 user@serveur-distant
# Maintenant connecte-toi avec ton client MySQL local :
mysql -h 127.0.0.1 -P 3307 -u root -p
```

### 4.3. Tunnel vers un serveur Git privé

```bash
# Accéder à un serveur Git qui n'est accessible que via SSH sur un port non standard
ssh -L 7999:serveur-git:22 -p 2222 user@gateway.com

# Clone via le tunnel
git clone ssh://localhost:7999/repo.git
```

### 4.4. Tunnel inverse pour debug

```bash
# Depuis chez toi, expose ton service local pour qu'un collègue y accède via le serveur
ssh -R 8080:localhost:3000 user@serveur-distant
# Ton collègue peut maintenant accéder à ton app via http://serveur-distant:8080
```

---

## 5. Configurer des tunnels persistent dans ~/.ssh/config

Au lieu de retaper les options à chaque fois, ajoute-les à ton fichier de config SSH :

```bash
nano ~/.ssh/config
```

```bash
# Tunnel vers le serveur de prod
Host prod-tunnel
    HostName serveur-production.com
    User admin
    LocalForward 3307 localhost:3306
    LocalForward 8080 localhost:80
    ServerAliveInterval 60
    IdentityFile ~/.ssh/cle_production

# Proxy SOCKS vers le serveur de backup
Host backup-proxy
    HostName backup.example.com
    User deploy
    DynamicForward 1080
    ServerAliveInterval 60
```

Maintenant, un simple `ssh prod-tunnel` crée tous les tunnels définis !

---

## 6. Créer un service systemd pour un tunnel permanent

Pour qu'un tunnel survive aux redémarrages, crée un service systemd :

```bash
sudo nano /etc/systemd/system/ssh-tunnel.service
```

```ini
[Unit]
Description=SSH Tunnel vers serveur-prod
After=network.target

[Service]
ExecStart=/usr/bin/ssh -N -L 3307:localhost:3306 -L 8080:localhost:80 -o ServerAliveInterval=60 -i /home/user/.ssh/cle_production user@serveur-production.com
Restart=always
RestartSec=10
User=user

[Install]
WantedBy=multi-user.target
```

```bash
# Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable ssh-tunnel
sudo systemctl start ssh-tunnel

# Vérifier le statut
sudo systemctl status ssh-tunnel
```

---

## 7. Sécurité et bonnes pratiques

### ⚠️ Attention aux tunnels inverses

Les tunnels inverses exposent ton réseau à l'extérieur. Utilise ces protections :

```bash
# Limiter le tunnel inverse à localhost uniquement sur le serveur
ssh -R 8080:localhost:3000 -o GatewayPorts=no user@serveur

# Ou autoriser uniquement certaines IP sur le serveur distant
# Dans /etc/ssh/sshd_config du serveur :
GatewayPorts clientspecified
```

### 🔑 Utiliser des clés SSH (jamais de mots de passe)

```bash
# Générer une clé
ssh-keygen -t ed25519 -f ~/.ssh/tunnel_cle

# La copier sur le serveur
ssh-copy-id -i ~/.ssh/tunnel_cle user@serveur
```

### 🕵️ Limiter les permissions du fichier de clé

```bash
chmod 600 ~/.ssh/tunnel_cle
```

---

## 8. Exercice pratique

### Objectif

Crée un tunnel SSH pour accéder à une base de données PostgreSQL qui tourne sur un serveur distant et n'accepte que les connexions locales.

### Étapes

1. **Vérifie que PostgreSQL écoute localement sur le serveur distant :**
   ```bash
   ssh user@serveur-distant
   sudo ss -tlnp | grep 5432
   ```

2. **Crée le tunnel SSH (depuis ta machine locale) :**
   ```bash
   ssh -L 5433:localhost:5432 -N -f -o ServerAliveInterval=60 user@serveur-distant
   ```

3. **Vérifie que le tunnel est actif :**
   ```bash
   ss -tlnp | grep 5433
   # Tu dois voir LISTEN sur 127.0.0.1:5433
   ```

4. **Installe un client PostgreSQL et connecte-toi :**
   ```bash
   sudo apt install postgresql-client
   psql -h 127.0.0.1 -p 5433 -U postgres -d ma_base
   ```

5. **Fais une requête simple :**
   ```sql
   SELECT version();
   \q
   ```

6. **Configure le tunnel dans ~/.ssh/config pour le réutiliser facilement :**
   ```bash
   nano ~/.ssh/config
   # Ajoute un bloc "Host pg-tunnel" avec LocalForward 5433:localhost:5432
   ```

7. **Nettoie :**
   ```bash
   # Trouve et tue le tunnel
   ps aux | grep "ssh -L"
   kill [PID]
   ```

### Vérification

Tu peux te connecter à la base de données distante **uniquement** quand le tunnel SSH est actif. Sans SSH, la connexion est refusée — c'est la sécurité par conception.

---

## Résumé

| Commande | Description |
|----------|-------------|
| `ssh -L port:host:port_dist user@srv` | Tunnel local : accède à un service du serveur |
| `ssh -R port:host:port_local user@srv` | Tunnel inverse : expose un service local vers le serveur |
| `ssh -D port user@srv` | Proxy SOCKS : tout le trafic passe par SSH |
| `-N` | N'exécute pas de commande distante |
| `-f` | Passe en arrière-plan |
| `autossh -M port ...` | Tunnel automatique qui redémarre si coupé |
| `~/.ssh/config` | Configurer des tunnels persistants |

Les tunnels SSH sont un outil puissant pour accéder en sécurité à des services qui ne sont pas exposés directement sur le réseau. Comprends bien les trois types (local, inverse, dynamique) et utilise toujours des clés SSH plutôt que des mots de passe.
