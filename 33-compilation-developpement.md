# Leçon 33 : Compilation et Développement (gcc / make)

Dans cette leçon, tu vas apprendre à compiler du code source en programmes exécutables avec `gcc`, et à automatiser le processus de construction avec `make`. Ces outils sont fondamentaux pour tout développeur ou administrateur Linux qui travaille avec du code source.

---

## 1. Préparer l'environnement de développement

Avant de compiler, installe les outils nécessaires :

```bash
# Sur Debian/Ubuntu
sudo apt update
sudo apt install build-essential

# Le package build-essential inclut :
# - gcc (compilateur C)
# - g++ (compilateur C++)
# - make (outil de construction)
# - libc6-dev (bibliothèque C standard)

# Vérifier les installations
gcc --version
g++ --version
make --version
```

---

## 2. Les bases de gcc

`gcc` (GNU Compiler Collection) est le compilateur principal sur Linux. Il transforme ton code source en exécutable.

### Compilation simple

```bash
# Créer un fichier source C
cat > salut.c << 'EOF'
#include <stdio.h>

int main() {
    printf("Bonjour le monde !\n");
    return 0;
}
EOF

# Compiler le programme
gcc salut.c -o salut

# Exécuter le résultat
./salut
```

### Les étapes de compilation

gcc compile en plusieurs étapes :

| Étape | Description | Fichier produit |
|---|---|---|
| **Préprocessing** | Traitement des `#include` et `#define` | `.i` |
| **Compilation** | Traduction en assembleur | `.s` |
| **Assemblage** | Conversion en code machine | `.o` |
| **Linking** | Assemblage des fichiers objets | exécutable |

```bash
# Voir chaque étape单独
gcc -E salut.c -o salut.i    # Préprocessing seulement
gcc -S salut.c -o salut.s   # Générer l'assembleur
gcc -c salut.c -o salut.o   # Compiler sans linker (fichier objet)
gcc salut.o -o salut         # Linker pour créer l'exécutable
```

### Options utiles de gcc

```bash
# Mode verbose (afficher les étapes)
gcc -v salut.c -o salut

# Activer tous les warnings
gcc -Wall -Wextra salut.c -o salut

# Débogage (ajouter les symboles de debug)
gcc -g salut.c -o salut

# Optimisation
gcc -O2 salut.c -o salut    # Niveau 2 d'optimisation

# Spécifier le standard C
gcc -std=c11 salut.c -o salut
gcc -std=c99 salut.c -o salut

# Compiler pour une architecture différente
gcc -march=native salut.c -o salut  # Optimisé pour ta machine
```

### Exemple complet avec messages d'erreur

```bash
# Programme avec une erreur volontaire
cat > test_erreur.c << 'EOF'
#include <stdio.h>

int main() {
    int x = 10;
    printf("La valeur est %d\n", x);
    return 0;
}
EOF

# Compiler avec warnings
gcc -Wall -Wextra test_erreur.c -o test_erreur

# Exécuter
./test_erreur
```

---

## 3. Compiler du C++ avec g++

