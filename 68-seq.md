# Leçon 68 : seq — Générer des suites de nombres

`seq` génère des séquences numériques. Parfait pour les boucles, la création de fichiers de test, ou la génération de listes.

## 1. Séquences simples

```bash
# De 1 à N
seq 5
# → 1
# → 2
# → 3
# → 4
# → 5

# De A à B
seq 5 10
# → 5
# → 6
# ...
# → 10

# De A à B par pas de C
seq 1 2 10
# → 1
# → 3
# → 5
# → 7
# → 9
```

## 2. Changer le séparateur

```bash
# Par défaut : saut de ligne
seq 3
# 1
# 2
# 3

# Avec -s : séparateur personnalisé
seq -s ", " 5
# → 1, 2, 3, 4, 5

seq -s " " 1 10
# → 1 2 3 4 5 6 7 8 9 10

seq -s "-" 5
# → 1-2-3-4-5
```

## 3. Égaliser la largeur (-w)

```bash
# Sans -w : tailles différentes
seq 8 11
# → 8
# → 9
# → 10
# → 11

# Avec -w : tous même largeur (pratique pour noms de fichiers)
seq -w 8 11
# → 08
# → 09
# → 10
# → 11
```

## 4. Cas pratiques

```bash
# Créer 100 dossiers numérotés
seq -w 1 100 | xargs -I {} mkdir dossier_{}

# Générer une liste d'hôtes
seq -f "serveur-%g" 1 5
# → serveur-1
# → serveur-2
# ...

# Format printf personnalisé
seq -f "host-%02g.local" 1 5
# → host-01.local
# → host-02.local
# ...

# Dans une boucle for
for i in $(seq 1 10); do
  echo "Itération $i"
done

# Tester rapidement avec des fichiers de taille croissante
for i in $(seq 1 100 1000); do
  head -c ${i}K /dev/urandom > fichier_${i}K.bin
done
```

## 5. Séquences descendantes

```bash
# Compte à rebours
seq 10 -1 1
# → 10 9 8 7 6 5 4 3 2 1

# Pas négatif
seq 100 -10 0
# → 100 90 80 ... 10 0

# Version Bash native (plus rapide) :
echo {10..1}
echo {100..0..10}
```

## 6. Exercices pratiques

1. **Base** — Génère les nombres de 1 à 20
2. **Pas** — Génère tous les nombres pairs de 0 à 20 (pas de 2)
3. **Séparateur** — Affiche les nombres de 1 à 10 sur une seule ligne séparés par des virgules
4. **Dossiers** — Crée 20 dossiers nommés `test_01` à `test_20`
