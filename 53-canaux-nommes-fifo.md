# Leçon 53 : Canaux nommés (Named Pipes / FIFO)

Un canal nommé (FIFO) permet à deux processus de communiquer via un fichier spécial, même s'ils n'ont aucun lien entre eux.

## 1. C'est quoi une FIFO ?

Contrairement au pipe classique `|` qui relie deux commandes sur une même ligne, une FIFO est un **fichier spécial** qui persiste sur le disque. Un processus écrit dedans, un autre lit — et les données transitent en mémoire, pas sur le disque.

## 2. Créer une FIFO

```bash
# Créer un canal nommé
mkfifo mon_tube

# Voir son type (p = pipe)
ls -l mon_tube
# prw-r--r-- 1 david david 0 Mar 10 10:00 mon_tube
# ↑ le 'p' indique un pipe nommé
```

## 3. Utilisation de base

La FIFO bloque jusqu'à ce qu'un lecteur et un écriveur soient connectés :

```bash
# Terminal 1 — Lecteur (reste bloqué en attente)
cat mon_tube

# Terminal 2 — Écriveur (débloque le lecteur)
echo "Message à travers le tube" > mon_tube
```

Dès que le Terminal 2 exécute sa commande, le Terminal 1 affiche le message et les deux se terminent.

## 4. Cas concret : communication entre scripts

```bash
# Script producteur (producer.sh)
#!/bin/bash
while true; do
  echo "$(date): Nouvelle donnée" > /tmp/data_pipe
  sleep 2
done

# Script consommateur (consumer.sh)
#!/bin/bash
while true; do
  read line < /tmp/data_pipe
  echo "Reçu: $line"
done
```

## 5. FIFO + compression à la volée

```bash
# Créer la FIFO
mkfifo /tmp/backup_pipe

# Lecteur : compresse ce qui arrive dans la FIFO
gzip < /tmp/backup_pipe > sauvegarde.tar.gz &

# Écriveur : envoie l'archive tar dans la FIFO
tar cf /tmp/backup_pipe /home/david/Documents/

# Nettoyage
rm /tmp/backup_pipe
```

## 6. Supprimer une FIFO

```bash
# Se supprime comme un fichier normal
rm mon_tube

# Un tube nommé ne stocke rien sur le disque, rm est sans danger
```

## 7. Exercices pratiques

1. **Premier tube** — Crée une FIFO, lis-la dans un terminal, écris dedans depuis un autre
2. **Log en direct** — Utilise une FIFO pour qu'un script écrive des logs et un autre les affiche
3. **Compression** — Reproduis l'exemple de compression à la volée avec tar et gzip

---

**À retenir** : les FIFO sont utiles pour connecter des processus indépendants. Pour les pipes simples entre commandes, `|` suffit dans 95% des cas.
