# Leçon 7 : Gestion des fichiers et dossiers

Dans cette leçon, tu vas apprendre à créer, copier, déplacer, supprimer et manipuler des fichiers et dossiers sous Linux de manière professionnelle.

---

## 1. Chemins et navigation

### Types de chemins

| Type | Description | Exemple |
|------|-------------|---------|
| **Absolu** | Depuis la racine `/` | `/home/david/Documents/fichier.txt` |
| **Relatif** | Depuis le répertoire courant | `Documents/fichier.txt` |
| **`.`** | Répertoire courant | `./script.sh` |
| **`..`** | Répertoire parent | `../autredossier` |
| **`~`** | Home de l'utilisateur | `~/Documents` |

### Commandes de navigation

```bash
pwd                 # Afficher le répertoire courant
cd /chemin/        # Aller dans un répertoire
cd                # Retourner au home (~)
cd -              # Retourner au répertoire précédent
ls                # Lister les fichiers
ls -l             # Liste détaillée
ls -a             # Inclure fichiers cachés
ls -la            # Tout lister
ls -lh            # Tailles lisibles (Ko, Mo)
ls -R             # Récursif (sous-dossiers)
```

---

## 2. Créer des fichiers et dossiers

### Créer un dossier

```bash
mkdir mondossier                    # Un dossier
mkdir -p dossier1/dossier2/dossier3  # Création récursive (avec parents)
mkdir -p ~/backup/{documents,images,config}  # Plusieurs dossiers
```

### Créer un fichier vide

```bash
touch fichier.txt        # Créer un fichier vide
touch file1.txt file2.txt  # Plusieurs fichiers
touch -d "2024-01-01" fichier.txt  # Avec date spécifique
```

### Créer un fichier avec contenu

```bash
echo "Bonjour" > bonjour.txt       # Écrase le fichier
echo "Ligne 1" >> bonjour.txt       # Ajoute à la fin
cat > fichier.txt                    # Saisie multiligne (Ctrl+D pour quitter)
printf "Texte %s\n" "test"          # Formaté
```

### Créer depuis un autre fichier

```bash
cp source.txt destination.txt       # Copier
mv ancien.txt nouveau.txt            # Déplacer (crée si n'existe pas)
```

---

## 3. Copier des fichiers et dossiers

### Syntaxe de base

```bash
cp [options] source destination
```

### Options essentielles

