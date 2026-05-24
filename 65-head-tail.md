# Leçon 65 : head et tail — Visualiser le début et la fin des fichiers

Deux commandes jumelles : `head` montre les premières lignes, `tail` les dernières. Indispensables pour explorer des fichiers rapidement.

## 1. head — Le début du fichier

```bash
# 10 premières lignes (défaut)
head mon_fichier.txt

# N premières lignes
head -n 5 mon_fichier.txt

# Premiers octets
head -c 100 mon_fichier.txt

# Tous SAUF les N dernières lignes
head -n -5 mon_fichier.txt
# → tout le fichier sauf les 5 dernières lignes
```

## 2. tail — La fin du fichier

```bash
# 10 dernières lignes (défaut)
tail mon_fichier.txt

# N dernières lignes
tail -n 20 mon_fichier.txt

# Derniers octets
tail -c 500 mon_fichier.txt

# Suivre un fichier en temps réel !
tail -f /var/log/syslog
# Ctrl+C pour arrêter

# Suivre avec conservation si le fichier est recréé
tail -F /var/log/nginx/access.log
```

## 3. tail -f : le plus utile

```bash
# Voir les logs en direct (le cas d'usage numéro 1)
tail -f /var/log/syslog

# Suivre plusieurs fichiers à la fois
tail -f /var/log/syslog /var/log/auth.log

# Filtrer ce qui défile
tail -f /var/log/syslog | grep --line-buffered erreur

# Voir ses propres actions en direct
tail -f ~/.bash_history
```

## 4. Combinaisons head + tail

```bash
# Lignes 15 à 25 d'un fichier
head -n 25 fichier.txt | tail -n 11

# Lignes 100 à 110
cat -n fichier.txt | tail -n +100 | head -n 11

# La 3e ligne d'un fichier
head -n 3 fichier.txt | tail -n 1
```

## 5. Cas pratiques

```bash
# Vérifier le début d'un CSV (entête + premières données)
head -n 5 data.csv

# Voir les dernières connexions SSH
tail -n 20 /var/log/auth.log | grep sshd

# Extraire une plage : enlever l'entête d'un CSV
tail -n +2 data.csv > data_sans_entete.csv

# Afficher les 5 plus récentes entrées
tail -n 5 /var/log/syslog
```

## 6. Exercices pratiques

1. **Head** — Affiche les 3 premières lignes de `/etc/passwd`
2. **Tail** — Affiche les 10 dernières lignes de `/var/log/syslog`
3. **Live** — Lance `tail -f` sur un fichier de log et écris dedans depuis un autre terminal
4. **Plage** — Affiche les lignes 5 à 10 d'un fichier avec head et tail combinés
