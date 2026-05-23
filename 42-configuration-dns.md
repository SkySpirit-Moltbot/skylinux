# Leçon 42 : Configuration DNS et /etc/hosts

Dans cette leçon, tu vas découvrir comment Linux traduit les noms de domaine en adresses IP. Nous verrons le fichier `/etc/hosts`, la résolution DNS, et les outils pour diagnostiquer les problèmes de réseau liés aux noms.

---

## 1. Qu'est-ce que le DNS ?

Le **DNS** (Domain Name System) est l'annuaire d'Internet. Quand tu tapes `google.com`, le DNS traduit ce nom en adresse IP (`142.250.185.46`). Sans DNS, tu devrais mémoriser toutes les adresses IP des sites que tu visites.

**Le flux de résolution DNS :**

```
Ton ordinateur → Serveur DNS (FAI ou Google) → Serveur racine → Serveur autoritaire
```

Sous Linux, la résolution DNS passe par :
- Le fichier `/etc/hosts`
- Le fichier `/etc/resolv.conf`
- Le service `systemd-resolved` (sur les systèmes modernes)

---

## 2. Le fichier /etc/hosts

Le fichier `/etc/hosts` est le moyen le plus simple pour faire correspondre un nom de domaine à une adresse IP. Il est consulté en **premier**, avant même d'interroger les serveurs DNS.

### Voir le contenu par défaut

```bash
cat /etc/hosts
```

```
127.0.0.1   localhost
127.0.1.1   mon-ordinateur

# Les lignes suivantes sont nécessaires pour IPv6
::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
```

### Ajouter une entrée personnalisée

```bash
sudo nano /etc/hosts
```

Ajoute une ligne :

```
192.168.1.100   mon-serveur.local
10.0.0.5        base-de-donnees.local
```

**Après modification**, applique les changements :

```bash
# Pas besoin de redémarrer — le fichier est lu à chaque requête DNS
# Mais pour être sûr, vide le cache DNS :
sudo systemd-resolve --flush-caches
# ou sur certaines distributions :
sudo resolvectl flush-caches
```

### Cas d'usage courants

| Situation | Exemple |
|-----------|---------|
| Serveur local sans DNS | `192.168.1.10   nas.local` |
| Bloquer un site publicitaire | `0.0.0.0   pub.example.com` |
| Rediriger un domaine vers une IP | `203.0.113.50   monsite.dev` |
| Tester un site avant mise en production | `203.0.113.50   www.monsite.com` |

> **Astuce** : Sur certaines distributions (Ubuntu Server 18+), `/etc/hosts` est **stateless** et géré par `systemd-resolved`. Ajoute `--static` dans `/etc/systemd/resolved.conf` si tu veux forcer son utilisation prioritaire.

---

## 3. Le fichier /etc/resolv.conf

Ce fichier contient la liste des **serveurs DNS** que ton système interroge.

```bash
cat /etc/resolv.conf
```

```
nameserver 8.8.8.8
nameserver 8.8.4.4
nameserver 1.1.1.1
```

**Serveurs DNS publics courants :**

| Fournisseur | Serveur primaire | Serveur secondaire |
|-------------|------------------|--------------------|
| Google | `8.8.8.8` | `8.8.4.4` |
| Cloudflare | `1.1.1.1` | `1.0.0.1` |
| Quad9 | `9.9.9.9` | `149.112.112.112` |

### Modifier les serveurs DNS

```bash
sudo nano /etc/resolv.conf
```

Ajoute ou remplace les lignes `nameserver` :

```
nameserver 1.1.1.1
nameserver 8.8.8.8
```

> **Note** : Sur les systèmes avec `systemd-resolved`, ce fichier est souvent un **lien symbolique**. Modifie plutôt `/etc/systemd/resolved.conf` :

```bash
sudo nano /etc/systemd/resolved.conf
```

```
[Resolve]
DNS=1.1.1.1 8.8.8.8
DNSOverTLS=no
Cache=yes
```

Puis redémarre le service :

```bash
sudo systemctl restart systemd-resolved
```

---

## 4. Ordre de résolution : /etc/nsswitch.conf

Le fichier `/etc/nsswitch.conf` détermine **l'ordre** dans lequel les sources de résolution sont consultées.

```bash
grep "^hosts:" /etc/nsswitch.conf
```

```
hosts:          files dns
```

