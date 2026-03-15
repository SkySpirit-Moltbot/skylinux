# Leçon 15 : Redirections et Pipes

Dans cette leçon, tu vas maîtriser le flux de données sous Linux : redirections et pipes. Ces outils sont fondamentaux pour traiter des données et créer des scripts puissants.

---

## 1. Entrée et sortie standard

### Les 3 flux

| Flux | Numéro | Description | Par défaut |
|------|--------|-------------|------------|
| **STDIN** | 0 | Entrée clavier | Clavier |
| **STDOUT** | 1 | Sortie normale | Écran |
| **STDERR** | 2 | Erreurs | Écran |

### Exemple simple

```bash
cat              # Lit depuis stdin, écrit vers stdout
ls > fichier     # Redirige stdout vers fichier
ls 2> erreur    # Redirige stderr vers erreur
```

---

## 2. Redirections de sortie

### > - Rediriger (écraser)

```bash
# Écrire dans un fichier (écrase)
echo "Bonjour" > fichier.txt
ls -l > liste.txt

# Rediriger stderr (2>)
ls /inexistant 2> erreurs.txt
```

### >> - Rediriger (ajouter)

```bash
# Ajouter à la fin
echo "Ligne 1" > log.txt
echo "Ligne 2" >> log.txt

# Logger avec horodatage
echo "$(date): Démarrage" >> /var/log/mon_script.log
```

### 2>&1 - Combiner stdout et stderr

```bash
# Tout rediriger vers un fichier
commande > tout.log 2>&1
commande &> tout.log              # Syntaxe courte

# Vers /dev/null (jeter)
commande > /dev/null 2>&1
```

---

## 3. Redirections d'entrée

### < - Entrée depuis fichier

```bash
# Au lieu de taper au clavier
cat < fichier.txt

# Trier un fichier
sort < fichier.txt

# Utiliser un fichier comme entrée
commande < input.txt
```

### << - Here Document

```bash
# Entrée multiligne
cat << EOF
Ligne 1
Ligne 2
Ligne 3
EOF

# Avec変数
NOM="David"
cat << EOF
Bonjour $NOM
Bienvenue!
EOF

# Sans expansion (ici-document)
cat << 'EOF'
$LITERAL ne sera pas expansé
EOF
```

### <<< - Here String

```bash
# Une seule ligne
wc -w <<< "Bonjour le monde"
# Résultat: 3

read -r nom <<< "Alice"
echo "Salut $nom"
```

---

## 4. Pipes (tubes)

### | - Chaîner les commandes

Le **pipe** envoie la sortie d'une commande vers l'entrée de la suivante.

```bash
# Trier et afficher
ls | sort

# Compter les fichiers
ls | wc -l

# Chercher dans la sortie
ls | grep ".txt"

# Afficher les 10 premières lignes
ls -l | head -10
```

### Exemples pratiques

```bash
# Voir processus qui utilisent le plus de mémoire
ps aux --sort=-%mem | head -10

# Compter les lignes de code
find . -name "*.py" | xargs wc -l | tail -1

# Dernier utilisateur connecté
last | head -1

# Rechercher et limiter
dmesg | grep -i error | tail -5

# Pipeline complexe
cat /var/log/syslog | grep -i error | sort | uniq -c | sort -rn | head -10
```

---

## 5. Commandes de traitement de texte

### head - Début du fichier

```bash
head fichier.txt              # 10 premières lignes
head -n 20 fichier.txt        # 20 premières lignes
head -c 100 fichier.txt       # 100 premiers octets
```

### tail - Fin du fichier

```bash
tail fichier.txt              # 10 dernières lignes
tail -n 20 fichier.txt        # 20 dernières lignes
tail -f fichier.log           # Suivre en temps réel
tail -f /var/log/syslog       # Logger en direct
```

### wc - Compter

```bash
wc -l fichier                # Nombre de lignes
wc -w fichier                # Nombre de mots
wc -c fichier                # Nombre d'octets
wc fichier                   # Les trois
```

### sort - Trier

```bash
sort fichier.txt             # Trier alphabétiquement
sort -n fichier.txt          # Trier numériquement
sort -r fichier.txt          # Inverser l'ordre
sort -u fichier.txt          # Trier et supprimer doublons
sort -k2 fichier.txt         # Trier par colonne 2
```

