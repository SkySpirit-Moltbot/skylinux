# Leçon 64 : bc — La calculatrice en ligne de commande

`bc` est une calculatrice puissante qui gère les grands nombres, les décimales, et les expressions mathématiques complexes.

## 1. Calculs simples

```bash
# Mode interactif
bc
# 2+2
# 4
# 10*5
# 50
# Ctrl+D pour quitter

# En ligne de commande
echo "2+2" | bc
# → 4

echo "10*5" | bc
# → 50
```

## 2. Gérer les décimales

```bash
# Par défaut, bc fait des divisions entières !
echo "5/2" | bc
# → 2  (entier !)

# scale = nombre de décimales
echo "scale=2; 5/2" | bc
# → 2.50

echo "scale=4; 10/3" | bc
# → 3.3333
```

## 3. Calculs avancés (avec -l)

```bash
# -l charge la bibliothèque mathématique standard
echo "scale=2; s(1)" | bc -l
# → .84  (sinus de 1 radian)

echo "scale=2; c(0)" | bc -l
# → 1.00  (cosinus de 0)

echo "e(1)" | bc -l
# → 2.718281...  (e^1)

echo "scale=2; l(2.718281)" | bc -l
# → 1.00  (logarithme naturel)

# Racine carrée
echo "scale=4; sqrt(2)" | bc -l
# → 1.4142
```

## 4. Conversions pratiques

```bash
# Décimal → Binaire
echo "obase=2; 42" | bc
# → 101010

# Décimal → Hexadécimal
echo "obase=16; 255" | bc
# → FF

# Hexadécimal → Décimal
echo "ibase=16; FF" | bc
# → 255

# Octets vers Mégaoctets
echo "scale=2; 12345678 / 1048576" | bc
# → 11.77  (Mo)
```

## 5. Dans un script bash

```bash
#!/bin/bash
taille_octets=12345678
taille_mo=$(echo "scale=2; $taille_octets / 1048576" | bc)
echo "Taille: ${taille_mo} Mo"

# Calculer un pourcentage
utilise=32000000
total=50000000
pourcent=$(echo "scale=1; $utilise * 100 / $total" | bc)
echo "Utilisé: ${pourcent}%"
```

## 6. Exercices pratiques

1. **Base** — Calcule 1234 * 5678 avec bc
2. **Décimales** — Calcule 22/7 avec 6 décimales
3. **Conversion** — Convertis 255 en binaire et en hexadécimal
4. **Sinus** — Calcule le sinus de 0.5 radian avec 4 décimales
