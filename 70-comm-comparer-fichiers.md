# Leçon 70 : comm — Comparer deux fichiers ligne par ligne

### Introduction

La commande comm permet de comparer deux fichiers texte ligne par ligne et d'afficher les différences de manière structurée. Contrairement à diff qui montre les modifications, comm sépare clairement les lignes uniques à chaque fichier et celles communes aux deux.

### Sortie en trois colonnes

Par défaut, comm affiche trois colonnes :

Colonne 1 : Lignes présentes uniquement dans le premier fichier

Colonne 2 : Lignes présentes uniquement dans le second fichier

Colonne 3 : Lignes communes aux deux fichiers

### Exemple simple

Créons deux fichiers pour tester :

Comparons les deux fichiers :

Résultat :

### Options principales

Affiche uniquement les colonnes 2 et 3 (lignes uniques à B + lignes communes).

Affiche uniquement les colonnes 1 et 3 (lignes uniques à A + lignes communes).

Affiche uniquement les colonnes 1 et 2 (lignes uniques à A ou B, sans les communes).

N'affiche que les lignes qui n'existent que dans un seul des deux fichiers (sans les communes).

### Comparaison avec fichiers triés

comm exige que les fichiers soient triés pour fonctionner correctement. Si vos fichiers ne sont pas triés, vous devez les trier d'abord :

### Conclusion

comm est un outil puissant pour comparer des fichiers texte triés. Sa sortie en trois colonnes permet de visualiser clairement les différences et les similitudes entre deux fichiers. Combiné avec le tri et d'autres commandes Unix, il devient un outil indispensable pour la gestion et la comparaison de données.

