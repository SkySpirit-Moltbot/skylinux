# Leçon 24 : Configuration réseau avancée

## Introduction

Cette leçon aborde les concepts avancés de configuration réseau sous Linux. Vous apprendrez à configurer des interfaces réseau, mettre en place un serveur DHCP, un serveur DNS, et à comprendre le routage avancé.

## Configuration des interfaces réseau

### IP statique vs DHCP

#### Configuration avec ip (temporaire)

```bash
# Ajouter une adresse IP
ip addr add 192.168.1.100/24 dev eth0

# Activer l'interface
ip link set eth0 up

# Désactiver l'interface
ip link set eth0 down

# Supprimer une adresse IP
ip addr del 192.168.1.100/24 dev eth0
```

#### Configuration persistente (Debian/Ubuntu)

Éditez le fichier `/etc/network/interfaces` :

```bash
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

#### Configuration avec systemd-networkd

Créez un fichier dans `/etc/systemd/network/` :

```ini
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=8.8.8.8
```

## Serveur DHCP

### Installation et configuration de dnsmasq

Dnsmasq est un serveur DHCP et DNS léger :

```bash
# Installation
sudo apt install dnsmasq

# Configuration (/etc/dnsmasq.conf)
interface=eth0
bind-interfaces
dhcp-range=192.168.1.50,192.168.1.150,12h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,8.8.8.8
```

### Commandes de gestion DHCP

```bash
# Démarrer le service
sudo systemctl start dnsmasq

# Activer au démarrage
sudo systemctl enable dnsmasq

# Voir les baux DHCP actifs
cat /var/lib/misc/dnsmasq.leases
```

## Serveur DNS

### Configuration locale (/etc/hosts)

```bash
# Fichier hosts local
sudo nano /etc/hosts

# Ajoutez vos entrées
192.168.1.10    serveur.local
192.168.1.20    mondomaine.com
```

### Configuration du resolve.conf

```bash
sudo nano /etc/resolv.conf

nameserver 8.8.8.8
nameserver 8.8.4.4
search mondomaine.com
```

### Serveur DNS avec bind9

```bash
# Installation
sudo apt install bind9 bind9utils

# Configuration de zone (/etc/bind/named.conf.local)
zone "mondomaine.local" {
    type master;
    file "/etc/bind/db.mondomaine.local";
};

# Fichier de zone
$TTL    604800
@       IN      SOA     ns.mondomaine.local. admin.mondomaine.local. (
                     2024031801         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns.mondomaine.local.
@       IN      A       192.168.1.10
ns      IN      A       192.168.1.10
www     IN      CNAME   @
```

## Routage avancé

### Table de routage

```bash
# Voir la table de routage
ip route show
ip route list

# Ajouter une route statique
ip route add 10.0.0.0/24 via 192.168.1.1 dev eth0

# Route par défaut
ip route add default via 192.168.1.1

# Supprimer une route
ip route del 10.0.0.0/24
```

### IP forwarding (routeur)

```bash
# Activer le routage temporairement
echo 1 > /proc/sys/net/ipv4/ip_forward

# Configuration permanente (/etc/sysctl.conf)
net.ipv4.ip_forward=1

# Appliquer sans redémarrer
sudo sysctl -p
```

### NAT (Network Address Translation)

```bash
# NAT pour le traffic sortant
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Redirection de port
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080

# Sauvegarder les règles
sudo iptables-save > /etc/iptables/rules.v4
```

## Pare-feu avec iptables

### Règles de base

```bash
# Politique par défaut : tout rejeter
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Autoriser localhost
iptables -A INPUT -i lo -j ACCEPT

# Autoriser les connexions établies
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Autoriser SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Autoriser HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Voir les règles
iptables -L -n -v
```

### Gestion du pare-feu

```bash
# Effacer toutes les règles
iptables -F

# Supprimer une règle spécifique
iptables -D INPUT -p tcp --dport 22 -j ACCEPT

# Sauvegarder les règles
sudo iptables-save > /etc/iptables.rules

# Restaurer les règles
sudo iptables-restore < /etc/iptables.rules
```

## Outils de diagnostic réseau

```bash
# Tester la connectivité
ping -c 4 8.8.8.8

# Tracer le parcours
traceroute google.com
tracepath google.com

# Tester un port spécifique
nc -zv google.com 80
telnet google.com 80

# Analyser le trafic
tcpdump -i eth0
tcpdump -i eth0 port 80

# Informations détaillée sur une interface
ethtool eth0
mii-tool eth0
```

## Résumé des commandes

| Commande | Utilité |
|----------|---------|
| `ip addr` | Configurer les adresses IP |
| `ip route` | Gérer le routage |
| `iptables` | Configurer le pare-feu |
| `dnsmasq` | Serveur DHCP/DNS léger |
| `bind9` | Serveur DNS complet |
| `traceroute` | Tracer le parcours réseau |
| `tcpdump` | Analyser le trafic réseau |
| `ethtool` | Informations sur l'interface |

## Exercice pratique

1. Affichez votre configuration réseau actuelle avec `ip addr` et `ip route`
2. Configurez une adresse IP statique sur une interface secondaire
3. Installez et configurez dnsmasq pour un petit réseau local
4. Mettez en place des règles iptables basiques
5. Testez la connectivité vers plusieurs hôtes avec ping et traceroute
6. Expérimentez avec la redirection de port

## Conclusion

La maîtrise de la configuration réseau avancée est essentielle pour administrer des serveurs Linux. Ces connaissances vous permettront de mettre en place des infrastructures réseau complètes, depuis le DHCP jusqu'au pare-feu, en passant par le routage et le DNS.