| Option | Description |
|--------|-------------|
| `-i` | Demander confirmation si destination existe |
| `-n` | Ne pas écraser |
| `-v` | Mode verbeux (affiche ce qu'il fait) |
| `-r` ou `-R` | Copie récursive (dossiers) |
| `-p` | Préserver les permissions, dates, propriétaire |
| `-a` | Archive = -dR --preserve=all |
| `-u` | Copier seulement si source plus récent |

### Exemples

```bash
cp fichier.txt dossier/              # Copier vers dossier
cp fichier1.txt fichier2.txt         # Copier avec nouveau nom
cp -r mondossier copie_mondossier   # Copier dossier récursif
cp -p fichier.txt backup/            # Préserver attributs
cp -i *.txt dossier/                # Confirmation pour chaque fichier
cp ../dossier/* .                   # Copier tous les fichiers du parent
cp fichier{,.bak}                   # Raccourci: fichier et fichier.bak
```

---

## 4. Déplacer et renommer

### La commande `mv`

```bash
mv [options] source destination
```

### Options

| Option | Description |
|--------|-------------|
| `-i` | Demander confirmation |
| `-n` | Ne pas écraser |
| `-v` | Verbeux |
| `-f` | Forcer (écraser sans demander) |
| `-u` | Déplacer seulement si plus récent |

### Exemples

```bash
mv fichier.txt /autre/dossier/       # Déplacer vers un dossier
mv ancien_nom.txt nouveau_nom.txt    # Renommer
mv fichier1 fichier2 dossier/       # Plusieurs fichiers
mv *.txt ~/Documents/                # Tous les .txt vers Documents
mv dossier/ ..                       # Monter d'un niveau
```

---

## 5. Supprimer

### Commandes de suppression

```bash
rm [options] fichier          # Supprimer fichier
rm -r dossier/               # Supprimer récursif (dossier + contenu)
rmdir dossier               # Supprimer dossier vide uniquement
```

### Options dangereuses à connaître

| Option | Description |
|--------|-------------|
| `-f` | Forcer (sans confirmation) |
| `-i` | Confirmer avant chaque suppression |
| `-r` | Récursif (dossiers) |
| `-v` | Verbeux |

### ⚠️ COMMANDES TRÈS DANGEREUSES - NE JAMAIS EXÉCUTER

```bash
rm -rf /          # SUPPRIMER TOUT LE DISQUE - DANGER!
rm -rf *          # Supprimer TOUT dans le dossier courant
rm -rf .*         # Supprimer fichiers cachés aussi
rm -rf ~/         # Supprimer son propre home - DANGER!
```

### Exemples sûrs

```bash
rm fichier.txt              # Supprimer un fichier
rm -r mondossier           # Supprimer dossier + contenu
rm -ri *.txt               # Confirmer pour chaque .txt
rm -v fichier.txt          # Afficher ce qui est supprimé
rmdir dossier_vide         # Supprime seulement si vide
```

---

## 6. Commandes avancées

### Lister avec détails

```bash
ls -l     # Permissions, owner, taille, date
ls -la    # + fichiers cachés
ls -lh    # Tailles humaines (1K, 1M)
ls -lt    # Tri par date modification
ls -lS    # Tri par taille
ls -1     # Un fichier par ligne
ls -d */  # Lister seulement les répertoires
```

### Permissions détaillées (ls -l)

```bash
-rw-r--r-- 1 david david 1234 Mar 12 10:00 fichier.txt
^ ^  ^   ^  ^   ^     ^    ^     ^
| |  |   |  |   |     |    |     +-- Nom du fichier
| |  |   |  |   |     |    +-- Taille en octets
| |  |   |  |   |     +-- Groupe
| |  |   |  |   +-- Propriétaire
| |  |   |  +-- Date de modification
| |  +----+-- Permissions (rwx pour owner, group, others)
+-- Type de fichier (- = fichier, d = dossier, l = lien)
```

### Commandes utiles supplémentaires

```bash
file fichier.txt        # Tipo de fichier (texte, image, etc.)
stat fichier            # Informations détaillées (dates, permissions)
rename 's/old/new/' *   # Renommer en masse (regex)
ln -s target lien       # Créer un lien symbolique
ls -li                  # Afficher numéro inode
```

---

## 7. Caractères spéciaux (Wildcards)

| Wildcard | Signification | Exemple |
|----------|---------------|---------|
| `*` | N'importe quels caractères | `*.txt` = tous les .txt |
| `?` | Un caractère | `fich?.txt` = fich1.txt |
| `[]` | Un caractère parmi | `[abc]*` = a*, b*, c* |
| `[!]` | Pas ces caractères | `[!a]*` = pas ceux commençant par a |
| `{...}` | Ensemble | `{a,b,c}.txt` = a.txt, b.txt, c.txt |

### Exemples

```bash
ls *.pdf                 # Tous les PDF
ls rapport-202*.pdf       # rapport-2020.pdf, rapport-2021.pdf
ls fichier?.txt          # fichier1.txt, fichier2.txt
ls [*]                   # Commençant par [
rm *~                    # Supprimer tous les fichiers de sauvegarde (~)
cp {file1,file2,file3}.txt dossier/  # Copier 3 fichiers
```

---

## 8. Exercices pratiques

### Exercice 1 : Créer une structure de projet
```bash
# Créer une structure de projet web
mkdir -p projet/{css,js,images,html}
touch projet/css/style.css
touch projet/js/main.js
ls -R projet
```

### Exercice 2 : Sauvegarde sécurisée
```bash
# Créer une backup avec date
mkdir -p ~/backups
cp -a ~/Documents ~/backups/documents_$(date +%Y%m%d)
ls -lh ~/backups/
```

### Exercice 3 : Nettoyer un dossier
```bash
# Déplacer tous les PDF vers un dossier
mkdir -p PDF
mv *.pdf PDF/
# Supprimer toutes les sauvegardes (~)
rm *~
```

### Exercice 4 : Renommer en masse
```bash
# Ajouter un préfixe à tous les fichiers
for f in *.txt; do mv "$f" "backup_$f"; done

# Ou avec rename
rename 's/^/backup_/' *.txt
```

---

## 9. Résumé

| Commande | Action |
|----------|--------|
| `mkdir -p` | Créer dossier avec parents |
| `touch` | Créer fichier vide |
| `cp -r` | Copier dossier récursif |
| `cp -p` | Préserver attributs |
| `mv` | Déplacer ou renommer |
| `rm -rf` | Supprimer récursif (DANGEREUX) |
| `rmdir` | Supprimer dossier vide |
| `ln -s` | Créer lien symbolique |
| `ls -lR` | Lister récursif |

---

## 10. Trucs et Astuces

```bash
# Raccourcis pratiques
mkdir -p ~/tmp/{a,b,c}       # Créer plusieurs dossiers
cp fichier{,.bak}            # Copie + backup
mv *.txt ../                 # Tout mover vers parent
rm -rf *                     # Vider un dossier (attention!)

# Historique des suppressions (si activé)
# Sous Zsh avec rm -v, les fichiers vont dans ~/.local/share/Trash/
```

---

Maîtrise ces commandes — elles sont le quotidien de tout administrateur Linux ! 💪