`g++` est le compilateur C++ (en fait, c'est un wrapper autour de gcc).

```bash
# Programme C++
cat > salut.cpp << 'EOF'
#include <iostream>

int main() {
    std::cout << "Bonjour depuis C++ !" << std::endl;
    return 0;
}
EOF

# Compiler avec g++
g++ salut.cpp -o salut

# Exécuter
./salut

# Avec C++11 et plus récent
g++ -std=c++17 salut.cpp -o salut
```

### Compiler plusieurs fichiers

```bash
# fichier1.c
int addition(int a, int b) {
    return a + b;
}

// fichier2.c
#include <stdio.h>

extern int addition(int a, int b);

int main() {
    int resultat = addition(5, 3);
    printf("5 + 3 = %d\n", resultat);
    return 0;
}

# Compiler chaque fichier séparément
gcc -c fichier1.c -o fichier1.o
gcc -c fichier2.c -o fichier2.o

# Linker ensemble
gcc fichier1.o fichier2.o -o programme

./programme
# Résultat : 5 + 3 = 8
```

---

## 4. Introduction à make et les Makefiles

`make` automatise la compilation. Au lieu de retaper toutes les commandes, tu décris ton projet dans un **Makefile**.

### Un Makefile simple

```bash
cat > Makefile << 'EOF'
CC = gcc
CFLAGS = -Wall -g
TARGET = salut

all: $(TARGET)

$(TARGET): salut.c
	$(CC) $(CFLAGS) salut.c -o $(TARGET)

clean:
	rm -f $(TARGET) *.o

run: $(TARGET)
	./$(TARGET)
EOF
```

### Utiliser le Makefile

```bash
# Compiler le projet
make

# Exécuter
make run

# Nettoyer les fichiers générés
make clean

# Forcer la recompilation
make clean && make
```

### Syntaxe d'un Makefile

```makefile
# Variables
CC = gcc           # Compilateur
CFLAGS = -Wall     # Options
TARGET = monprog   # Nom de l'exécutable

# Règle par défaut (ce qui est exécuté avec 'make')
all: $(TARGET)

# Règle : dépendance -> actions (TAB obligatoire !)
$(TARGET): main.o fonc.o
	$(CC) $(CFLAGS) main.o fonc.o -o $(TARGET)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

fonc.o: fonc.c
	$(CC) $(CFLAGS) -c fonc.c

clean:
	rm -f $(TARGET) *.o

.PHONY: all clean  # Indique que ces cibles ne sont pas des fichiers
```

**Important** : Les lignes d'actions doivent commencer par une **TABULATION** (tab), pas des espaces !

### Variables automatiques de make

```makefile
# $< = fichier source dépendant
# $@ = cible
# $^ = toutes les dépendances

$(TARGET): $(OBJ)
	$(CC) $^ -o $@    # Équivalent à : gcc main.o fonc.o -o monprog

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
# Équivalent à : gcc -Wall -g -c main.c -o main.o
```

---

## 5. Un vrai projet multi-fichiers

### Structure du projet

```
monprojet/
├── include/
│   └── calcul.h
├── src/
│   ├── main.c
│   └── calcul.c
└── Makefile
```

### Les fichiers source

```bash
mkdir -p monprojet/include monprojet/src
cd monprojet

# Header
cat > include/calcul.h << 'EOF'
#ifndef CALCUL_H
#define CALCUL_H

int addition(int a, int b);
int soustraction(int a, int b);

#endif
EOF

# Implémentation
cat > src/calcul.c << 'EOF'
#include "calcul.h"

int addition(int a, int b) {
    return a + b;
}

int soustraction(int a, int b) {
    return a - b;
}
EOF

# Programme principal
cat > src/main.c << 'EOF'
#include <stdio.h>
#include "calcul.h"

int main() {
    int x = 10, y = 3;
    printf("%d + %d = %d\n", x, y, addition(x, y));
    printf("%d - %d = %d\n", x, y, soustraction(x, y));
    return 0;
}
EOF
```

### Le Makefile complet

```makefile
CC = gcc
CFLAGS = -Wall -g -Iinclude
TARGET = calculatrice
SRC = src
OBJ = $(SRC)/main.o $(SRC)/calcul.o

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET)

$(SRC)/main.o: $(SRC)/main.c include/calcul.h
	$(CC) $(CFLAGS) -c $(SRC)/main.c -o $(SRC)/main.o

$(SRC)/calcul.o: $(SRC)/calcul.c include/calcul.h
	$(CC) $(CFLAGS) -c $(SRC)/calcul.c -o $(SRC)/calcul.o

clean:
	rm -f $(TARGET) $(SRC)/*.o

.PHONY: all clean
```

### Compiler et tester

```bash
make
# Résultat : cc -Wall -g -Iinclude -c src/main.c -o src/main.o
#            cc -Wall -g -Iinclude -c src/calcul.c -o src/calcul.o
#            cc src/main.o src/calcul.o -o calculatrice

./calculatrice
# Résultat : 10 + 3 = 13
#            10 - 3 = 7
```

---

## 6. Compiler avec des bibliothèques

### Bibliothèque standard

```bash
# Bibliothèque math (à linker avec -lm)
cat > math_demo.c << 'EOF'
#include <stdio.h>
#include <math.h>

int main() {
    double x = 16.0;
    printf("sqrt(%.1f) = %.2f\n", x, sqrt(x));
    printf("pow(2, 8) = %.1f\n", pow(2, 8));
    return 0;
}
EOF

gcc math_demo.c -o math_demo -lm
./math_demo
```

### Bibliothèque externe

```bash
# Exemple avec curl (libcurl)
# sudo apt install libcurl4-openssl-dev

cat > web_test.c << 'EOF'
#include <stdio.h>
#include <curl/curl.h>

int main() {
    CURL *curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://example.com");
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return 0;
}
EOF

gcc web_test.c -o web_test -lcurl
```

---

## 7. make -n (dry run) et debugging

```bash
# Voir ce que make ferait SANS exécuter
make -n

# Makefile avec debugging
# Ajouter des echoes pour voir les valeurs
$(TARGET): $(OBJ)
	@echo "Compilation de $(TARGET)..."
	$(CC) $(OBJ) -o $(TARGET)
	@echo "Terminé !"

# Vérifier la syntaxe makefile
make -n

# make avec debug
make DEBUG=1
```

---

## 8. Scripts de build plus avancés

### Makefile avec options conditionnelles

```makefile
# Mode release (optimisé) ou debug
MODE = debug

ifeq ($(MODE),debug)
    CFLAGS = -Wall -g -O0
    TARGET = $(PROGRAM)_debug
else
    CFLAGS = -Wall -O2
    TARGET = $(PROGRAM)
endif

# Changer de mode :
# make MODE=release
# make MODE=debug
```

### Ajouter un target "install"

```makefile
PREFIX = /usr/local

install: $(TARGET)
	install -d $(PREFIX)/bin
	install -m 755 $(TARGET) $(PREFIX)/bin

uninstall:
	rm -f $(PREFIX)/bin/$(TARGET)
```

---

## 9. Exercices pratiques

### Exercice 1 : Premier programme compilé

```bash
# 1. Créer un fichier salut.c
cat > salut.c << 'EOF'
#include <stdio.h>

int main() {
    printf("Hello, Linux !\n");
    return 0;
}
EOF

# 2. Compiler avec gcc
gcc salut.c -o salut

# 3. Exécuter
./salut

# 4. Voir le fichier généré
ls -la salut
file salut
```

### Exercice 2 : Programme avec fonctions

```bash
# 1. Créer un programme qui calcule la factorielle
cat > factorielle.c << 'EOF'
#include <stdio.h>

long factorielle(int n) {
    if (n <= 1) return 1;
    return n * factorielle(n - 1);
}

int main() {
    int n = 5;
    printf("%d! = %ld\n", n, factorielle(n));
    return 0;
}
EOF

# 2. Compiler avec warnings
gcc -Wall -Wextra factorielle.c -o factorielle

# 3. Exécuter
./factorielle
```

### Exercice 3 : Projet multi-fichiers avec Makefile

```bash
# 1. Créer la structure
mkdir -p triangle/src triangle/include

# 2. Les fichiers
cat > triangle/include/aire.h << 'EOF'
#ifndef AIRE_H
#define AIRE_H
double aire_cercle(double rayon);
double aire_rectangle(double largeur, double hauteur);
#endif
EOF

cat > triangle/src/aire.c << 'EOF'
#include "aire.h"
#define PI 3.14159

double aire_cercle(double rayon) {
    return PI * rayon * rayon;
}

double aire_rectangle(double largeur, double hauteur) {
    return largeur * hauteur;
}
EOF

cat > triangle/src/main.c << 'EOF'
#include <stdio.h>
#include "aire.h"

int main() {
    printf("Aire cercle (r=3): %.2f\n", aire_cercle(3.0));
    printf("Aire rectangle (5x4): %.2f\n", aire_rectangle(5.0, 4.0));
    return 0;
}
EOF

# 3. Le Makefile
cat > triangle/Makefile << 'EOF'
CC = gcc
CFLAGS = -Wall -g -Isrc/include -Isrc
SRC = src
TARGET = aire_calc

all: $(TARGET)

$(TARGET): $(SRC)/main.o $(SRC)/aire.o
	$(CC) $(SRC)/main.o $(SRC)/aire.o -o $(TARGET)

$(SRC)/main.o: $(SRC)/main.c $(SRC)/include/aire.h
	$(CC) $(CFLAGS) -c $(SRC)/main.c -o $(SRC)/main.o

$(SRC)/aire.o: $(SRC)/aire.c $(SRC)/include/aire.h
	$(CC) $(CFLAGS) -c $(SRC)/aire.c -o $(SRC)/aire.o

clean:
	rm -f $(TARGET) $(SRC)/*.o

.PHONY: all clean
EOF

# 4. Compiler et tester
cd triangle
make
./aire_calc
cd ..
```

### Exercice 4 : Automatiser la compilation avec un script

```bash
# Créer un script build.sh
cat > build.sh << 'EOF'
#!/bin/bash

set -e  # Arrêter en cas d'erreur

echo "=== Compilation du projet ==="

# Nettoyer
make clean 2>/dev/null || true

# Compiler
make

# Exécuter si la compilation a réussi
if [ -f "./monprog" ]; then
    echo ""
    echo "=== Exécution ==="
    ./monprog
else
    echo "Erreur : la compilation a échoué"
    exit 1
fi
EOF

chmod +x build.sh
./build.sh
```

---

## 10. Résumé des commandes

| Commande | Description |
|---|---|
| `gcc -o prog source.c` | Compiler un fichier C |
| `g++ -o prog source.cpp` | Compiler un fichier C++ |
| `gcc -c source.c` | Compiler sans linker (fichier .o) |
| `gcc -Wall source.c` | Activer tous les warnings |
| `gcc -g source.c` | Ajouter les symboles de debug |
| `gcc -O2 source.c` | Compiler avec optimisation niveau 2 |
| `gcc -lm source.c` | Linker avec la bibliothèque math |
| `make` | Exécuter le Makefile |
| `make clean` | Nettoyer les fichiers générés |
| `make -n` | Simuler sans exécuter |
| `make -C dir` | Exécuter make dans un autre répertoire |

---

## 11. Aller plus loin

- **CMake** : Système de build plus moderne et portable (utilisé par de gros projets)
- **Autotools (configure/make)** : Le système classique de build Unix
- **IDE** : VSCode, CLion, ou Qt Creator pour développer visuellement
- **Valgrind** : Détecter les fuites mémoire (`valgrind ./programme`)
- **gdb** : Débogueur GNU (`gdb ./programme`)
- **strace** : Voir les appels système d'un programme (`strace ./programme`)
