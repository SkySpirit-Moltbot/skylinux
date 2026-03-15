# Leçon 2 : Commandes de base

Dans cette leçon, tu vas maîtriser les commandes essentielles de Linux pour naviguer, manipuler des fichiers et interagir avec le terminal. Ce sont les fondations de tout administrateur Linux.

---

## 1. Navigation dans le système de fichiers

### pwd - print working directory

Affiche le répertoire courant (où tu es).

```bash
pwd                     # Résultat: /home/david
pwd -P                  # Chemin physique (suivre les liens)
pwd -L                  # Chemin logique (tel que tapé)
```

### cd - change directory

Se déplacer dans l'arborescence.

```bash
cd /home/david/Documents    # Chemin absolu
cd Documents               # Chemin relatif
cd ~                       # Home de l'utilisateur
cd                         # Retour au home
cd -                       # Répertoire précédent
cd ..                      # Monter d'un niveau
cd ../..                   # Monter de 2 niveaux
cd /                       # Racine du système
```

**Raccourcis utiles :**
- `~` ou `$HOME` : Répertoire personnel
- `..` : Répertoire parent
- `.` : Répertoire courant
- `-` : Répertoire précédent

---

## 2. Lister les fichiers

### ls - list

```bash
ls                      # Liste basique
ls -l                   # Format long (détails)
ls -a                   # Inclure fichiers cachés
ls -A                   # Cachés sauf . et ..
ls -la                  # Tout ensemble
ls -lh                  # Tailles humaines (Ko, Mo, Go)
ls -lS                  # Trier par taille
ls -lt                  # Trier par date
ls -ltr                 # Trier par date inversé
ls -1                   # Un fichier par ligne
ls -d */                # Lister seulement les dossiers
ls -F                   # Indicateurs de type
ls -R                   # Récursif (sous-dossiers)
```

### Comprendre ls -l

```
-rw-r--r-- 1 david david 1234 Mar 10 10:00 fichier.txt
^            ^    ^     ^   ^        ^
|            |    |     |   |        +-- Nom
|            |    |     |   +-- Date modification
|            |    |     | +-- Taille (octets)
|            |    |     +-- Groupe
|            |    +-- Propriétaire
|            +-- Permissions (rwx)
+-- Type de fichier (- = fichier, d = dossier, l = lien)
```

### Commandes complémentaires

```bash
# Lister par extension
ls *.txt

# Lister par motif
ls fichier*

# Lister avec couleur (si activé)
ls --color=auto

# Lister inode (numéro unique)
ls -li
```

---

## 3. Créer des fichiers et dossiers

### mkdir - make directory

```bash
mkdir dossier                 # Créer un dossier
mkdir -p a/b/c/d              # Créer récursif
mkdir -p projet/{src,bin,doc} # Plusieurs dossiers
mkdir -m 755 dossier          # Avec permissions
```

### touch - créer un fichier vide

```bash
touch fichier.txt             # Créer fichier vide
touch file1.txt file2.txt     # Plusieurs fichiers
touch -d "2024-01-01" file    # Avec date
touch -a file                # Modifier date accès
touch -m file                # Modifier date modification
```

### echo et printf - créer avec contenu

```bash
echo "Bonjour" > fichier.txt         # Créer et écrire
echo "Ligne 1" >> fichier.txt         # Ajouter
printf "Bonjour %s\n" "Monde"        # Formaté
```

---

## 4. Copier des fichiers

### cp - copy

```bash
cp source.txt destination.txt           # Copier fichier
cp fichier.txt dossier/                  # Vers dossier
cp -r dossier/ copie_dossier/           # Copier dossier
cp -i fichier.txt dest.txt              # Confirmation
cp -n fichier.txt dest.txt              # Pas écraser
cp -p fichier.txt dest.txt              # Préserver attributs
cp -a dossier/ copie/                   # Archive (tout préserver)
cp -v fichier.txt dest.txt              # Verbeux
cp -u fichier.txt dest.txt              # Copier si plus récent
cp fichier{,.bak}                       # Raccourci: + .bak
```

### Options détaillées

| Option | Description |
|--------|-------------|
| `-i` | Demander confirmation |
| `-n` | Ne pas écraser |
| `-v` | Afficher ce qui est fait |
| `-p` | Préserver permissions, propriétaire, timestamp |
| `-r` | Copier récursivement |
| `-a` | Archive = -dR --preserve=all |
| `-u` | Mettre à jour si plus récent |

---

## 5. Déplacer et renommer

### mv - move

```bash
mv source.txt destination.txt       # Renommer
mv fichier.txt dossier/              # Déplacer vers dossier
mv fichier1.txt fichier2.txt dossier/  # Plusieurs fichiers
mv -i fichier.txt dest.txt          # Confirmation
mv -n fichier.txt dest.txt         # Pas écraser
mv -v fichier.txt dest.txt         # Verbeux
mv -f fichier.txt dest.txt         # Forcer
mv *.txt dossier/                   #Tous les .txt
```

---

## 6. Supprimer des fichiers

### rm - remove

```bash
rm fichier.txt                   # Supprimer fichier
rm -r dossier/                   # Supprimer dossier
rm -rf dossier/                  # Forcer (sans confirmation)
rm -ri dossier/                  # Confirmer chaque
rm -v fichier.txt                 # Verbeux

# ⚠️ DANGEREUX - NE JAMAIS FAIRE :
rm -rf /              # SUPPRIMER TOUT LE SYSTÈME !
rm -rf .             # Supprimer tout dossier courant
rm -rf *             # Supprimer TOUT le contenu
```

