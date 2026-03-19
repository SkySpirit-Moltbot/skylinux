# Leçon 3 : Permissions Linux

Dans cette leçon, tu vas maîtriser les permissions Linux, un concept fondamental pour la sécurité et l'administration système.

---

## 1. Comprendre les permissions

### Qu'est-ce que les permissions ?

Sous Linux, chaque fichier et dossier a des **permissions** qui définissent qui peut :
- **Lire** (r - Read)
- **Écrire** (w - Write)
- **Exécuter** (x - Execute)

### Trois types d'utilisateurs

| Catégorie | Description |
|-----------|-------------|
| **Propriétaire (Owner)** | L'utilisateur qui a créé le fichier |
| **Groupe (Group)** | Le groupe associé au fichier |
| **Autres (Others)** | Tous les autres utilisateurs |

### Notation symbolique

```
rwx rwx rwx
│      │      │
proprio groupe autres
```

| Symbole | Signification |
|---------|---------------|
| `r` | Lecture autorisée |
| `w` | Écriture autorisée |
| `x` | Exécution autorisée |
| `-` | Permission refusée |

---

## 2. Voir les permissions

### Commande ls -l

```bash
ls -l /home/david/fichier.txt
```

Résultat :
```
-rw-r--r-- 1 david david 1234 Mar 10 10:00 fichier.txt
```

Décryptage :
```
-    rw-    r--    r--  1  david  david  1234  Mar 10 10:00 fichier.txt
│    │      │      │    │     │      │      │       │         │
Type│Owner │Group │Other│Link │Owner │Group │Size   │Date      │Name
```

| Caractère | Type |
|-----------|------|
| `-` | Fichier régulier |
| `d` | Répertoire |
| `l` | Lien symbolique |
| `c` | Périphérique caractère |
| `b` | Périphérique bloc |

---

## 3. Modifier les permissions

### Commande chmod

#### Notation symbolique

```bash
# Ajouter une permission
chmod +x script.sh         # Ajouter exécution pour tous
chmod u+x script.sh       # Propriétaire peut exécuter
chmod g+w dossier/        # Groupe peut écrire
chmod o-r fichier.txt     # Autres ne peuvent plus lire

# Retirer une permission
chmod -w fichier.txt      # Retirer écriture pour tous

# Définir exactement
chmod u=rwx,g=rx,o=r fichier
```

#### Notation octale

```bash
#Valeurs
r = 4
w = 2
x = 1
- = 0

# Exemples
chmod 777 fichier     # rwxrwxrwx (tout permis)
chmod 755 fichier    # rwxr-xr-x (standard)
chmod 644 fichier    # rw-r--r-- (lecture pour tous)
chmod 700 fichier    # rwx------ (propriétaire seul)
chmod 600 fichier    # rw------- (propriétaire seul)
```

### Tableau des permissions Octales

| Octal | Symbolique | Description |
|-------|-----------|-------------|
| 0 | `---` | Aucune permission |
| 1 | `--x` | Exécution |
| 2 | `-w-` | Écriture |
| 3 | `-wx` | Écriture + exécution |
| 4 | `r--` | Lecture |
| 5 | `r-x` | Lecture + exécution |
| 6 | `rw-` | Lecture + écriture |
| 7 | `rwx` | Tout |

---

## 4. Modifier propriétaire et groupe

### Chown - Changer le propriétaire

```bash
# Changer le propriétaire
sudo chown utilisateur fichier

# Changer propriétaire et groupe
sudo chown utilisateur:groupe fichier

# Changer le groupe seulement
sudo chown :groupe fichier
```

### Chgrp - Changer le groupe

```bash
sudo chgrp groupe fichier
```

### Options utiles

```bash
# Récursif (dossiers)
sudo chown -R utilisateur dossier/

# Préserver les liens symbolique
sudo chown -h lien_symbolique
```

### Exemples pratiques

```bash
# Rendre un script exécutable
chmod +x monscript.sh

# Permettre l'écriture au groupe
chmod g+w dossier/

# Serveur web (Apache/Nginx)
sudo chown -R www-data:www-data /var/www/html/

# Dossier partagé
sudo chown -R root:shared /partage/
sudo chmod -R 2775 /partage/  # SGID pour hériter
```

---

## 5. Permissions spéciales

### SetUID (4000)

Exécute avec les droits du propriétaire (rare, dangéreux).

```bash
# Ajouter
chmod 4755 executable

# Notation symbolique
chmod u+s executable
```

### SetGID (2000)

Les fichiers héritent du groupe du répertoire.

```bash
chmod 2755 dossier/
chmod g+s dossier/
```

### Sticky Bit (1000)

Sur un répertoire, seuls les propriétaires peuvent supprimer leurs fichiers.

```bash
chmod 1777 /tmp
chmod +t /tmp
```

---

## 6. Umask

### Qu'est-ce que umask ?

`umask` définit les permissions par défaut pour les nouveaux fichiers.

```bash
# Voir umask actuel
umask

# Modifier pour la session
umask 022

# Rendre permanent (ajouter dans ~/.bashrc)
echo "umask 022" >> ~/.bashrc
```

### Calculer umask

Pour un fichier (par défaut 666) :
- umask 022 → 666 - 022 = 644

Pour un répertoire (par défaut 777) :
- umask 022 → 777 - 022 = 755

---

## 7. Propriétés avancées des fichiers

### ACL (Access Control Lists)

Pour des permissions plus fines, utiliser les ACL.

```bash
# Installer si besoin
sudo apt install acl

# Voir les ACL
getfacl fichier

# Ajouter une permission ACL
setfacl -m u:utilisateur:rwx fichier

# Supprimer ACL
setfacl -x u:utilisateur fichier

# Par défaut (pour nouveaux fichiers)
setfacl -m d:u:utilisateur:rx dossier/
```

---

## 8. Bonnes pratiques de sécurité

### Permissions recommandées

| Fichier/Dossier | Permissions | Raison |
|-----------------|-------------|--------|
| Scripts shell | 755 (rwxr-xr-x) | Exécutable par tous |
| Fichiers personnels | 600 (rw-------) | Privé |
| Clés SSH | 600 (rw-------) | Sécurisé |
| Répertoire web | 755 | Lecture publique |
| /tmp | 1777 | Temporaire mais protégé |
| Fichiers config système | 644 | Lecture, écriture root |

### ⚠️ Commandes dangereuses à éviter

```bash
chmod -R 777 /          # DANGER!
chmod -R 777 /home      # DANGER!
chmod -R 777 /etc       # TRES DANGER!
chmod 777 /etc/passwd   # DANGER!
```

---

## 9. Exercices pratiques

### Exercice 1 : Script exécutable
```bash
# Créer un script
echo '#!/bin/bash' > test.sh
echo 'echo "Hello"' >> test.sh

# Rendre exécutable
chmod +x test.sh

# Exécuter
./test.sh
```

### Exercice 2 : Partage de dossier
```bash
# Créer un groupe
sudo groupadd partage

# Ajouter des utilisateurs
sudo usermod -aG partage utilisateur1
sudo usermod -aG partage utilisateur2

# Configurer le dossier
sudo chown :partage /partage
sudo chmod 2775 /partage
```

---

## 10. Résumé

| Commande | Description |
|----------|-------------|
| `ls -l` | Voir les permissions |
| `chmod` | Modifier les permissions |
| `chown` | Modifier le propriétaire |
| `chgrp` | Modifier le groupe |
| `umask` | Permissions par défaut |
| `getfacl` | Voir ACL |
| `setfacl` | Modifier ACL |

---

Maîtrise les permissions pour sécuriser ton système Linux ! 🔐