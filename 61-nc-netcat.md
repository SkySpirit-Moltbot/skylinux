# Leçon 61 : nc — Netcat, le couteau suisse du réseau

`nc` (netcat) lit et écrit des données à travers le réseau. Un outil minimaliste capable de tout : transfert de fichiers, chat, scan de ports, serveur web minimal.

## 1. Vérifier qu'un port est ouvert

```bash
# Tester si le port 80 est ouvert sur un serveur
nc -zv 192.168.1.100 80
# -z : scan sans envoyer de données
# -v : verbeux

# Tester une plage de ports
nc -zv 192.168.1.100 20-25

# Exemple : vérifier que SSH répond
nc -zv 192.168.1.119 22
# → Connection to 192.168.1.119 22 port [tcp/ssh] succeeded!
```

## 2. Chat minimaliste entre deux machines

```bash
# Machine A — Serveur (écoute)
nc -l 1234

# Machine B — Client (se connecte)
nc 192.168.1.100 1234

# Tape du texte de chaque côté, il apparaît chez l'autre.
# Ctrl+C pour quitter.
```

## 3. Transférer un fichier

```bash
# Machine A — Reçoit le fichier (serveur)
nc -l 1234 > fichier_recu.txt

# Machine B — Envoie le fichier (client)
nc 192.168.1.100 1234 < fichier_a_envoyer.txt

# Avec barre de progression (via pv)
# Récepteur :
nc -l 1234 | pv > gros_fichier.iso
# Émetteur :
pv gros_fichier.iso | nc 192.168.1.100 1234
```

## 4. Servir une page web (one-shot)

```bash
# Créer une réponse HTTP minimale
echo -e "HTTP/1.1 200 OK\n\n<h1>Ça marche !</h1>" | nc -l 8080 -q 1

# Ouvre http://localhost:8080 dans un navigateur
# La connexion se ferme après avoir servi la page.
```

## 5. Cloner un disque à travers le réseau

```bash
# Machine source (envoie le disque)
dd if=/dev/sda | nc 192.168.1.200 9999

# Machine destination (reçoit et écrit)
nc -l 9999 | dd of=/dev/sdb

# ⚠️ Extrêmement puissant et dangereux. Vérifie 3 fois avant.
```

## 6. Options utiles

```bash
# -l : mode écoute (serveur)
# -p : spécifier le port
# -v : verbeux
# -z : scan sans données
# -w : timeout en secondes
nc -w 5 -zv serveur 80

# -k : garder le serveur actif après déconnexion (répéter)
nc -lk 1234

# -u : mode UDP (défaut = TCP)
nc -ul 1234
```

## 7. Exercices pratiques

1. **Scan** — Vérifie que le port 22 (SSH) est ouvert sur `localhost`
2. **Chat** — Ouvre deux terminaux et fais un chat local avec nc
3. **Fichier** — Transfère un petit fichier texte entre deux terminaux avec nc
