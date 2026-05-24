# Leçon 51 : cut — Extraire des colonnes de texte

`cut` est l'outil idéal pour découper du texte structuré en colonnes : fichiers CSV, logs, sortie de commandes formatées.

## 1. Le principe

`cut` découpe chaque ligne selon un délimiteur et extrait les colonnes demandées.

```bash
# Syntaxe
cut -d 'délimiteur' -f colonnes fichier

# Exemple : extraire le 1er champ d'un CSV
cut -d ',' -f 1 utilisateurs.csv
```

## 2. Découper par caractère (sans délimiteur)

```bash
# Extraire les 3 premiers caractères de chaque ligne
echo "abcdef" | cut -c 1-3
# → abc

# Extraire du 5e caractère jusqu'à la fin
echo "abcdefgh" | cut -c 5-
# → efgh

# Extraire le caractère 2 uniquement
echo "abc" | cut -c 2
# → b
```

## 3. Découper par champ avec délimiteur

```bash
# Le fichier /etc/passwd utilise ':' comme séparateur
# Format: user:x:uid:gid:comment:home:shell

# Extraire tous les noms d'utilisateurs (champ 1)
cut -d ':' -f 1 /etc/passwd

# Extraire le shell par défaut (champ 7)
cut -d ':' -f 7 /etc/passwd

# Extraire plusieurs champs
cut -d ':' -f 1,7 /etc/passwd

# Changer le délimiteur en sortie
cut -d ':' -f 1,7 --output-delimiter=' → ' /etc/passwd
```

## 4. Cas pratiques

```bash
# Afficher l'heure depuis la commande date
date | cut -d ' ' -f 4

# Extraire une colonne d'un fichier CSV
cut -d ',' -f 2,3 ventes.csv

# Trouver tous les utilisateurs avec bash comme shell
grep bash /etc/passwd | cut -d ':' -f 1

# Afficher les permissions (1er champ) de ls -l
ls -l | tail -n +2 | cut -c 1-10

# Extraire une plage de caractères : du 5e au 12e
echo "1234567890ABCDEF" | cut -c 5-12
```

## 5. Exercices pratiques

1. **Passwd** — Affiche la liste des utilisateurs avec leur répertoire home (`/etc/passwd`, champs 1 et 6)
2. **CSV** — Crée un fichier `notes.csv` avec "Nom,Note,Matière" et extrais la colonne des notes
3. **Logs** — Dans un fichier de log avec des colonnes séparées par des espaces, extrais la 3e colonne
