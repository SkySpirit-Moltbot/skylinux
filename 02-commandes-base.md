# Leçon 2 : Les commandes de base

Dans cette leçon, nous allons découvrir les commandes essentielles pour naviguer et manipuler le système de fichiers sous Linux.

## 2.1 Navigation de base

### pwd - Where am I ?

La commande `pwd` (print working directory) affiche le répertoire courant. C'est très utile pour savoir où l'on se trouve dans l'arborescence.

```bash
pwd
# Exemple de résultat : /home/david
```

### ls - Liste des fichiers

La commande `ls` liste le contenu d'un répertoire.

```bash
# Lister le contenu courant
ls

# Liste détaillée (permissions, taille, date)
ls -l

# Liste incluant les fichiers cachés
ls -la

# Liste avec les couleurs
ls --color=auto
```

**Options utiles :**
- `-l` : format long (détaillé)
- `-a` : afficher les fichiers cachés (commençant par .)
- `-h` : tailles lisibles (Ko, Mo, Go)
- `-r` : ordre inverse
- `-t` : trier par date de modification

### cd - Changer de répertoire

La commande `cd` (change directory) permet de se déplacer dans l'arborescence.

```bash
# Aller dans un répertoire
cd /home/david/Documents

# Revenir au répertoire personnel
cd ~

# Revenir au répertoire précédent
cd -

# Remonter d'un niveau
cd ..

# Rester dans le répertoire courant (rarement utilisé seul)
cd .
```

**Raccourcis utiles :**
- `~` représente votre répertoire personnel (/home/votreutilisateur)
- `..` représente le répertoire parent
- `.` représente le répertoire courant

## 2.2 Manipuler les fichiers et dossiers

### mkdir - Créer un répertoire

```bash
# Créer un répertoire
mkdir mon_dossier

# Créer plusieurs niveaux
mkdir -p dossier1/dossier2/sous-dossier

# Créer avec permissions spécifiques
mkdir -m 755 mon_dossier
```

### touch - Créer un fichier vide

```bash
# Créer un fichier vide
touch mon_fichier.txt

# Créer plusieurs fichiers
touch fichier1.txt fichier2.txt
```

### cp - Copier des fichiers

```bash
# Copier un fichier
cp source.txt destination.txt

# Copier dans un répertoire
cp fichier.txt /home/david/Documents/

# Copier récursivement (répertoires)
cp -r dossier_source dossier_destination

# Conserver les attributs
cp -p fichier.txt copie.txt
```

### mv - Déplacer ou renommer

```bash
# Déplacer un fichier
mv fichier.txt /home/david/Documents/

# Renommer un fichier
mv ancien_nom.txt nouveau_nom.txt

# Déplacer et renommer
mv fichier.txt /home/david/Documents/nouveau.txt
```

### rm - Supprimer

```bash
# Supprimer un fichier
rm mon_fichier.txt

# Supprimer un répertoire et son contenu
rm -r mon_dossier

# Supprimer sans confirmation
rm -f fichier.txt

# Supprimer uniquement les fichiers (pas les répertoires)
rm -rf *
```

**Attention :** La suppression sous Linux est définitive ! Pas de corbeille par défaut.

## 2.3 Lire le contenu des fichiers

### cat - Afficher un fichier

```bash
# Afficher le contenu complet
cat mon_fichier.txt

# Afficher avec numéros de lignes
cat -n fichier.txt
```

### less - Afficher page par page

```bash
# Afficher un fichier volumineux
less gros_fichier.log

# Commandes dans less :
# - Espace : page suivante
# - b : page précédente
# - q : quitter
# - /motif : rechercher
# - n : prochain résultat
```

### head et tail - Début et fin d'un fichier

```bash
# Afficher les 10 premières lignes
head fichier.txt

# Afficher les 20 premières lignes
head -n 20 fichier.txt

# Afficher les 10 dernières lignes
tail fichier.txt

# Suivre un fichier en temps réel (logs)
tail -f /var/log/syslog
```

### wc - Compter lignes, mots, caractères

```bash
# Compter lignes, mots et caractères
wc fichier.txt

# Compter uniquement les lignes
wc -l fichier.txt

# Compter uniquement les mots
wc -w fichier.txt
```

## 2.4 Recherche de fichiers

### find - Rechercher des fichiers

```bash
# Rechercher par nom
find /home -name "*.txt"

# Rechercher dans le répertoire courant
find . -name "fichier.txt"

# Rechercher par type (f = fichier, d = répertoire)
find . -type d -name "Documents"

# Rechercher par taille
find . -size +100M

# Rechercher par date de modification
find . -mtime -7  # modifiés il y a moins de 7 jours
```

### locate - Recherche rapide

```bash
# Rechercher un fichier (doit être indexé)
locate mon_fichier

# Mettre à jour la base de données
sudo updatedb
```

## 2.5 Exercices pratiques

### Exercice 1 : Navigation
1. Ouvrez un terminal
2. Affichez votre répertoire courant avec `pwd`
3. Listez les fichiers avec `ls -la`
4. Créez un dossier nommé "exercices_linux" avec `mkdir`
5. Entrez dans ce dossier avec `cd`
6. Vérifiez votre position avec `pwd`

### Exercice 2 : Manipulation de fichiers
1. Créez un fichier vide nommé "test.txt" avec `touch`
2. Copiez ce fichier vers "test_copie.txt"
3. Renommez le fichier original en "mon_fichier.txt"
4. Listez les fichiers pour vérifier
5. Supprimez les fichiers avec `rm`

### Exercice 3 : Lecture de fichiers
1. Affichez le contenu de `/etc/os-release` avec `cat`
2. Utilisez `head` et `tail` pour voir le début et la fin
3. Parcourez un fichier volumineux avec `less`

### Exercice 4 : Recherche
1. Utilisez `find` pour rechercher tous les fichiers ".txt" dans votre dossier personnel
2. Comparez avec la commande `locate` (si disponible)

## 2.6 Résumé

| Commande | Description |
|----------|--------------|
| `pwd` | Affiche le répertoire courant |
| `ls` | Liste les fichiers |
| `cd` | Change de répertoire |
| `mkdir` | Crée un répertoire |
| `touch` | Crée un fichier vide |
| `cp` | Copie des fichiers |
| `mv` | Déplace ou renomme |
| `rm` | Supprime des fichiers |
| `cat` | Affiche le contenu d'un fichier |
| `less` | Affiche page par page |
| `head` | Affiche le début d'un fichier |
| `tail` | Affiche la fin d'un fichier |
| `find` | Recherche de fichiers |

Ces commandes sont les fondations de l'utilisation de Linux. Pratiquez-les régulièrement pour devenir à l'aise avec le terminal !

---

*Dans la prochaine leçon, nous aborderons les permissions des fichiers.*
