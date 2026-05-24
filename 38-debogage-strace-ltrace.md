# Leçon 38 : strace et ltrace — Déboguer ce que fait vraiment un programme

Un programme plante sans raison ? `strace` et `ltrace` te montrent tout ce qu'il fait en coulisses : fichiers ouverts, appels réseau, mémoire allouée.

## 1. strace — Les appels au noyau

`strace` intercepte les appels système : chaque fois qu'un programme ouvre un fichier, lit le réseau ou alloue de la mémoire.

```bash
# Installer
sudo apt install strace

# Tracer une commande simple
strace ls -l /tmp
```

Tu verras une sortie comme :

```
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY) = 3
fstat(3, {st_mode=S_IFREG|0644, ...})   = 0
mmap(NULL, 12345, PROT_READ, ...)       = 0x7f...
```

- **Valeur positive** = succès (ex: `= 3` → descripteur de fichier 3)
- **Valeur = -1** = échec, suivi du code erreur (ex: `ENOENT` = fichier non trouvé)

## 2. Options essentielles de strace

```bash
# Filtrer un type d'appel spécifique
strace -e openat ls /tmp

# Plusieurs appels à la fois
strace -e trace=open,read,write cat /etc/hostname

# Résumé statistique (ultra utile !)
strace -c ls /tmp
# Affiche : temps passé, nombre d'appels, erreurs pour chaque syscall

# Sauvegarder dans un fichier
strace -o /tmp/trace.log ./mon_programme

# Attacher à un processus EXISTANT
sudo strace -p 1234

# Suivre les processus enfants (fork)
sudo strace -fp 1234

# Timestamps
strace -t ls /tmp        # heure HH:MM:SS
strace -tt ls /tmp       # avec microsecondes
strace -r ls /tmp        # durée relative de chaque appel
```

## 3. ltrace — Les appels aux bibliothèques

`ltrace` montre les appels aux fonctions des bibliothèques partagées (.so), comme malloc, strlen, printf.

```bash
sudo apt install ltrace

# Tracer les appels aux bibliothèques
ltrace ls /tmp
```

Exemple de sortie :

```
malloc(32)                        = 0x55a...
strcmp("HOME", "HOME")            = 0
getenv("HOME")                    = "/home/david"
```

```bash
# Résumé statistique
ltrace -c ls /tmp

# Filtrer une fonction précise
ltrace -e malloc,free ./mon_programme

# Attacher à un processus existant
sudo ltrace -p 1234
```

## 4. Cas pratiques de débogage

### Cas 1 : "Fichier non trouvé"

```bash
strace -e openat ./mon_programme 2>&1 | grep ENOENT
# → montre exactement quel fichier est cherché et manquant
```

### Cas 2 : Le programme plante au démarrage

```bash
strace -e trace=open,execve ./programme 2>&1 | grep -E "ENOENT|EACCES"
```

### Cas 3 : Lent au démarrage

```bash
# Voir combien de fichiers sont ouverts
strace -c -e trace=open,read,write,execve ./programme_lent

# Lister les fichiers ouverts
strace -e openat ./programme_lent 2>&1 | head -30
```

### Cas 4 : Comprendre les connexions réseau

```bash
strace -e trace=connect,socket,bind ./mon_service
# ou plus simple :
strace -e trace=network ./script_reseau
```

### Cas 5 : Déboguer un script shell

```bash
strace -f -o /tmp/script_trace.log ./script.sh
grep -E "ENOENT|EACCES" /tmp/script_trace.log
```

## 5. strace vs ltrace

| Outil | Trace | Usage typique |
|-------|-------|---------------|
| `strace` | Appels système (noyau) | Fichiers, réseau, processus |
| `ltrace` | Appels bibliothèques (libc) | malloc, printf, strlen |
| `strace -c` | Statistiques | Trouver les lenteurs |
| `strace -p` | Processus en cours | Déboguer sans redémarrer |

## 6. Exercices pratiques

1. **Première trace** — Lance `strace ls /tmp` et observe les appels système
2. **Résumé** — Lance `strace -c ls /tmp` et identifie l'appel le plus fréquent
3. **Fichier manquant** — Lance `strace -e openat cat /fichier_inexistant 2>&1 | grep ENOENT`
4. **ltrace** — Compare la sortie de `strace ls` et `ltrace ls`
