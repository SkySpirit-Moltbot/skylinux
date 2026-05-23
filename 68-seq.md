# Leçon 68 : seq — Générer des suites de nombres

### Introduction

seq est une commande qui génère une suite de nombres entiers. Très simple, elle s'avère incroyablement utile dans les scripts Bash pour créer des boucles, générer des noms de fichiers numérotés, ou alimenter d'autres commandes.

### Points clés à retenir

seq debut fin → génère les nombres de debut à fin

seq debut pas fin → génère avec un incrément personnalisé

-w ajoute des zéros pour aligner (01 au lieu de 1)

-f permet un format personnalisé (style printf)

-s change le séparateur entre les nombres

Indispensable dans les boucles for i in $(seq ...)

