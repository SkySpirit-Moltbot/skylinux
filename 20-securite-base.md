# Leçon 20 : Sécurité de base sous Linux

## Introduction

La sécurité est un aspect fondamental de l'administration Linux. Cette leçon présente les commandes et bonnes pratiques de base pour protéger votre système.

## Les bases de la sécurité

### Vérifier les utilisateurs connectés

```bash
# Voir qui est connecté au système
who

# Voir plus de détails (derrière un écran)
w

# Dernières connexions
last
```

### Gérer les mots de passe

```bash
# Changer son propre mot de passe
passwd

# Changer le mot de passe d'un autre utilisateur (root)
passwd nom_utilisateur

# Verrouiller un compte utilisateur
passwd -l nom_utilisateur

# Déverrouiller un compte
passwd -u nom_utilisateur
```

### Vérifier les ports ouverts

```bash
# Voir les ports en écoute
ss -tuln

# Alternative avec netstat
netstat -tuln

# Voir les connexions établies
ss -tn
```

## Pare-feu de base avec UFW

UFW (Uncomplicated Firewall) est un outil simple pour gérer le pare-feu.

### Commandes de base UFW

```bash
# Activer le pare-feu
sudo ufw enable

# Désactiver le pare-feu
sudo ufw disable

# Voir le statut
sudo ufw status

# Autoriser un port
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS

# Bloquer un port
sudo ufw deny 23

# Autoriser par service
sudo ufw allow ssh
sudo ufw allow http

# Régles détaillées
sudo ufw allow from 192.168.1.0/24 to any port 22
```

## Permissions de fichiers

###Bits spéciaux

```bash
# Bit setuid (exécuté avec les droits du propriétaire)
chmod u+s fichier

# Bit setgid (répertoire: nouveaux fichiers appartiennent au groupe)
chmod g+s repertoire

# Bit sticky (seul le propriétaire peut supprimer dans un répertoire)
chmod +t repertoire

# Voir les permissions avec ls
ls -l /bin/ping    # Notez le 's' à la place de x pour setuid
```

## Authentification par clé SSH

### Générer une clé SSH

```bash
# Générer une clé RSA
ssh-keygen -t rsa

# Générer une clé ED25519 (plus récente et sécurisée)
ssh-keygen -t ed25519

# Spécifier un commentaire
ssh-keygen -t ed25519 -C "mon_email@exemple.com"
```

### Copier la clé publique

```bash
# Méthode automatique
ssh-copy-id utilisateur@serveur

# Méthode manuelle
cat ~/.ssh/id_ed25519.pub
# Copier le contenu et l'ajouter dans ~/.ssh/authorized_keys du serveur
```

## Analyser les journaux de sécurité

```bash
# Voir les tentatives de connexion échouées
sudo grep "Failed password" /var/log/auth.log

# Voir les connexions réussies
sudo grep "Accepted" /var/log/auth.log

# Surveiller les connexions en temps réel
sudo tail -f /var/log/auth.log
```

## Commandes utiles

```bash
# Voir les processus qui consomment le plus
top
htop

# Vérifier l'espace disque
df -h

# Trouver les fichiers modifiés récemment (sécurité)
find / -mtime -1 -type f 2>/dev/null

# Vérifier les exécutables avec des droits root
sudo find / -perm -4000 -type f 2>/dev/null
```

## Exercice pratique

1. **Vérifier les utilisateurs** : Utilisez `who` et `w` pour voir qui est connecté sur votre système.

2. **Configurer UFW** :
   ```bash
   sudo ufw status
   sudo ufw allow ssh
   sudo ufw enable
   ```

3. **Créer une clé SSH** : Générez une clé SSH sur votre machine:
   ```bash
   ssh-keygen -t ed25519
   ```

4. **Analyser les logs** : Regardez les dernières connexions à votre système:
   ```bash
   sudo tail -20 /var/log/auth.log
   ```

5. **Vérifier les ports ouverts** :
   ```bash
   ss -tuln
   ```

## Résumé

Dans cette leçon, vous avez appris :

- **who/w** : Voir qui est connecté
- **passwd** : Gérer les mots de passe
- **ss/netstat** : Analyser les ports ouverts
- **UFW** : Gestion simple du pare-feu
- **ssh-keygen** : Créer des clés SSH sécurisées
- **/var/log/auth.log** : Consulter les journaux de sécurité

La sécurité est un processus continu. Vérifiez régulièrement ces éléments et gardez votre système à jour.