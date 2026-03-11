# Leçon 16 : Éditeurs de texte en ligne de commande

## Introduction

Sous Linux, vous serez souvent amenés à modifier des fichiers de configuration ou des scripts. Deux éditeurs sont disponibles directement dans le terminal : **Nano** (simple) et **Vim** (puissant). Cette leçon vous introduit aux deux.

---

## Nano : l'éditeur simple

Nano est idéal pour les débutants. Il affiche les raccourcis en bas de l'écran.

### Ouvrir/créer un fichier

```bash
nano fichier.txt
```

### Raccourcis utiles

- **Ctrl + O** : Enregistrer (WriteOut)
- **Ctrl + X** : Quitter
- **Ctrl + W** : Rechercher
- **Ctrl + K** : Couper la ligne
- **Ctrl + U** : Coller

### Exemple

```bash
nano ~/mon-script.sh
# Écrit ton script, puis Ctrl+O pour sauvegarder, Ctrl+X pour quitter
```

---

## Vim : l'éditeur puissant

Vim est plus complexe mais très puissant. Il fonctionne avec des **modes**.

### Modes de Vim

1. **Mode normal** : Par défaut, pour naviguer et exécuter des commandes
2. **Mode insertion** : Pour taper du texte (touche `i`)
3. **Mode commande** : Pour des commandes avancées (touche `:`)

### Commandes de base

```bash
vim fichier.txt        # Ouvrir un fichier
i                      # Passer en mode insertion (écrire)
Échap                  # Retourner en mode normal
:wq                    # Enregistrer et quitter
:q!                    # Quitter sans enregistrer
dd                     # Couper une ligne
p                      # Coller
/string                # Rechercher "string"
```

### Vimtutor

Pour pratiquer Vim :

```bash
vimtutor
```

---

## Quel éditeur choisir ?

| Critère | Nano | Vim |
|---------|------|-----|
| Difficulté | Facile | Moyen |
| Puissance | Basique | Très puissant |
| Idéal pour | Débutants,快速修改 | Fichiers complexes, développeurs |

---

## Exercice pratique

1. Crée un fichier nommé `test.txt` avec Nano contenant quelques lignes de texte
2. Ouvre ce même fichier avec Vim, ajoute du texte et enregistre
3. Utilise `vimtutor` pour faire les 2 premières leçons

---

## Résumé

- **Nano** : éditeur simple, parfait pour les débutants
- **Vim** : éditeur puissant avec modes de fonctionnement
- `nano fichier` pour éditer facilement
- `vim fichier` pour une édition avancée
- `vimtutor` pour apprendre Vim pas à pas