### rmdir - remove directory

```bash
rmdir dossier              # Supprimer dossier vide
rmdir -p a/b/c/d           # Supprimer chemin vide
```

---

## 7. Lire le contenu des fichiers

### cat - concatenate

```bash
cat fichier.txt                    # Afficher tout
cat -n fichier.txt                 # Avec numéros de ligne
cat -b fichier.txt                 # Numéros lignes non-vides
cat -s fichier.txt                 # Supprimer lignes vides multiples
cat fichier1.txt fichier2.txt      # Concaténer
cat -A fichier.txt                 # Afficher caractères spéciaux
```

### less - afficher page par page

```bash
less gros_fichier.log              # Afficher
less -N gros_fichier              # Numéros de ligne
less -S gros_fichier              # Sans retour à la ligne
```

**Commandes dans less :**

| Touche | Action |
|--------|--------|
| Espace | Page suivante |
| b | Page précédente |
|Entrée | Ligne suivante |
| q | Quitter |
| /motif | Rechercher en avant |
| ?motif | Rechercher en arrière |
| n | Résultat suivant |
| N | Résultat précédent |
| g | Début du fichier |
| G | Fin du fichier |

### head - début du fichier

```bash
head fichier.txt                   # 10 premières lignes
head -n 20 fichier.txt            # 20 premières lignes
head -c 100 fichier.txt            # 100 premiers octets
head -q fichier1.txt fichier2.txt # Plusieurs fichiers
```

### tail - fin du fichier

```bash
tail fichier.txt                   # 10 dernières lignes
tail -n 20 fichier.txt             # 20 dernières lignes
tail -f fichier.log                # Suivre en temps réel
tail -f -n 100 fichier.log         # 100 dernières lignes en direct
tail -c 100 fichier.txt            # 100 derniers octets
```

### nl - numbered lines

```bash
nl fichier.txt                     # Afficher avec numéros
nl -ba fichier.txt                 # Numéros même lignes vides
```

---

## 8. Compter et analyser

### wc - word count

```bash
wc fichier.txt                     # Lignes mots octets
wc -l fichier.txt                  # Nombre de lignes
wc -w fichier.txt                  # Nombre de mots
wc -c fichier.txt                  # Nombre d'octets
wc -m fichier.txt                  # Nombre de caractères
```

### file - type de fichier

```bash
file fichier.txt
file *
file -z archive.tar.gz             # Contenu sans décompresser
```

---

## 9. Commandes d'information

### date - afficher la date

```bash
date                   # Date et heure
date +%H:%M            # Juste l'heure
date +%d/%m/%Y         # Format personnalisé
date -d "tomorrow"     # Date future
date -d "2 days ago"  # Date passée
```

### whoami - utilisateur courant

```bash
whoami                 # Nom de l'utilisateur
whoami -r             # ID du groupe
```

### uptime - temps de fonctionnement

```bash
uptime                 # Heures de fonctionnement
uptime -s              # Depuis quand allumé
```

### cal - calendrier

```bash
cal                    # Mois en cours
cal 2024                #Année entière
cal -3                 # 3 mois
cal -m 1               # Janvier avec Lundi
```

---

## 10. Alias et raccourcis

### Créer des alias

```bash
# Temporaire (session)
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'

# Permanent (ajouter à ~/.bashrc)
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc
```

### Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| Tab | Complétion automatique |
| Ctrl+C | Interrompre commande |
| Ctrl+Z | Suspendre commande |
| Ctrl+L | Effacer l'écran |
| Ctrl+U | Effacer la ligne |
| Ctrl+K | Effacer jusqu'à la fin |
| Ctrl+A | Début de ligne |
| Ctrl+E | Fin de ligne |
| Ctrl+R | Rechercher dans l'historique |
| !! | Dernière commande |
| !$ | Dernier argument |
| !!:gs/old/new | Remplacer dans la dernière commande |

---

## 11. Exercices pratiques

### Exercice 1 : Navigation
```bash
pwd                              # Où suis-je ?
cd /tmp                          # Aller dans /tmp
cd ~                             # Retour au home
cd -                             # Revenir au précédent
```

### Exercice 2 : Créer une structure
```bash
mkdir -p projet/{src,docs,tests}
touch projet/src/main.py
touch projet/tests/test_main.py
ls -R projet/
```

### Exercice 3 : Manipulation de fichiers
```bash
echo "#!/bin/bash" > script.sh
chmod +x script.sh
cp script.sh script_backup.sh
ls -l *.sh
```

### Exercice 4 : Lire des logs
```bash
head -20 /var/log/syslog
tail -f /var/log/syslog          # En temps réel
grep -i error /var/log/syslog | head -10
```

---

## 12. Tableau résumé

| Commande | Description |
|----------|-------------|
| `pwd` | Répertoire courant |
| `ls` | Lister fichiers |
| `cd` | Changer répertoire |
| `mkdir` | Créer dossier |
| `touch` | Créer fichier |
| `cp` | Copier |
| `mv` | Déplacer/renommer |
| `rm` | Supprimer |
| `cat` | Afficher fichier |
| `less` | Afficher page par page |
| `head` | Début du fichier |
| `tail` | Fin du fichier |
| `wc` | Compter |

---

Ces commandes sont ton quotidien sous Linux. Maîtrise-les ! 💪