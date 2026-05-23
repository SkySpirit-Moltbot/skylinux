# Leçon 64 : bc — La calculatrice en ligne de commande

### Introduction

Sous Linux, bc est la calculatrice arbitrary-precision (précision arbitraire) du terminal. Contrairement à expr qui ne gère que des nombres entiers, bc supporte les nombres décimaux, les fonctions mathématiques avancées (trigonométrie, racines carrées, logarithmes), et peut même lire des calculs depuis un fichier ou un pipe.

Son nom vient de "Basic Calculator". C'est l'outil idéal pour des calculs rapides sans quitter le terminal.

### Installation

bc est généralement préinstallé sur les distributions Linux. Si ce n'est pas le cas :

### Utilisation basique

Dans le mode interactif, tapez vos calculs et appuyez sur Entrée. Tapez quit pour quitter.

La variable scale définit le nombre de décimales affichées (par défaut : 0).

### La variable scale

Par défaut, bc affiche uniquement des nombres entiers. Pour obtenir des décimales, utilisez scale :

Sans scale, la division donne un résultat entier arrondi.

### Fonctions mathématiques

bc intègre une bibliothèque mathématique complète. Activez-la avec -l :

Fonctions disponibles avec -l :

### Utilisation avancée

L'option -q supprime le message de bienvenue.

bc supporte les opérateurs de comparaison (>, , >=, , ==, !=) et les instructions if/else, while, for.

### Conversion de bases

bc peut convertir entre différentes bases grâce à ibase et obase :

### Exercices pratiques

Calculez 256 * 1024 sans calculatrice ni Python.

Trouvez la racine carrée de 2 avec 10 décimales.

Convertissez le nombre 255 en binaire et en hexadécimal.

Créez un script qui convertit des degrés Celsius en Fahrenheit.

Calculez la factorielle de 20 avec une boucle dans bc.

### Corrections

echo "256 * 1024" | bc → 262144

echo "scale=10; sqrt(2)" | bc → 1.4142135623

Binaire : echo "obase=2; 255" | bc → 11111111Hexadécimal : echo "obase=16; 255" | bc → FF

Script : echo "scale=2; celsius * 9 / 5 + 32" | bc où celsius est une variable

echo "f=1; for(i=1;i → 2432902008176640000

