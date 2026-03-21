# Leçon 26 : Liens symboliques et liens durs

Dans cette leçon, tu vas découvrir comment créer des liens symboliques et des liens durs sous Linux. Ces mécanismes permettent d'accéder à un même fichier depuis plusieurs endroits sans le dupliquer.

---

## 1. Qu'est-ce qu'un lien ?

Sous Linux, tout est fichier. Chaque fichier stocké sur le disque a :
- Un **inode** : un numéro unique qui identifie le fichier sur le disque
- Un **nom de fichier** : le point d'accès dans un répertoire

Un **lien** est un second nom pointant vers le même inode. Cela permet d'accéder à un même fichier depuis plusieurs endroits sans le dupliquer.

Il existe deux types de liens :

| Type | Lien dur (hard link) | Lien symbolique (soft link / symlink) |
|------|---------------------|----------------------------------------|
| **Concept** | Un autre nom pour le même fichier | Un raccourci ou pointeur vers un autre fichier |
| **Inode** | Même inode | Inode différent |
| **Cross-filesystem** | ❌ Non | ✅ Oui |
| **Vers répertoire** | ❌ Non | ✅ Oui |
| **Vers fichier supprimé** | Continue de fonctionner | Devient cassé (lien mort) |

---

## 2. Liens durs (hard links)

### ln - Créer un lien dur

```bash
ln fichier_original lien_nouveau
```

**Exemple :**

```bash
# Créer un lien dur vers rapport.txt dans ~/Documents/
ln /home/david/rapport.txt /home/david/Documents/rapport_lien.txt
```

> ⚠️ Les deux noms pointent vers le **même contenu**. Modifier l'un modifie l'autre.

### ls - Vérifier l'inode commun

```bash
ls -li fichier_original lien_nouveau
```

Le `-i` affiche le numéro d'inode. Tu verras que les deux fichiers ont le **même inode**.

```bash
$ ls -li rapport.txt Documents/rapport_lien.txt
1234567 -rw-r--r-- 2 david david 4096 jan 15 10:00 rapport.txt
1234567 -rw-r--r-- 2 david david 4096 jan 15 10:00 Documents/rapport_lien.txt
```

Le chiffre `2` (deuxième colonne) est le **nombre de liens durs** vers cet inode. Tant qu'au moins un lien existe, le fichier n'est pas supprimé physiquement.

### rm - Supprimer un lien dur

```bash
rm lien_nouveau
```

Le fichier original reste intact. Les données ne sont vraiment effacées du disque que quand le **dernier lien dur** est supprimé.

---

## 3. Liens symboliques (symlinks)

### ln -s - Créer un lien symbolique

```bash
ln -s fichier_cible lien_symbolique
```

**Exemple :**

```bash
# Créer un raccourci vers mes-documents dans le bureau
ln -s /home/david/mes-documents /home/david/Bureau/mes-documents

# Créer un lien symbolique vers un script dans /usr/local/bin/
sudo ln -s /opt/mon-script.sh /usr/local/bin/mon-script
```

### ls - À quoi ça ressemble ?

```bash
$ ls -la Bureau/
lrwxrwxrwx 1 david david   20 jan 15 10:00 mes-documents -> /home/david/mes-documents
```

- `l` au début = c'est un lien symbolique
- La flèche `->` montre vers quoi le lien pointe

### test - Vérifier si un lien symbolique est cassé

```bash
# Tester le lien
test -e lien_symbolique && echo "OK" || echo "CASSÉ"

# Lister les liens cassés
find . -type l -xtype l
```

### rm - Supprimer un lien symbolique

```bash
rm lien_symbolique
```

> ⚠️ Pas de `/` à la fin du nom ! Sinon tu pourrais supprimer la **cible** par erreur.

---

## 4. Quand utiliser quoi ?

### Utilise le lien symbolique quand :
- Tu veux créer un **raccourci** vers un fichier ou répertoire
- La cible peut se trouver sur un **autre système de fichiers**
- Tu veux créer une liaison vers un **répertoire**
- La cible peut être modifiée ou supprimée (un lien mort est visible)

### Utilise le lien dur quand :
- Tu veux une **copie de sécurité intégrée** d'un fichier
- Les deux fichiers doivent **toujours** pointer vers le même contenu
- Tu travailles sur un **même système de fichiers**
- Tu veux que le fichier persiste même si l'original est renommé ou supprimé (tant qu'un lien reste)

### Exemple concret : la configuration système

```bash
# Ubuntu lie python3 vers python pour la compatibilité
$ ls -la /usr/bin/python
lrwxrwxrwx 1 root root   7 jan 15 10:00 python -> python3

# Python3 est le vrai exécutable
$ ls -la /usr/bin/python3
-rwxr-xr-x 1 root root 10480 jan 15 10:00 python3
```

---

## 5. Exercices pratiques

### Exercice 1 : Créer un lien symbolique vers un script

1. Crée un fichier `test.sh` dans ton dossier personnel :
```bash
echo 'echo "Bonjour depuis le script"' > ~/test.sh
chmod +x ~/test.sh
```

2. Crée un lien symbolique sur ton bureau :
```bash
ln -s ~/test.sh ~/Bureau/test_rapide.sh
```

3. Exécute le lien :
```bash
~/Bureau/test_rapide.sh
```

✅ Tu devrais voir "Bonjour depuis le script"

### Exercice 2 : Découvrir les liens dans /etc/

```bash
# Les paramètres régionaux sont souvent des liens symboliques
ls -la /etc/localtime

# Trouver tous les symlinks dans /etc
find /etc -type l -maxdepth 1 -ls
```

### Exercice 3 : Comprendre les liens durs

```bash
# Créer un fichier
echo "Contenu important" > ~/important.txt

# Créer un lien dur
ln ~/important.txt ~/backup_important.txt

# Vérifier l'inode commun
ls -li ~/important.txt ~/backup_important.txt

# Supprimer l'original
rm ~/important.txt

# Vérifier que la copie fonctionne encore
cat ~/backup_important.txt
```

### Exercice 4 : Identifier les liens cassés

```bash
# Créer un lien symbolique vers un fichier
echo "test" > ~/fichier_test.txt
ln -s ~/fichier_test.txt ~/lien_test

# Supprimer le fichier original
rm ~/fichier_test.txt

# Vérifier que le lien est maintenant cassé
test -e ~/lien_test && echo "OK" || echo "LIEN CASSÉ"
```

---

## 6. Résumé

| Commande | Description |
|----------|-------------|
| `ln original lien` | Créer un lien dur |
| `ln -s cible lien` | Créer un lien symbolique |
| `ls -li fichier` | Voir l'inode et le nombre de liens |
| `find . -type l` | Trouver tous les liens symboliques |
| `test -e lien` | Tester si un lien (symbole) est valide |

- Un **lien dur** = un nom supplémentaire pour le même fichier (même inode)
- Un **lien symbolique** = un raccourci vers un autre chemin (inode différent)
- Les liens symboliques peuvent traverser les systèmes de fichiers et pointer vers des répertoires
- Un lien symbolique cassé apparaît clairement ; un lien dur reste valide tant qu'un nom existe encore
