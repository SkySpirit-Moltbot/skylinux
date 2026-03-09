# Leçon 14 : Gestion des utilisateurs et groupes

## Introduction

Linux est un système multi-utilisateurs. Chaque personne qui accède à une machine Linux le fait via un compte utilisateur. Comprendre comment créer, modifier et supprimer des utilisateurs, ainsi que comment gérer les groupes, est essentiel pour tout administrateur système.

---

## Les fichiers de configuration

Avant de manipuler les utilisateurs, connais ces fichiers clés :

| Fichier | Description |
|---------|-------------|
| `/etc/passwd` | Liste de tous les utilisateurs (nom, UID, GID, shell, etc.) |
| `/etc/shadow` | Contient les mots de passe chiffrés |
| `/etc/group` | Liste des groupes et de leurs membres |
| `/etc/skel/` | Répertoire modèle pour les nouveaux utilisateurs |

---

## Commandes de base

### Ajouter un utilisateur

```bash
sudo useradd -m david       # Crée l'utilisateur "david" avec son répertoire personnel
sudo passwd david           # Définit le mot de passe de david
```

Options utiles :
- `-m` : Crée le répertoire home (`/home/david`)
- `-s /bin/bash` : Définit le shell par défaut
- `-G groupe1,groupe2` : Ajoute à des groupes secondaires

### Supprimer un utilisateur

```bash
sudo userdel david          # Supprime l'utilisateur (garde le home)
sudo userdel -r david       # Supprime aussi le répertoire home
```

### Modifier un utilisateur

```bash
sudo usermod -l nouveau_nom ancien_nom    # Renomme l'utilisateur
sudo usermod -aG groupe utilisateur       # Ajoute à un groupe (IMPORTANT : -a sinon remplace)
sudo usermod -s /bin/sh utilisateur       # Change le shell
```

---

## Gestion des groupes

### Créer et supprimer un groupe

```bash
sudo groupadd developpeurs   # Crée le groupe "developpeurs"
sudo groupdel developpeurs   # Supprime le groupe
```

### Ajouter/retirer des membres

```bash
sudo gpasswd -a david developpeurs   # Ajoute david au groupe
sudo gpasswd -d david developpeurs   # Retire david du groupe
```

### Voir ses groupes

```bash
id              # Affiche UID, GID et tous les groupes
groups          # Affiche seulement les groupes
```

---

## Exemple pratique

### Scenario : Créer un utilisateur pour un nouvel employé

```bash
# 1. Créer l'utilisateur avec son répertoire
sudo useradd -m -s /bin/bash -G sudo,navigation marc

# 2. Définir son mot de passe
sudo passwd marc

# 3. Vérifier
id marc
# Résultat : uid=1001(marc) gid=1001(marc) groups=1001(marc),27(sudo),100(navigation)
```

### Changer le propriétaire d'un fichier

```bash
sudo chown marc:developpeurs /var/projet      # Change propriétaire ET groupe
sudo chown marc /var/projet                   # Change seulement le propriétaire
sudo chgrp developpeurs /var/projet            # Change seulement le groupe
```

---

## Exercice pratique

1. **Crée un utilisateur test** nommé "stagiaire" avec un répertoire personnel
2. **Crée un groupe** nommé "stagiaires"
3. **Ajoute "stagiaire"** au groupe "stagiaires"
4. **Vérifie** avec la commande `id` que tout est correct
5. **Crée un fichier** dans `/tmp` et change son propriétaire pour "stagiaire"
6. **Supprime** l'utilisateur et le groupe créés

---

## Résumé

| Commande | Action |
|----------|--------|
| `useradd -m nom` | Crée un utilisateur |
| `passwd nom` | Définit le mot de passe |
| `userdel -r nom` | Supprime l'utilisateur et son home |
| `groupadd nom` | Crée un groupe |
| `usermod -aG groupe user` | Ajoute un utilisateur à un groupe |
| `id user` | Affiche les infos d'un utilisateur |
| `chown user:groupe fichier` | Change propriétaire et groupe |

La gestion des utilisateurs et groupes est fondamentale pour la sécurité et l'organisation d'un système Linux. Maîtrise ces commandes pour掌控er accès à ta machine !
