# Leçon 40 : Git - Gestion de versions

Dans cette leçon, tu vas découvrir **Git**, l'outil de gestion de versions le plus utilisé au monde. Que tu développes du code, des configs ou des scripts, Git te permet de suivre chaque modification, de revenir en arrière et de travailler à plusieurs sur le même projet — sans jamais perdre de travail.

---

## 1. Pourquoi un outil de gestion de versions ?

Voici ce qui se passe sans Git :

```
Tu modifies script.sh
  → Tu ajoutes une功能
  → Ça casse tout
  → Tu n'as plus la version qui marchait
  → Panique
```

**Avec Git**, chaque modification est enregistrée. Tu peux revenir à n'importe quel moment, voir exactement ce qui a changé, et travailler avec d'autres personnes sans écraser leur travail.

---

## 2. Les concepts de base

### Le dépôt (Repository)

Un **dépôt** Git, c'est un dossier dans lequel Git suit toutes les modifications. Chaque fichier est surveillé.

```
Mon projet/          ← dossier normal
Mon projet/          ← dépôt Git (contient .git/)
  .git/              ← ici Git stocke l'historique
  fichier1.txt
  fichier2.sh
```

### Les trois états d'un fichier

Chaque fichier dans un dépôt Git peut être dans l'un de ces états :

```
┌──────────────┐   git add    ┌──────────────┐  git commit   ┌──────────────┐
│   Modifié    │ ──────────→  │  Indexé      │ ───────────→  │  Validé      │
│ (modified)   │              │ (staged)     │              │ (committed)  │
└──────────────┘              └──────────────┘              └──────────────┘
     Ton fichier              Ce qui sera              Ce qui est
     tel qu'il est           validé dans              enregistré dans
     maintenant               le prochain              l'historique
                               commit
```

---

## 3. Créer un dépôt et première validation

### Initialiser Git

```bash
cd ~/mon-projet
git init
```

Résultat :
```
Initialized empty Git repository in /home/toi/mon-projet/.git/
```

Un dossier `.git/` vient d'être créé. Git surveille maintenant ce dossier.

### Vérifier l'état

```bash
git status
```

Quand tu commences, tout est vide :
```
On branch master

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

### Créer un premier fichier

```bash
echo "Bienvenue dans mon projet" > README.txt
git status
```

```
Untracked files:
  README.txt
```

**"Untracked"** = Git voit le fichier, mais ne le surveille pas encore.

### Ajouter au suivi (stage)

```bash
git add README.txt
git status
```

```
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.txt
```

Le fichier est maintenant **indexé** — prêt à être validé.

### Valider (commit)

```bash
git commit -m "Ajout du fichier README"
```

```
[master (root-commit) a1b2c3d] Ajout du fichier README
 1 file changed, 1 insertion(+)
 create mode 100644 README.txt
```

`-m "message"` = une description courte de ce que tu as fait. C'est obligatoire.

---

## 4. Le cycle de travail quotidien

Tu modifies des fichiers toute la journée. Voici le cycle :

```bash
# 1. Tu modifies tes fichiers
nano config.txt

# 2. Tu vérifies ce qui a changé
git status        # quels fichiers modifiés
git diff          # détails des changements (lignes ajoutées/enlevées)

# 3. Tu ajoutes les fichiers modifiés à l'index
git add config.txt

# 4. Tu valides avec un message clair
git commit -m "Mise à jour de la configuration serveur"
```

### La commande git diff

Voir exactement ce qui a changé :

```bash
git diff              # montre les modifications NON indexées
git diff --staged     # montre les modifications indexées (prêtes à commit)
```

Exemple de sortie :
```
- ancienne_ligne
+ nouvelle_ligne_plus_belle
```

Le `-` = ligne enlevée, le `+` = ligne ajoutée.

---

## 5. L'historique des commits

### Voir le journal

```bash
git log
```

```
commit a1b2c3d4e5f6 (HEAD -> master)
Author: Ton Nom <ton@email.com>
Date:   Sun Mar 29 12:00:00 2026

    Mise à jour de la configuration serveur

commit 9f8e7d6c5b4a
Author: Ton Nom <ton@email.com>
Date:   Sat Mar 28 10:30:00 2026

    Ajout du fichier README
