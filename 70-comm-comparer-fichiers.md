# Leçon 70 : comm — Comparer deux fichiers ligne par ligne

`comm` compare deux fichiers triés et affiche les lignes uniques à chacun et les lignes communes.

## 1. Prérequis : fichiers triés

```bash
# ⚠️ comm exige des fichiers TRIÉS !
# Sinon, résultat faux.

# Toujours trier avant :
sort fichier1.txt > f1_trie.txt
sort fichier2.txt > f2_trie.txt
comm f1_trie.txt f2_trie.txt
```

## 2. Comprendre les 3 colonnes

```bash
comm fichier1.txt fichier2.txt
# → Colonne 1 : lignes UNIQUES à fichier1
# → Colonne 2 : lignes UNIQUES à fichier2
# → Colonne 3 : lignes COMMUNES
```

Exemple :

```bash
echo -e "Alice\nBob\nCharlie" > equipe_a.txt
echo -e "Bob\nCharlie\nDavid" > equipe_b.txt

comm equipe_a.txt equipe_b.txt
# Alice                  ← uniquement dans A
#         David          ← uniquement dans B
#                 Bob    ← commun
#                 Charlie← commun
```

## 3. Masquer des colonnes

```bash
# -1 : masquer la colonne 1 (lignes uniques à fichier1)
comm -1 f1.txt f2.txt
# → uniquement fichier2 + commun

# -2 : masquer la colonne 2
comm -2 f1.txt f2.txt
# → uniquement fichier1 + commun

# -3 : masquer la colonne 3
comm -3 f1.txt f2.txt
# → uniquement fichier1 + uniquement fichier2

# Combiner : afficher SEULEMENT ce qui est commun
comm -12 f1.txt f2.txt
# → uniquement les lignes communes

# Afficher SEULEMENT ce qui est unique à fichier1
comm -23 f1.txt f2.txt
# → lignes dans f1 mais pas dans f2

# Afficher SEULEMENT ce qui est unique à fichier2
comm -13 f1.txt f2.txt
```

## 4. Cas pratiques

```bash
# Quels paquets sont installés sur serveur1 mais pas sur serveur2 ?
ssh serveur1 'dpkg -l | awk "{print \$2}" | sort' > paquets_srv1.txt
ssh serveur2 'dpkg -l | awk "{print \$2}" | sort' > paquets_srv2.txt
comm -23 paquets_srv1.txt paquets_srv2.txt

# Quels utilisateurs sont sur les deux machines ?
comm -12 <(sort /etc/passwd | cut -d: -f1) <(ssh autre 'sort /etc/passwd | cut -d: -f1')

# Comparer deux backups de configuration
comm -3 <(sort config_avant.txt) <(sort config_apres.txt)
```

## 5. comm avec des flux (sans fichiers temporaires)

```bash
# La syntaxe <(commande) crée un pseudo-fichier avec la sortie de la commande
comm -23 <(sort liste1.txt) <(sort liste2.txt)

# Comparer deux dossiers (les noms de fichiers)
comm -23 <(ls dossier1/ | sort) <(ls dossier2/ | sort)
```

## 6. Résumé des options

| Option | Affiche |
|--------|---------|
| `comm f1 f2` | Les 3 colonnes |
| `comm -1 f1 f2` | Uniques f2 + commun |
| `comm -2 f1 f2` | Uniques f1 + commun |
| `comm -3 f1 f2` | Uniques f1 + uniques f2 |
| `comm -12 f1 f2` | Commun seulement |
| `comm -23 f1 f2` | Uniques f1 seulement |
| `comm -13 f1 f2` | Uniques f2 seulement |

## 7. Exercices pratiques

1. **Base** — Crée deux fichiers triés et compare-les avec `comm`
2. **Commun** — Affiche uniquement les lignes communes avec `comm -12`
3. **Différence** — Trouve les lignes présentes dans le fichier A mais pas dans le B avec `comm -23`
4. **Dossiers** — Compare le contenu de deux dossiers avec `comm -3`
