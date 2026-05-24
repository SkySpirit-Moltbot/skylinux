# Leçon 50 : rsync — Synchroniser des fichiers comme un pro

Dans cette leçon, tu vas apprendre à utiliser `rsync`, l'outil indispensable pour copier et synchroniser des fichiers rapidement, que ce soit en local ou entre deux machines.

## 1. C'est quoi rsync ?

`rsync` est un outil de copie **intelligent**. Contrairement à `cp`, il ne copie que ce qui a changé. Résultat : la deuxième synchronisation est ultra-rapide.

**Cas concret :** tu as un dossier de 10 Go. Tu modifies un seul fichier de 2 Ko. Avec `cp`, tu recopies tout (10 Go). Avec `rsync`, seuls les 2 Ko modifiés sont transférés.

## 2. rsync en local — la base

```bash
# Syntaxe de base
rsync [options] SOURCE DESTINATION

# Copier un dossier et tout son contenu
rsync -av /home/david/Documents/ /tmp/sauvegarde/

# Que signifient les options ?
# -a : mode archive (garde les permissions, dates, propriétaire)
# -v : verbeux (affiche ce qui est copié)
```

Le résultat ressemble à ça :

```
sending incremental file list
./
rapport.pdf
photos/
photos/vacances.jpg
photos/portrait.jpg

sent 2.45M bytes  received 68 bytes  4.90M bytes/sec
```

## 3. Le piège du slash final — ATTENTION !

C'est l'erreur la plus fréquente avec rsync. Le `/` à la fin de la source change tout :

```bash
# AVEC slash final → copie le CONTENU du dossier
rsync -av /home/david/Documents/ /tmp/sauvegarde/
# Résultat : /tmp/sauvegarde/rapport.pdf

# SANS slash final → copie le DOSSIER lui-même
rsync -av /home/david/Documents /tmp/sauvegarde/
# Résultat : /tmp/sauvegarde/Documents/rapport.pdf
```

**Pense-bête :** slash à la fin = « ce qu'il y a dedans »

## 4. Mode simulation : voir avant d'agir

Toujours tester avant une synchro importante avec `-n` (dry-run) :

```bash
# Simuler sans rien copier
rsync -avn /home/david/Documents/ /tmp/sauvegarde/

# Avec des statistiques détaillées
rsync -avn --stats /home/david/Documents/ /tmp/sauvegarde/
```

## 5. Synchroniser avec un serveur distant (via SSH)

```bash
# Envoyer un dossier local vers un serveur
rsync -av /home/david/projet/ user@192.168.1.100:/home/user/projet/

# Récupérer un dossier distant en local
rsync -av user@192.168.1.100:/home/user/projet/ /home/david/projet/

# Avec compression pour les connexions lentes (-z)
rsync -avz /home/david/projet/ user@192.168.1.100:/home/user/projet/
```

**Concrètement**, si tu veux sauvegarder tes documents sur ton PC Ubuntu (192.168.1.119) :

```bash
rsync -avz ~/Documents/ aselophe@192.168.1.119:~/Sauvegardes/
```

## 6. Reprendre un transfert coupé

L'option `-P` combine progression et reprise. Indispensable pour les gros fichiers :

```bash
# Transfert avec barre de progression + reprise possible
rsync -avP gros-fichier.iso user@serveur:/backup/

# Si le transfert est coupé, relance la MÊME commande
# rsync reprend là où il s'était arrêté
```

## 7. Exclure des fichiers

```bash
# Exclure un type de fichier
rsync -av --exclude='*.log' /home/david/projet/ /tmp/sauvegarde/

# Exclure plusieurs motifs
rsync -av --exclude='*.log' --exclude='*.tmp' --exclude='.git/' source/ dest/

# Utiliser un fichier d'exclusions
echo "*.log" > /tmp/exclusions.txt
echo ".git/" >> /tmp/exclusions.txt
echo "node_modules/" >> /tmp/exclusions.txt
rsync -av --exclude-from=/tmp/exclusions.txt source/ dest/
```

## 8. Mode miroir avec --delete

Supprime les fichiers qui n'existent plus dans la source. Pratique pour une copie parfaite :

```bash
# La destination devient un miroir exact de la source
rsync -av --delete /home/david/Documents/ /tmp/miroir/

# ⚠️ ATTENTION : --delete supprime des fichiers !
# Toujours tester avec -n d'abord :
rsync -avn --delete /home/david/Documents/ /tmp/miroir/
```

## 9. Récapitulatif des options essentielles

| Option | Action | Quand l'utiliser |
|--------|--------|-----------------|
| `-a` | Mode archive | Toujours (garde tout intact) |
| `-v` | Verbeux | Pour voir ce qui se passe |
| `-n` | Dry-run (simulation) | Avant toute première synchro |
| `-z` | Compression | Transferts réseau lents |
| `-P` | Progression + reprise | Gros fichiers |
| `--delete` | Miroir (supprime l'extra) | Sauvegardes exactes, avec prudence |
| `--exclude` | Ignorer des fichiers | Fichiers temporaires, logs, .git |

## 10. Exemples concrets de tous les jours

```bash
# Sauvegarde quotidienne de tes documents
rsync -av ~/Documents/ /media/disque-usb/Sauvegarde/

# Envoyer un site web sur ton serveur
rsync -avz --delete ~/mon-site/ user@serveur:/var/www/mon-site/

# Synchroniser deux dossiers en local (bidirectionnel… pas vraiment, rsync est unidirectionnel)
# Pour comparer deux dossiers
rsync -avn --delete dossier1/ dossier2/
```

## 11. Exercices pratiques

1. **Copie locale** — Synchronise ton dossier `~/Documents` vers `/tmp/backup-documents/` en mode verbeux.
2. **Simulation** — Utilise `-n` pour voir ce qui serait copié sans rien modifier.
3. **Exclusion** — Synchronise un dossier en excluant tous les fichiers `.log` et le dossier `.git`.
4. **Sauvegarde distante** — Si tu as accès SSH à une machine, synchronise un petit dossier via SSH.

---

**Résumé :** La commande à retenir pour 90% des cas : `rsync -av source/ destination/`. Ajoute `-n` pour tester, `-z` si c'est à travers le réseau, `-P` pour les gros fichiers.
