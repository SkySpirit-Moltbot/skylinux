# Leçon 37 : Sécuriser Linux avec UFW (Pare-feu)

Dans cette leçon, tu vas découvrir comment protéger ton système Linux avec **UFW** (*Uncomplicated Firewall*), un outil simple et efficace pour gérer le pare-feu intégré au noyau Linux (iptables/nftables).

---

## 1. Qu'est-ce qu'un pare-feu ?

Un **pare-feu** (firewall) est un filtrage qui décide quelles connexions réseau sont autorisées ou bloquées. Sans lui, n'importe qui peut se connecter à ton ordinateur. Avec lui, tu contrôle le trafic :

- **Entrant** (IN) : connexions vers ta machine (serveur web, SSH...)
- **Sortant** (OUT) : connexions depuis ta machine (navigation, mises à jour...)

Linux intègre un pare-feu puissant dans le noyau : **iptables** (ou **nftables**). Mais它们的 commandes sont complexes. **UFW**简化了这个过程。

---

## 2. Installer UFW

UFW est généralement **préinstallé** sur Ubuntu. Pour les autres distributions :

```bash
# Debian / Ubuntu / Linux Mint
sudo apt install ufw

# Fedora
sudo dnf install ufw

# Vérifier le statut
sudo ufw status
```

---

## 3. Règles de base

### Voir le statut

```bash
# Statut actuel (actif/inactif, règles en place)
sudo ufw status verbose
```

### Activer / Désactiver le pare-feu

```bash
# Activer UFW (appliquera les règles définies)
sudo ufw enable

# Désactiver UFW (tout ouvert)
sudo ufw disable
```

> ⚠️ **Attention** : si tu te connectes en SSH et que le pare-feu est inactive, assieds-toi d'abord une règle SSH AVANT d'activer UFW !

---

## 4. Autoriser ou Bloquer des Ports

### Autoriser un port (entrant)

```bash
# Autoriser le port 80 (HTTP)
sudo ufw allow 80/tcp

# Autoriser le port 443 (HTTPS)
sudo ufw allow 443/tcp

# Autoriser un service par son nom
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
```

### Bloquer un port (entrant)

```bash
# Bloquer le port 23 (Telnet — non sécurisé)
sudo ufw deny 23/tcp

# Bloquer tout le trafic entrant (très restrictif)
sudo ufw default deny incoming
```

### Autoriser depuis une IP ou un réseau

```bash
# Autoriser une IP spécifique
sudo ufw allow from 192.168.1.100

# Autoriser un réseau entier
sudo ufw allow from 192.168.1.0/24

# Autoriser SSH uniquement depuis le réseau local
sudo ufw allow from 192.168.1.0/24 to any port 22
```

---

## 5. Supprimer une règle

```bash
# Voir les règles avec leurs numéros
sudo ufw status numbered

# Supprimer la règle n°3
sudo ufw delete 3

# Supprimer une règle par sa définition
sudo ufw delete allow 80/tcp
```

---

## 6. Logging (journalisation)

```bash
# Niveau basique
sudo ufw logging low

# Niveau moyen (recommandé)
sudo ufw logging medium

# Désactiver les logs
sudo ufw logging off

# Lire les logs
sudo tail -f /var/log/ufw.log
```

---

## 7. Configuration pour un serveur SSH

C'est le cas le plus courant — on veut sécuriser l'accès SSH :

```bash
# 1. Autoriser SSH (port 22)
sudo ufw allow ssh

# Ou explicitement :
sudo ufw allow 22/tcp

# 2. Si tu te connectes depuis une IP fixe, encore mieux :
sudo ufw allow from 192.168.1.50 to any port 22

# 3. Tout le reste en entrée : refuser
sudo ufw default deny incoming

# 4. Sortie : tout autorisé (par défaut)
sudo ufw default allow outgoing

# 5. Activer le pare-feu
sudo ufw enable
```

---

## 8. Réinitialiser UFW

```bash
# Remettre à zéro (efface toutes les règles)
sudo ufw reset
```

---

## Exercice pratique

**Objectif :** Configure UFW sur ta machine pour un usage bureautique sécurisé.