### uniq - Lignes uniques

```bash
uniq fichier.txt              # Supprimer doublons adjacents
uniq -c fichier.txt           # Avec compteur
uniq -d fichier.txt          # Afficher seulement doublons
sort fichier | uniq          # Tous les uniques (triés)
```

### cut - Extraire des colonnes

```bash
cut -d: -f1 /etc/passwd      # Première colonne (séparateur :)
cut -c1-10 fichier.txt        # Caractères 1 à 10
cut -f1,3 fichier.tsv        # Colonnes 1 et 3
```

### awk - Traitement puissant

```bash
# Afficher la première colonne
awk '{print $1}' fichier.txt

# Avec séparateur
awk -F: '{print $1, $5}' /etc/passwd

# Condition
awk '$3 > 1000' /etc/passwd

# Somme
awk '{sum+=$1} END {print sum}' fichier.txt
```

### sed - Éditeur de flux

```bash
# Remplacer
sed 's/ancien/nouveau/' fichier.txt

# Remplacer global
sed 's/ancien/nouveau/g' fichier.txt

# Supprimer lignes
sed '/motif/d' fichier.txt

# Numérotation
sed = fichier.txt | sed 'N;s/\n/\t/'
```

---

## 6. tee - Dupliquer le flux

### Afficher ET sauvegarder

```bash
# Afficher + écrire dans un fichier
commande | tee fichier.txt

# Ajouter + afficher
commande | tee -a fichier.txt

# Pipeline avec log
make | tee build.log
```

---

## 7. xargs - Construire des commandes

### Construire des arguments

```bash
# Supprimer tous les fichiers .tmp
find . -name "*.tmp" | xargs rm

# Confirmation
find . -name "*.tmp" | xargs -p rm

# Limiter par lot
cat fichiers.txt | xargs -n 10 commande

# Avec placeholder
find . -name "*.txt" | xargs -I {} cp {} /backup/
```

---

## 8. Exercices pratiques

### Exercice 1 : Pipeline de logs
```bash
# Rechercher les erreurs dans les logs
tail -f /var/log/syslog | grep -i error
```

### Exercice 2 : Statistiques
```bash
# Compter les fichiers par extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

### Exercice 3 : Nettoyage
```bash
# Supprimer les fichiers de plus de 30 jours
find /tmp -mtime +30 | xargs rm -rf
```

### Exercice 4 : Surveillance
```bash
# Voir les plus gros fichiers
du -sh * | sort -rh | head -10
```

---

## 9. Tableaux résumés

### Symboles de redirection

| Symbole | Description |
|---------|-------------|
| `>` | Rediriger stdout (écrase) |
| `>>` | Rediriger stdout (ajoute) |
| `2>` | Rediriger stderr |
| `2>&1` | Stdout + stderr |
| `<` | Rediriger stdin |
| `<<` | Here document |
| `<<<` | Here string |
| `|` | Pipe |

### Commandes utiles avec pipes

| Commande | Utilisation |
|----------|-------------|
| `head` | Début du fichier |
| `tail` | Fin du fichier |
| `grep` | Rechercher |
| `sort` | Trier |
| `uniq` | Dupliquer |
| `wc` | Compter |
| `cut` | Colonnes |
| `awk` | Traitement |
| `sed` | Édition |
| `tee` | Dupliquer |

---

## 10. Examples avancés

### Transformer des données

```bash
# Extraire et formater
cat /etc/passwd | awk -F: '{print $1 ":" $5}' | sort

# Compter par groupe
groups * 2>/dev/null | cut -d: -f2 | sort | uniq -c

# Nettoyer et dédoublonner
cat data.txt | sed '/^$/d' | sort | uniq > clean.txt
```

### Surveillance système

```bash
# Top 10 processus mémoire
ps aux --sort=-%mem | head -11

# Connexions réseau par IP
netstat -tn | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn

# Fichiers les plus modifiés récemment
find . -type f -mmin -60 | sort -k -M
```

---

Maîtrise les redirections et pipes pour devenir un ninja du terminal ! 🔥