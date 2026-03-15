# Leçon 14 : Gestion des utilisateurs et groupes

Dans cette leçon, tu vas maîtriser la gestion des utilisateurs et groupes sous Linux, essentiel pour l'administration système.

---

## 1. Concepts de base

### Utilisateur

Un utilisateur Linux possède :
- **UID** : Identifiant unique
- **GID** : Groupe principal
- **Répertoire personnel** : /home/username
- **Shell** : Interpréteur par défaut
- **Mot de passe** : Stocké dans /etc/shadow

### Groupe

Un groupe permet de :
- Partager des fichiers entre utilisateurs
- Gérer des permissions collectivement

### Fichiers système importants

| Fichier | Description |
|---------|-------------|
| `/etc/passwd` | Infos utilisateurs |
| `/etc/shadow` | Mots de passe chiffrés |
| `/etc/group` | Infos groupes |
| `/etc/skel/` | Modèle pour nouveaux utilisateurs |

---

## 2. Commandes utilisateur

### Ajouter un utilisateur

```bash
# Créer un utilisateur
sudo useradd -m nom_utilisateur

# Avec options
sudo useradd -m -s /bin/bash -c "Description" -G groupe1,groupe2 nom

#交互式
sudo adduser nom_utilisateur
```

### Modifier un utilisateur

```bash
# Changer le shell
sudo usermod -s /bin/zsh nom

# Ajouter à un groupe
sudo usermod -aG groupe nom

# Changer le répertoire home
sudo usermod -d /nouveau/chemin -m nom

# Verrouiller/déverrouiller un compte
sudo usermod -L nom           # Verrouiller
sudo usermod -U nom           # Déverrouiller
```

### Supprimer un utilisateur

```bash
# Supprimer (garde les fichiers)
sudo userdel nom

# Supprimer avec fichiers
sudo userdel -r nom

# Supprimer avec confirmation
sudo userdel -r -f nom
```

### Changer le mot de passe

```bash
# Changer son mot de passe
passwd

# Changer mot de passe d'un autre utilisateur (root)
sudo passwd nom_utilisateur

# Vider le mot de passe
sudo passwd -d nom_utilisateur

# Expirer le mot de passe
sudo passwd -e nom_utilisateur
```

---

## 3. Commandes groupe

### Créer un groupe

```bash
sudo groupadd nom_groupe
sudo groupadd -g 1005 nom_groupe   # Avec GID spécifique
```

### Modifier un groupe

```bash
# Renommer un groupe
sudo groupmod -n nouveau_nom ancien_nom

# Changer le GID
sudo groupmod -g 1006 nom_groupe
```

### Supprimer un groupe

```bash
sudo groupdel nom_groupe
```

### Gérer les membres

```bash
# Ajouter un utilisateur à un groupe
sudo usermod -aG groupe utilisateur

# Retirer d'un groupe
sudo gpasswd -d utilisateur groupe

# Voir les membres d'un groupe
getent group groupe
```

---

## 4. Informations et listing

### Voir les utilisateurs

```bash
# Liste des utilisateurs
cat /etc/passwd
# ou
getent passwd

# Filtrer
getent passwd | cut -d: -f1

# Derniers utilisateurs créés
lastlog
```

### Voir les groupes

```bash
# Liste des groupes
cat /etc/group
# ou
getent group

# groupes d'un utilisateur
groups nom_utilisateur
id nom_utilisateur
```

### Voir l'UID et GID

```bash
id                       # Ses propres IDs
id nom_utilisateur       # IDs d'un utilisateur
```

---

## 5. Commandes avancées

### sudoers - Permissions sudo

```bash
# Éditer le fichier sudoers (TOUJOURS avec visudo!)
sudo visudo

# Ajouter un utilisateur au groupe sudo
sudo usermod -aG sudo nom

# Voir qui a sudo
getent group sudo
```

### Expiration de compte

```bash
# Définir une date d'expiration
sudo usermod -e 2024-12-31 nom

# Voir la date d'expiration
sudo chage -l nom

#Forcer changement mot de passe
sudo chage -d 0 nom
```

### Verrouillage de compte

```bash
# Verrouiller
sudo passwd -l nom

# Déverrouiller
sudo passwd -u nom

# Voir le statut
sudo passwd -S nom
```

---

## 6. Gestion des mots de passe

### Politiques de mot de passe

```bash
# Installer libpam-pwquality
sudo apt install libpam-pwquality

# Configurer (/etc/security/pwquality.conf)
sudo nano /etc/security/pwquality.conf
```

### Exigences communes

```
minlen = 12
dcredit = -1          # Au moins 1 chiffre
ucredit = -1          # Au moins 1 majuscule
lcredit = -1          # Au moins 1 minuscule
ocredit = -1          # Au moins 1 caractère spécial
```

### Historique et expiration

```bash
# Configuration dans /etc/login.defs
# ou avec chage
sudo chage -m 7 nom       # Minimum 7 jours
sudo chage -M 90 nom      # Maximum 90 jours
sudo chage -W 7 nom       # Avertissement 7 jours avant expiration
sudo chage -I 30 nom      # Verrouillage 30 jours après expiration
```

---

## 7. Scripts pratiques

### Créer un nouvel utilisateur avec tout

```bash
#!/bin/bash

# Variables
USERNAME="nouvelutilisateur"
FULLNAME="Nouvel Utilisateur"
SHELL="/bin/bash"
GROUPES="sudo,users"

# Créer le groupe principal s'il n'existe pas
sudo groupadd $USERNAME 2>/dev/null

# Créer l'utilisateur
sudo useradd -m -s $SHELL -c "$FULLNAME" -G $GROUPES $USERNAME

# Définir le mot de passe
sudo passwd $USERNAME

echo "Utilisateur $USERNAME créé avec succès!"
```

### Script de suppression

```bash
#!/bin/bash

USERNAME="utilisateur_a_supprimer"

# Demander confirmation
read -p "Supprimer l'utilisateur $USERNAME? (o/n): " confirm

if [ "$confirm" = "o" ]; then
    sudo userdel -r $USERNAME
    echo "Utilisateur supprimé."
else
    echo "Annulé."
fi
```

---

## 8. Bonnes pratiques

| Pratique | Description |
|----------|-------------|
| Utiliser sudo | Pas de connection root directe |
| Mots de passe forts | Minimum 12 caractères, mélange |
| Groupes logiques | Regrouper par projet/fonction |
| Audit régulier | Vérifier les utilisateurs |
| Désactiver compte | Jamais supprimer (garder UID) |
| Limiter sudo | Seulement utilisateurs nécessaires |

---

## 9. Résumé

| Commande | Description |
|----------|-------------|
| `useradd` | Créer utilisateur |
| `usermod` | Modifier utilisateur |
| `userdel` | Supprimer utilisateur |
| `passwd` | Changer mot de passe |
| `groupadd` | Créer groupe |
| `groupdel` | Supprimer groupe |
| `groups` | Lister ses groupes |
| `id` | Voir UID/GID |
| `getent` | Consulter base |

---

Maîtrise la gestion des utilisateurs pour administrer Linux correctement ! 👤