1. Installe UFW si pas déjà présent
2. Affiche le statut actuel (`sudo ufw status verbose`)
3. Configure ces règles dans l'ordre :
   - `sudo ufw default deny incoming` (tout refuser par défaut)
   - `sudo ufw allow out 53/udp` (DNS sortant)
   - `sudo ufw allow out 80/tcp` (HTTP sortant)
   - `sudo ufw allow out 443/tcp` (HTTPS sortant)
   - `sudo ufw allow ssh` (si tu te connectes en SSH)
   - `sudo ufw allow 22/tcp` (si pas encore fait)
4. Active UFW : `sudo ufw enable`
5. Vérifie : `sudo ufw status numbered`
6. Teste la navigation web (elle doit fonctionner)
7. Lis les logs : `sudo tail -5 /var/log/ufw.log`

---

## Résumé

| Commande | Rôle |
|----------|------|
| `sudo ufw status` | Voir l'état du pare-feu |
| `sudo ufw enable` | Activer UFW |
| `sudo ufw disable` | Désactiver UFW |
| `sudo ufw allow <port>` | Autoriser un port |
| `sudo ufw deny <port>` | Bloquer un port |
| `sudo ufw delete <règle>` | Supprimer une règle |
| `sudo ufw status numbered` | Lister les règles avec numéros |
| `sudo ufw reset` | Réinitialiser UFW |

UFW permet de sécuriser ta machine en quelques commandes. Pour un serveur, pense toujours à autoriser **SSH en premier** avant d'activer le pare-feu.

---

## Complément: iptables

### Concept : Les chaînes (chains)

iptables organise les règles en chaînes. Chaque paquet réseau traverse ces chaînes et est examiné par les règles.

INPUT : paquets destinés à ta machine

OUTPUT : paquets originates de ta machine

FORWARD : paquets qui transitent par ta machine (routeur)

PREROUTING : avant le routage (NAT)

POSTROUTING : après le routage (NAT)

### Concept : Les cibles (targets)

Quand un paquet correspond à une règle, une cible est appliquée :

ACCEPT : autoriser le paquet

DROP : ignorer le paquet (sans réponse)

