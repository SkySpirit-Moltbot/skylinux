# Leçon 38 : Débogage avec Strace et Ltrace
Un programme ne fonctionne pas ? Il plante sans raison apparente ? **strace** et **ltrace** sont tes meilleurs alliés pour comprendre ce qu'un programme fait vraiment — en regardant les appels système et les appels aux bibliothèques partagées.
## 1. Qu'est-ce que strace ?
**strace** intercepte et enregistre les **appels système** (syscalls) qu'un programme effectue vers le noyau Linux. Chaque fois qu'un programme ouvre un fichier, lit du réseau, alloue de la mémoire ou crée un processus, c'est un appel système.
En gros : strace te montre la conversation entre le programme et le noyau.
sudo apt install strace
# Vérifier qu'il fonctionne
strace -V
## 2. Utiliser strace sur un programme
### Tracer un programme existant
strace ls -l /tmp
# Lancer et tracer un script
strace ./mon_script.sh
Tu verras une longue liste d'appels comme :
brk(NULL)                               = 0x55a3c000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT
open("/etc/ld.so.cache", O_RDONLY)      = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=...) = 0
mmap(NULL, ..., PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f...
open("/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY) = 3
### Lire les colonnes d'un appel système
Chaque ligne strace suit ce format :
^nom de l'appel  ^ses arguments           ^valeur de retour (fd=3)
- **Valeur de retour positive** : l'appel a réussi (ex : descripteur de fichier 3)
- **Valeur = -1** : l'appel a échoué, suivi du code d'erreur (ex : `ENOENT` = fichier non trouvé, `EACCES` = permission refusée)
## 3. Options utiles de strace
### Suivre les appels à un nom précis
strace -e openat ls /tmp
# Plusieurs appels système à surveiller
strace -e trace=open,read,write cat /etc/hostname
### Comptage des appels (sans détail)
strace -c ls /tmp
# Résultat :
# % time     seconds  usecs/call     calls    errors syscall
# ------ ----------- ----------- --------- --------- -------
#  35.00    0.000210          12        17           mmap
#  20.00    0.000120           8        15           openat
#  15.00    0.000090           6        15           fstat
#   ...
# 100.00    0.000600          11        52           total
### Filtrer par résultat (erreurs)
strace -e trace=open -P /root ls /tmp
# Ou capturer dans un fichier (sans polluer le terminal)
strace -o /tmp/trace.txt ls /tmp
# Lire le fichier de trace
less /tmp/trace.txt
### Attacher strace à un processus existant (PID)
ps aux | grep firefox
# Attacher strace à un processus en cours
sudo strace -p 1234
# Suivre aussi les processus enfants (fork)
sudo strace -fp 1234
### Timestamps pour voir la chronologie
strace -t ls /tmp
# Temps absolu
strace -tt ls /tmp
# Durée de chaque appel
strace -r ls /tmp
## 4. Qu'est-ce que ltrace ?
**ltrace** intercepte les **appels aux bibliothèques partagées** (librairies .so). Là où strace montre les appels au noyau, ltrace montre les appels aux fonctions des bibliothèques (libc, pthread, etc.).
sudo apt install ltrace
# Lancer et tracer les appels bibliothèques
ltrace ls /tmp
Exemple de sortie :
malloc(32)                                                    = 0x55a...
strcmp("HOME", "HOME")                                        = 0
getenv("HOME")                                                = "/home/david"
strlen("/home/david")                                         = 10
strcpy(0x55..., "/home/david")                                = 0x55...
### Options utiles de ltrace
ltrace -c ls /tmp
# Suivre un nom de fonction précis
ltrace -e malloc,free ls /tmp
# Attacher à un processus existant
sudo ltrace -p 1234
# Afficher les paramètres des fonctions
ltrace -i ls /tmp
## 5. Cas pratiques de débogage
### Cas 1 : Un programme dit "Fichier non trouvé"
strace -e openat ./mon_programme 2>&1 | grep ENOENT
# Ou chercher "No such file"
strace -e openat ./mon_programme 2>&1 | grep -i "no such"
Tu verras exactement quel fichier le programme essaie d'ouvrir.
### Cas 2 : Un programme plante au démarrage
strace -e trace=open,execve ./programme_fantome 2>&1 | grep -E "ENOENT|EACCES|ERR"
# Déboguer avec les signaux ( voir comment le programme se termine)
strace -e signal=none -e trace=none -f ./programme_fantome
### Cas 3 : Un programme est lent au démarrage
strace -c -e trace=open,read,write,execve ./programme_lent
# Vérifier si des fichiers sont ouverts inutilement
strace -e openat ./programme_lent 2>&1 | head -30
### Cas 4 : Comprendre ce qu'un programme réseau fait
strace -e trace=connect,socket,bind ./mon_service
# Tracer aussi send/recv
strace -e trace=network ./script_reseau
### Cas 5 : Déboguer un script shell qui échoue
strace -f -o /tmp/script_trace.log ./script.sh
# Lire le fichier de trace
grep -E "ENOENT|EACCES" /tmp/script_trace.log
## 6. strace vs ltrace — Quand utiliser quoi ?
| Outil | Ce qu'il trace | Cas d'usage |
| --- | --- | --- |
| `ltrace` | Appels aux bibliothèques partagées | Fonctions malloc/free, printf, libc |
| `strace -c` | Résumé statistique | Trouver les goulots d'étranglement |
| `strace -p` | Processus existant (PID) | Déboguer un programme déjà lancé |
## 7. Combiner strace et ltrace
(strace -f -e trace=execve ./programme 2>&1) | grep ENOENT
(ltrace -f ./programme 2>&1) | grep NULL
# Enregistrer les deux dans des fichiers séparés
strace -o /tmp/strace.log ./programme &
ltrace -o /tmp/ltrace.log ./programme
> **Warning** : ⚠️ **Performance** : strace ralentit considérablement le programme tracé (surtout avec `-f`). Utilise-le sur des programmes qui ne sont pas en production critique, ou en lecture seule.
## Exercice pratique
**Objectif :** Utilise strace et ltrace pour comprendre le comportement d'un programme simple.
- Installe les outils : `sudo apt install strace ltrace`
- `strace -e openat ls /var/log 2>&1 | head -20`
- Observe les fichiers ouverts par `ls`
- Utilise le mode résumé : `strace -c ls /tmp`
- Trace avec ltrace : `ltrace -c ls /tmp 2>&amp;1 | head -20`
cat /etc/hostname
mkdir /tmp/test_debug
echo "OK" &gt; /tmp/test_debug/fichier.txt
- Trace-le avec strace : `strace -f -o /tmp/script_trace.log ./test.sh`
- Cherche les erreurs : `grep -E "ENOENT|EACCES" /tmp/script_trace.log`
- Utilise `ltrace` sur le script : `ltrace -f ./test.sh 2>&amp;1 | grep getenv`
## Résumé
| Commande | Rôle |
| --- | --- |
| `strace -e openat &lt;commande&gt;` | Ne tracer qu'un appel précis |
| `strace -c &lt;commande&gt;` | Résumé statistique des appels |
| `strace -p &lt;PID&gt;` | Attacher à un processus existant |
| `strace -o fichier.log &lt;commande&gt;` | Sauvegarder la trace dans un fichier |
| `ltrace &lt;commande&gt;` | Tracer les appels aux bibliothèques |
| `ltrace -c &lt;commande&gt;` | Résumé statistique des appels bibliothèques |
| `strace -f &lt;commande&gt;` | Suivre aussi les processus enfants (fork) |
strace et ltrace sont des outils puissants pour comprendre ce qui se passe vraiment dans un programme. En cas de doute, trace tout et cherche les erreurs — elles ne mentent jamais.