# Leçon 47 : AWK — Manipuler et transformer du texte

Dans cette lecon, tu vas decouvrir **AWK**, un langage incruste设计和 un outil en ligne de commande extrmement puissant pour manipuler du texte structure. Si `grep` selectionne des lignes et `sed` remplace du texte, **AWK** va bien plus loin : il permet d'appliquer des calculs, des conditions, des formats et de generer des rapports structures — le tout en une seule commande.

Tu verras egalement le cousin de AWK : **GAWK** (GNU AWK), qui est la version la plus courante sur Linux aujourd'hui.

---

## 1. Qu'est-ce que AWK ?

AWK est ne en 1977 aux laboratoires Bell. Son nom vient des initiales de ses createurs : **Aho, Weinberger et Kernighan**.

Concu a l'origine pour traiter des fichiers textes structures (comme des tableaux ou des logs), AWK lit un fichier ligne par ligne, divise chaque ligne en **champs** (colonnes) separes par des espaces ou un separateur personnalise, et execute des **actions** sur chaque ligne correspondant a un **motif**.

La syntaxe de base est simple :

```bash
awk 'motif { action }' fichier
```

- **motif** : condition que la ligne doit verifier (ou `BEGIN` / `END` speciales)
- **action** : ce qu'on fait quand le motif correspond
- **fichier** : le fichier a traiter (ou `-` pour l'entree standard)

---

## 2. Les champs ($1, $2, ... $NF)

Chaque ligne est automatiquement divisee en champs. AWK utilise :

| Variable | Signification |
|----------|---------------|
| `$0` | La ligne entiere |
| `$1` | Le 1er champ |
| `$2` | Le 2e champ |
| `$3` ... | Les champs suivants |
| `$NF` | Le dernier champ (NF = Number of Fields) |

**Exemple** — Voici un fichier `employes.txt` :

```
Alice  Administrateur  4500
Bob    Developpeur      6200
Claire Technicien      3800
David  Developpeur      6100
Emma   Manager          7500
```

Afficher le nom et le salaire (1er et 3e champ) :

```bash
awk '{ print $1, $3 }' employes.txt
```

**Resultat :**

```
Alice 4500
Bob 6200
Claire 3800
David 6100
Emma 7500
```

---

## 3. Le separateur de champs (option -F)

Par defaut, AWK utilise l'espace comme separateur. Pour un fichier CSV (separateur `;`) :

```bash
awk -F';' '{ print $1, $3 }' employes.csv
```

On peut aussi changer le separateur avec `BEGIN { FS = ";" }` :

```bash
awk 'BEGIN { FS = ":" } { print $1, $NF }' /etc/passwd | head -5
```

---

## 4. Les conditions et motifs

### Motif sur un champ

Afficher uniquement les developpeurs :

```bash
awk '$2 == "Developpeur" { print $1, $3 }' employes.txt
```

**Resultat :**

```
Bob 6200
David 6100
```

### Comparaison numerique

Afficher les employes gagnant plus de 5000 :

```bash
awk '$3 > 5000 { print $1, $3 }' employes.txt
```

**Resultat :**

```
Bob 6200
David 6100
Emma 7500
```

### Motif texte (expression reguliere)

Afficher les lignes commençant par "D" :

```bash
awk '$1 ~ /^D/ { print $0 }' employes.txt
```

**Resultat :**

```
David  Developpeur  6100
```

---

## 5. BEGIN et END — Traiter avant et apres

- `BEGIN` : s'execute **avant** le traitement du fichier
- `END` : s'execute **apres** le traitement du fichier

Calculer la somme totale des salaries :

```bash
awk 'BEGIN { total = 0 }
     { total += $3 }
     END { print "Total salaries :", total }' employes.txt
```

**Resultat :**

```
Total salaries : 28100
```

Autre exemple — ajouter un en-tete :

```bash
awk 'BEGIN { print "Nom", "Salaire" }
     { print $1, $3 }
     END { print "--- Fin du rapport ---" }' employes.txt
```

---

## 6. Les variables integrees

AWK fournit des variables predefinies tres utiles :

| Variable | Description |
|----------|-------------|
| `NF` | Nombre de champs dans la ligne courante |
| `NR` | Numero de la ligne courante (Number of Record) |
| `FNR` | Numero de ligne dans le fichier courant |
| `FS` | Separateur de champs (Field Separator) |
| `RS` | Separateur d'enregistrements (Record Separator) |
| `OFS` | Separateur de champs en sortie (Output FS) |
| `ORS` | Separateur d'enregistrements en sortie |

**Exemple** — Numeroter les lignes :

```bash
awk '{ print NR, $0 }' employes.txt
```

**Resultat :**

```
1 Alice  Administrateur  4500
2 Bob    Developpeur      6200
3 Claire Technicien       3800
4 David  Developpeur      6100
5 Emma   Manager          7500
```

---

## 7. Les fonctions

AWK dispose de nombreuses fonctions predefinies :

| Fonction | Description |
|----------|-------------|
| `length()` | Longueur de la chaene |
| `substr(s, d, l)` | Extraire une sous-chaene |
| `toupper()` / `tolower()` | Changer la casse |
| `sprintf()` | Formater une chaene |
| `int()` | Partie entiere |
| `rand()` / `srand()` | Nombres aleatoires |
| ` systime()` | Timestamp Unix |

**Exemple** — Mettre les noms en majuscules :

```bash
awk '{ print toupper($1), $3 }' employes.txt
```

**Resultat :**

```
ALICE 4500
BOB 6200
CLAIRE 3800
DAVID 6100
EMMA 7500
```

---

## 8. Les tableaux associatifs

AWK supporte des **tableaux associatifs** (cles = chaines) :

```bash
awk '{ salaries[$2] += $3 }
     END { for (dept in salaries)
           print dept, salaries[dept] }' employes.txt
```

**Resultat :**

```
Administrateur 4500
Developpeur 12300
Technicien 3800
Manager 7500
```

---

## 9. Formatage avec printf

Pour un controle precis du formatage, utilise `printf` :

```bash
awk '{ printf "%-10s %-15s %6d\n", $1, $2, $3 }' employes.txt
```

| Format | Signification |
|--------|---------------|
| `%-10s` | Chaene, justifie a gauche, 10 caracteres |
| `%6d` | Entier, justifie a droite, 6 caracteres |

**Resultat :**

```
Alice      Administrateur    4500
Bob        Developpeur        6200
Claire     Technicien         3800
David      Developpeur        6100
Emma       Manager            7500
```

---

## 10. Utiliser un script AWK dans un fichier

Quand la logique devient complexe, place-la dans un fichier `.awk` :

```bash
# rapport.awk
BEGIN {
    print "=== Rapport des salaries ==="
    FS = " "
}
$3 > 5000 {
    count++
    total += $3
    printf "%-10s %6d\n", $1, $3
}
END {
    printf "\n%d employes > 5000 | Total : %d\n", count, total
}
```

Execute-le avec :

```bash
awk -f rapport.awk employes.txt
```

---

## 11. Combiner AWK avec des pipes

AWK brille aussi en combinaison avec d'autres commandes :

Nombre de connexions SSH par IP dans les logs :

```bash
grep "sshd" /var/log/auth.log | awk '{ print $NF }' | sort | uniq -c | sort -rn | head -10
```

Afficher la memoire libre toutes les 2 secondes (3 iterations) :

```bash
free -m | awk 'NR==2{print "Memoire libre : "$7 " MB"}' 
```

Extraire les colonnes 1 et 5 d'un `ls -l` (taille et nom) :

```bash
ls -l | awk '{ print $5, $9 }' | tail -n +2
```

---

## 12. Exercice pratique

**Contexte** : Tu as un fichier `logs.txt` avec le format suivant :

```
2026-04-08 10:15:22 GET /index.html 200
2026-04-08 10:15:45 POST /api/login 401
2026-04-08 10:16:03 GET /index.html 200
2026-04-08 10:16:28 GET /dashboard 302
2026-04-08 10:17:01 GET /api/users 200
2026-04-08 10:17:33 POST /api/login 200
2026-04-08 10:18:05 GET /index.html 200
2026-04-08 10:18:22 GET /dashboard 404
2026-04-08 10:19:11 GET /api/users 200
```

**Objectifs** (realise-les avec AWK) :

1. Affiche uniquement les lignes avec un code HTTP 200 (OK)
2. Affiche la date, l'heure et l'URL de chaque requete
3. Compte combien de fois chaque URL apparait
4. Affiche le nombre total de requetes et combien ont retourne 200

**Corrige** :

```bash
# 1. Lignes avec code 200
awk '$NF == 200 { print $0 }' logs.txt

# 2. Date, heure et URL
awk '{ print $1, $2, $4 }' logs.txt

# 3. Compteur par URL
awk '{ urls[$4]++ } END { for (u in urls) print urls[u], u }' logs.txt

# 4. Total et compteur 200
awk 'BEGIN { total=0; ok=0 }
     { total++; if ($NF == 200) ok++ }
     END { print "Total :", total, "| 200 OK :", ok }' logs.txt
```

---

## Resumé

| Concept | Description |
|---------|-------------|
| `$0, $1, $NF` | Champs d'une ligne |
| `-F` | Separateur de champs personnalise |
| `NR, NF` | Numeros de ligne et nombre de champs |
| `BEGIN / END` | Actions avant / apres le fichier |
| `printf` | Formatage personnalise |
| `-f script.awk` | Executer un script AWK depuis un fichier |
| Tableaux associatifs | Agrger, compter, grouper |

**A retenir** : AWK est l'outil ideal pour tout travail tabulaire ou structure. La prochaine fois que tu dois extraire une colonne, calculer une somme ou generer un rapport depuis un fichier texte, pense d'abord a AWK — tu gagneras du temps et tu ecriras moins de code.

---

*AWK complete parfaitement `grep` et `sed`. Si tu as suivi les lecons 9 (recherche) et 15 (redirections/pipes), tu as maintenant un arsenal complet pour manipuler du texte sous Linux.*