REJECT : rejeter le paquet (avec message d'erreur)

LOG : enregistrer le paquet dans les logs

### Afficher les règles actuelles

Explication des options :

-L : afficher les règles

-v : mode verbeux (afficher les compteurs)

-n : ne pas résoudre les noms (afficher les IP, pas les noms de domaine)

Affiche les règles de la chaîne INPUT avec les numéros de ligne.

### Règles de base

-A INPUT ajoute une règle à la chaîne INPUT, -i lo targets l'interface loopback, -j ACCEPT accepte les paquets.

-m state charge le module state, --state ESTABLISHED,RELATED cible les connexions déjà établies ou liées.

-p tcp targets le protocole TCP, --dport 22 cible le port destination 22.

-s spécifie l'adresse source.

Cette règle limite à 100 connexions simultanées sur le port 80.

### Gérer les règles

Supprime la règle numéro 3 de la chaîne INPUT.

-F vide la chaîne INPUT.

Remplace la règle 5 dans INPUT.

-I INPUT 1 insère la règle en position 1 (au début).

### Politiques par défaut

Par défaut, toutes les chaînes acceptent tout. Pour changer :

Attention : si tu changes la politique INPUT en DROP sans avoir autorisé le trafic localhost et les connexions établies, tu risques de te retrouver bloqué hors de ta machine !

### Sauvegarder et restaurer les règles

Sur Debian/Ubuntu, utilise plutôt :

Cela sauvegarde automatiquement dans /etc/sysconfig/iptables.

### Loguer les paquets bloqués

Les logs apparaîtront dans /var/log/syslog ou /var/log/messages selon ta distribution.

### Bonnes pratiques

Commence par tout interdire (-P INPUT DROP)

Autorise le loopback en premier (-i lo -j ACCEPT)

Autorise les connexions établies pour ne pas casser les sessions

Place les règles les plus spécifiques avant les générales

Sauvegarde toujours tes règles avant de tester de nouvelles configurations

Teste en local si possible, ou garde un accès SSH ouvert

### Exercices pratiques

Affiche les règles iptables actuelles avec sudo iptables -L -v -n.

Ajoute une règle pour autoriser le port 80 (HTTP).

Bloque le trafic entrant depuis une IP spécifique de ton choix.

Supprime une règle que tu viens de créer.

Sauvegarde tes règles et restaure-les pour vérifier que ça fonctionne.

Crée un script qui configure un pare-feu de base pour un serveur web (ports 22, 80, 443).

---

## Complément: nftables

### Pourquoi passer à nftables ?

iptables utilise quatre outils distincts (iptables, ip6tables, arptables, ebtables) pour gérer IPv4, IPv6, ARP et les bridges. nftables unifie tout cela dans un seul outil cohérent. De plus, les règles iptables sont directement convertibles vers nftables.

### Concepts fondamentaux

nftables organise les règles en trois niveaux :

Table : conteneur de niveau supérieur, attaché à une famille réseau (ip, ip6, inet, arp, bridge, netdev)

Chaîne : contient les règles, possède un type (filter, nat, route, etc.) et un crochet (hook)

Règle : action appliquée à un paquet (accepter, rejeter,.Drop, NATer...)

ip : IPv4 uniquement

ip6 : IPv6 uniquement

inet : mélange IPv4 et IPv6 (recommandé)

arp : protocole ARP

bridge : pont réseau

netdev : attaches de bas niveau

### Premiers pas avec nftables

Affiche les règles actuelles (vide si aucune règle n'est définie).

Crée une table nommée mon_parefeu dans la famille inet (IPv4 + IPv6).

Crée une chaîne INPUT de type filter accrochée sur le hook input, avec priorité 0 et politique par défaut drop.

### Afficher les règles

Affiche toutes les règles actives.

Affiche uniquement les règles de la table demandée.

Affiche uniquement les règles de la chaîne input.

### Supprimer des règles

L'option -a affiche les handles de chaque règle.

Supprime la règle portant le handle 3.

Attention : cela supprime toutes les tables et règles.

### Insérer et remplacer des règles

Cette règle bloque le trafic entrant depuis 192.168.1.50.

### Bloquage avancé

Limite à 10 connexions par seconde sur le port 80.

Les logs apparaîtront dans /var/log/kern.log ou /var/log/syslog.

### NAT (Network Address Translation)

Active le MASQUERADE pour le réseau 192.168.1.0/24 sur l'interface eth0 (partage de connexion).

Redirige le trafic TCP du port 8080 vers 192.168.1.100:80.

### Sauvegarder et restaurer les règles

Le service nftables charge automatiquement /etc/nftables.conf au démarrage.

### Exemple complet : pare-feu pour serveur web

Sauvegarde ce contenu dans /etc/nftables.conf et charge-le avec sudo nft -f /etc/nftables.conf.

### Convertir iptables vers nftables

La commande iptables-restore peut convertir automatiquement tes règles iptables :

Ou de façon permanente :

### Commandes utiles pour le diagnostic

sudo nft list ruleset -a : afficher avec les handles

sudo nft monitor : afficher les changements de règles en temps réel

sudo nft monitor trace : tracer le trajet des paquets

sudo nft reset table inet mon_parefeu : réinitialiser une table

### Bonnes pratiques

Commence toujours par une politique drop sur la chaîne input

Utilise la famille inet pour gérer IPv4 et IPv6 dans la même table

Teste avec une session SSH ouverte avant d'activer le pare-feu — garde toujours un accès

Sauvegarde dans /etc/nftables.conf pour le démarrage automatique

Utilise un script pour décrire tes règles de manière lisible (voir exemple ci-dessus)

Vérifie régulièrement tes règles avec nft list ruleset

### Exercices pratiques

Vérifie si nftables est installé sur ta machine : which nft && nft -v

Crée une table inet test_parefeu et ajoute les règles de base (loopback, established, SSH, HTTP/HTTPS).

Affiche tes règles avec sudo nft list ruleset.

Bloque le trafic depuis une IP de test (par exemple 10.255.255.1).

Sauvegarde tes règles dans un fichier et restaure-les.

Inverse le problème : remplace une règle existante par une autre.
