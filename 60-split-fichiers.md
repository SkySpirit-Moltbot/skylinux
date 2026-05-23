# Leçon 60 : split et cat — Diviser et assembler des fichiers

### 1. split — Diviser un fichier

La syntaxe de base de split est simple :

Par défaut, split crée des fichiers de 1000 lignes chacun. Le préfixe par défaut est x, donc les fichiers générés s'appellent xaa, xab, xac, etc.

### 3. Exemples pratiques

Pour diviser un fichier de log en morceaux de 500 lignes :

Cela crée des fichiers partie_aa, partie_ab, etc.

Pour créer des fichiers de 10 Mo chacun :

Ou des fichiers de 1,5 Mo (utile pour les disquettes/CDs) :

Pour avoir des suffixes plus lisibles :

Résultat : data_00, data_01, data_02, etc.

Pour diviser en exactement 4 parties :

### 4. cat — Réassembler les fichiers

Pour reconstruire le fichier original, utilisez cat avec une redirection :

Ou avec des suffixes numériques :

Attention : l'ordre de concatenation depend de l'ordre alphabétique. Si vos suffixes sont data_00, data_01, etc., le tri alphabétique fonctionne parfaitement.

### 5. Cas d'usage courants

Diviser une archive pour l'envoyer en pieces :

### 6. Vérifier l'intégrité après reassemblage

Pour vous assurer que le fichier reassemblé est identique à l'original :

Les deux hashes doivent être identiques.

### 7. Astuces utiles

Si vous recevez des données via un tube :

### Exercice pratique

Créez un fichier texte contenant plusieurs lignes (utilisez seq 1 5000 > test.txt)

Divisez-le en fichiers de 1000 lignes : split -l 1000 test.txt bloc_

Listez les fichiers créés : ls -lh bloc_*

Réassemblez-les : cat bloc_* > test_reconstruit.txt

Vérifiez l'intégrité : diff test.txt test_reconstruit.txt (ne doit rien afficher)

Supprimez les fichiers temporaires : rm bloc_* test.txt test_reconstruit.txt