```

Chaque commit a un **hash** unique (ex: `a1b2c3d4`). Tu peux revenir à n'importe lequel.

### En une ligne (plus compact)

```bash
git log --oneline
```

```
a1b2c3d Mise à jour de la configuration serveur
9f8e7d6 Ajout du fichier README
```

---

## 6. Les branches (branches)

Une **branche**, c'est une copie parallèle du projet. Tu peux expérimenter sans toucher à la version principale.

```
          master (branche principale)
            │
            ▼
    ┌───────────────┐
    │ Commit A      │ ← HEAD (position actuelle)
    │ Commit B      │
    │ Commit C      │
    └───────────────┘
            │
            └── experimental (branche secondaire)
                │
                ▼
          ┌───────────────┐
          │ Commit D      │ ← nouvelles modifications
          │ Commit E      │
          └───────────────┘
```

### Créer une branche

```bash
git branch experimental        # crée la branche
git checkout experimental       # se placer dessus
```

Ou en une seule commande :
```bash
git checkout -b experimental    # créer ET se placer dessus
```

### Travailler sur une branche

```bash
echo "fonctionnalité expérimentale" > feature.txt
git add feature.txt
git commit -m "Ajout d'une fonctionnalité expérimentale"
```

### Revenir à la branche principale

```bash
git checkout master
```

Le fichier `feature.txt` disparaît de ton dossier — il est toujours dans la branche `experimental`.

### Fusionner une branche (merge)

```bash
git checkout master
git merge experimental
```

Git combine les deux branches. Si tout va bien, c'est un **fast-forward** (avance rapide). Si des fichiers sont en conflit, Git te demande de choisir.

---

## 7. Git avec un serveur distant (GitHub)

Quand ton projet est sur GitHub, tu peux le synchroniser.

### Cloner un dépôt existant

```bash
git clone https://github.com/utilisateur/depot.git
```

Cela télécharge tout le projet + l'historique complet.

### Pousser tes modifications

```bash
git push origin master
```

`origin` = le serveur distant (GitHub, GitLab, etc.)
`master` = la branche que tu pousses

### Récupérer les mises à jour

```bash
git pull origin master
```

---

## 8. Commandes utiles du quotidien

```bash
# État du dépôt
git status              # quoi de modifié
git diff                # détails des changements
git log --oneline       # historique concis

# Ajouter et valider
git add fichier.txt     # indexer un fichier précis
git add .               # indexer TOUS les fichiers modifiés
git commit -m "Message" # valider avec message

# Branches
git branch              # lister les branches
git checkout -b nom     # créer et basculer
git checkout master     # revenir à master
git merge branche       # fusionner une branche

# Synchronisation
git clone url            # télécharger un dépôt
git push origin master   # envoyer sur le serveur
git pull origin master   # récupérer du serveur
```

---

## Exercice pratique

**Objectif :** Transformer ton dossier de cours Linux en dépôt Git.

```bash
# 1. Va dans ton dossier de cours
cd ~/linux-debutant

# 2. Initialise Git
git init

# 3. Vérifie l'état
git status

# 4. Configure ton nom et email (une seule fois)
git config --global user.name "Ton Nom"
git config --global user.email "ton@email.com"

# 5. Ajoute tous les fichiers
git add .

# 6. Premier commit
git commit -m "Premier commit - cours Linux"

# 7. Vérifie l'historique
git log --oneline
```

**Bonus :**
```bash
# Modifie un fichier, puis vois la différence
nano README.md          # ajoute une ligne
git diff                # vois ce qui a changé
git add README.md
git commit -m "Ajout d'une description dans README"
```

---

## Résumé

| Concept | Définition |
|---------|-----------|
| `git init` | Créer un nouveau dépôt Git |
| `git add` | Ajouter un fichier à l'index (staging) |
| `git commit` | Valider les modifications |
| `git status` | Voir l'état du dépôt |
| `git diff` | Voir les changements non validés |
| `git log` | Voir l'historique des commits |
| `git branch` | Créer/lister des branches |
| `git checkout` | Basculer entre branches |
| `git merge` | Fusionner deux branches |
| `git push` | Envoyer sur le serveur |
| `git pull` | Récupérer du serveur |

**La règle d'or :** commit souvent, avec des messages clairs. Un commit = une modification cohérente et testée.

---

*Dans la prochaine leçon, nous verrons comment utiliser GitHub pour collaborer et sauvegarder ton code en ligne.*