Cela signifie :
1. D'abord **`files`** → `/etc/hosts`
2. Ensuite **`dns`** → serveurs DNS de `/etc/resolv.conf`

Tu peux modifier cet ordre. Par exemple, pour ignorer le DNS :

```
hosts:          files
```

Ou pour ajouter un annuaire LDAP :

```
hosts:          files dns ldap
```

---

## 5. Outils de diagnostic DNS

### Vérifier la résolution avec `dig`

```bash
# Résolution simple
dig google.com

# Avec un serveur DNS spécifique
dig @1.1.1.1 github.com

# Voir seulement la réponse
dig github.com +short
```

Résultat de `dig google.com` :

```
; <<>> DiG 9.18.1 <<>> google.com
;; ANSWER SECTION:
google.com.     299     IN      A       142.250.185.46
```

### Vérifier avec `nslookup`

```bash
nslookup google.com
```

```
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.185.46
```

### Vérifier avec `host`

```bash
host google.com
```

```
google.com has address 142.250.185.46
google.com has IPv6 address 2a00:1450:4007:812::200e
```

### Tester la propagation DNS

```bash
# Voir depuis quel serveur DNS vient la réponse
dig +trace monsite.com
```

### Vider le cache DNS

```bash
# systemd-resolved
sudo resolvectl flush-caches

# ou via systemd :
sudo systemd-resolve --flush-caches

# dnsmasq
sudo systemctl restart dnsmasq
```

---

## 6. /etc/hosts vs DNS : lequel choisir ?

| Critère | `/etc/hosts` | DNS |
|---------|-------------|-----|
| Portée | Locale (machine) | Globale (réseau) |
| Vitesse | Instantané (fichier local) | Dépend du réseau |
| Maintenance | Manuelle | Automatique |
| Idéal pour | Serveurs locaux, tests | Production, sites publics |

**Règle simple** :
- Utilise `/etc/hosts` pour tes machines locales et tes tests.
- Utilise DNS pour les noms de domaine publics.

---

## 7. Bloquer les publicités avec /etc/hosts

Une utilisation pratique de `/etc/hosts` est de bloquer les publicités et trackers.

```bash
# Exemple : bloquer un domaine publicitaire
sudo nano /etc/hosts
```

Ajoute :

```
0.0.0.0   ads.google.com
0.0.0.0   tracking.analytics.com
0.0.0.0   pub.cdn.example.com
```

> **0.0.0.0** est préféré à `127.0.0.1` car `127.0.0.1` peut charger un serveur web local et ralentir la connexion.

Tu peux aussi utiliser des listes préconstruites :

```bash
# Installer une liste de blocage
sudo curl -o /etc/hosts https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
```

---

## 8. Exercices pratiques

### Exercice 1 : Ajouter une entrée dans /etc/hosts

1. Ouvre le fichier `/etc/hosts` avec `nano`
2. Ajoute une entrée `127.0.0.1   mon-test.local`
3. Teste avec `ping mon-test.local` — tu dois recevoir des réponses de `127.0.0.1`
4. Supprime la ligne que tu as ajoutée

### Exercice 2 : Changer de serveur DNS

1. Vérifie ton serveur DNS actuel : `cat /etc/resolv.conf | grep nameserver`
2. Changes le pour Cloudflare (`1.1.1.1`) dans `/etc/resolv.conf`
3. Teste la résolution : `dig github.com +short`
4. Restore le serveur DNS original

### Exercice 3 : Diagnostic DNS

1. Utilise `dig` pour résoudre `ubuntu.com`
2. Utilise `dig @1.1.1.1 ubuntu.com` avec Cloudflare
3. Compare les temps de réponse (`Query time:`)
4. Utilise `host` pour obtenir les enregistrements IPv6

---

## Résumé

| Concept | Commande / Fichier |
|---------|-------------------|
| Fichier hosts local | `/etc/hosts` |
| Serveurs DNS | `/etc/resolv.conf` |
| Ordre de résolution | `/etc/nsswitch.conf` |
| Diagnostic DNS | `dig`, `nslookup`, `host` |
| Vider le cache DNS | `sudo resolvectl flush-caches` |
| Configurer systemd-resolved | `/etc/systemd/resolved.conf` |

Le DNS est un pilier d'Internet. Comprendre `/etc/hosts` et les outils de diagnostic te permettra de résoudre rapidement les problèmes de réseau et de configurer tes propres serveurs.
