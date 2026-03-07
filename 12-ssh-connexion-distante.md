# Leçon 12 : SSH et connexion distante

## Introduction

SSH (Secure Shell) est un protocole qui permet de se connecter à distance à un autre ordinateur de manière sécurisée. C'est indispensable pour administrer des serveurs ou accéder à sa machine depuis un autre endroit.

## Concepts clés

- **SSH** : Protocole sécurisé pour la connexion à distance
- **Client SSH** : Logiciel qui permet de se connecter (ssh sous Linux)
- **Serveur SSH** : Service qui accepte les connexions distantes (sshd)
- **Clé SSH** : Méthode d'authentification plus sécurisée que le mot de passe

## Commandes essentielles

### Se connecter à une machine distante

```bash
ssh utilisateur@adresse_ip
# Exemple : ssh admin@192.168.1.100
ssh utilisateur@nom-domaine.com
```

### Utiliser un port différent (par défaut 22)

```bash
ssh -p 2222 utilisateur@serveur
```

### Générer une clé SSH

```bash
ssh-keygen -t ed25519 -C "votre_email@exemple.com"
```

### Copier sa clé publique sur le serveur

```bash
ssh-copy-id utilisateur@serveur
```

### Copier des fichiers via SSH (SCP)

```bash
# Copier un fichier local vers le serveur
scp fichier.txt utilisateur@serveur:/chemin/destination/

# Copier un fichier du serveur vers local
scp utilisateur@serveur:/chemin/fichier.txt ./
```

### Utiliser SFTP pour un transfert interactif

```bash
sftp utilisateur@serveur
```

## Port Forwarding (Tunnel SSH)

Le port forwarding permet d'accéder à un service sur le serveur SSH comme si il était en local sur ta machine.

### Format
```bash
ssh -L [port_local]:[destination]:[port_destination] utilisateur@serveur
```

### Exemple pratique
```bash
ssh -L 11435:127.0.0.1:11434 utilisateur@serveur
```
解释 :
- **11435** → port local sur ton ordinateur (après -L)
- **127.0.0.1** → adresse vue depuis le serveur SSH (ici localhost)
- **11434** → port du service sur le serveur

### Cas d'usage courants

| Commande | Description |
|---------|-------------|
| `ssh -L 8080:localhost:80 user@serveur` | Accéder au serveur web local du serveur |
| `ssh -L 3306:localhost:3306 user@serveur` | Accéder à MySQL du serveur |
| `ssh -L 5432:localhost:5432 user@serveur` | Accéder à PostgreSQL du serveur |

### Exercice

1. Connecte-toi avec un tunnel :
   ```bash
   ssh -L 9000:localhost:80 user@ton_serveur
   ```
2. Ouvre un navigateur et va sur `http://localhost:9000`
3. Tu devrais voir le serveur web du serveur distant !

## Exercice pratique

1. Génère une clé SSH sur ta machine :
   ```bash
   ssh-keygen -t ed25519
   ```

2. Essaie de te connecter à localhost si SSH est installé :
   ```bash
   ssh localhost
   ```

3. Crée un fichier texte et copie-le vers un autre répertoire en utilisant `scp` :
   ```bash
   echo "Bonjour" > test.txt
   scp test.txt /tmp/
   ```

## Résumé

- **SSH** permet de se connecter à distance de manière sécurisée
- La commande `ssh` sert de client, `sshd` est le serveur
- Les clés SSH offrent une authentification plus sécurisée
- **SCP** et **SFTP** permettent de transférer des fichiers
