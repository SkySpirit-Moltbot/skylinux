# Leçon 21 : Gestion des services avec systemd

## Introduction

**systemd** est le système d'initialisation et le gestionnaire de services le plus utilisé dans les distributions Linux modernes (Ubuntu, Debian, Fedora, CentOS, etc.). Il permet de démarrer, arrêter, redémarrer et gérer les services (daemons) du système.

Dans cette leçon, nous allons apprendre à utiliser la commande `systemctl` pour gérer les services.

## Concepts de base

### Qu'est-ce qu'un service ?

Un service (ou daemon) est un programme qui tourne en arrière-plan et qui est démarré automatiquement au démarrage du système. Exemples :
- `nginx` : serveur web
- `sshd` : serveur SSH
- `cron` : gestionnaire de tâches planifiées
- `systemd-logind` : gestion des connexions utilisateur

### Les cibles (targets)

Les cibles (`targets`) sont des groupes de services qui définissent un état du système. Les plus courantes :
- `multi-user.target` : système multi-utilisateur sans interface graphique
- `graphical.target` : système avec interface graphique
- `rescue.target` : mode rescue (mode mono-utilisateur)
- `poweroff.target` : arrêt du système

## Commandes de base avec systemctl

### Voir le statut d'un service

```bash
# Voir le statut d'un service spécifique
sudo systemctl status nginx

# Statut sans les détails (plus concis)
sudo systemctl is-active nginx

# Vérifier si un service est activé au démarrage
sudo systemctl is-enabled nginx
```

### Démarrer et arrêter un service

```bash
# Démarrer un service
sudo systemctl start nginx

# Arrêter un service
sudo systemctl stop nginx

# Redémarrer un service (arrêt + démarrage)
sudo systemctl restart nginx

# Recharger la configuration sans arrêter le service
sudo systemctl reload nginx
```

### Activer ou désactiver un service

```bash
# Activer un service au démarrage (démarrage automatique)
sudo systemctl enable nginx

# Désactiver un service au démarrage
sudo systemctl disable nginx

# Activer et démarrer immédiatement
sudo systemctl enable --now nginx
```

### Lister les services

```bash
# Lister tous les services actifs
systemctl list-units --type=service

# Lister tous les services (actifs et inactifs)
systemctl list-units --type=service --all

# Lister les services qui ont échoué
systemctl --failed --type=service
```

### Voir les journaux d'un service

```bash
# Voir les journaux d'un service (logs)
sudo journalctl -u nginx

# Suivre les journaux en temps réel
sudo journalctl -u nginx -f

# Voir les journaux depuis le dernier démarrage
sudo journalctl -u nginx --since today
```

## Exemples pratiques

### Exemple 1 : Gestion du service SSH

```bash
# Vérifier le statut de SSH
sudo systemctl status ssh

# Démarrer SSH
sudo systemctl start ssh

# Activer SSH au démarrage
sudo systemctl enable ssh

# Voir les journaux SSH
sudo journalctl -u ssh
```

### Exemple 2 : Gestion du service Cron

```bash
# Statut de cron
sudo systemctl status cron

# Redémarrer cron pour prendre en compte les changements
sudo systemctl restart cron

# Vérifier si cron est actif
systemctl is-active cron
```

### Exemple 3 : Analyser pourquoi un service ne démarre pas

```bash
# Voir le statut détaillé
sudo systemctl status nginx

# Voir les dernières lignes de journal
sudo journalctl -xe -u nginx

# Voir la configuration du service
sudo systemctl cat nginx
```

## Exercice pratique

1. **Vérifier le statut de votre service cron** :
   ```bash
   systemctl status cron
   ```

2. **Activer le service cron au démarrage** :
   ```bash
   sudo systemctl enable cron
   ```

3. **Créer un script de test** dans `/tmp/test_service.sh` :
   ```bash
   #!/bin/bash
   echo "Mon script de test" >> /tmp/test.log
   ```

4. **Créer un service systemd** dans `/etc/systemd/system/test.service` :
   ```bash
   [Unit]
   Description=Mon service de test

   [Service]
   Type=oneshot
   ExecStart=/tmp/test_service.sh

   [Install]
   WantedBy=multi-user.target
   ```

5. **Tester le service** :
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start test
   cat /tmp/test.log
   sudo systemctl enable test
   ```

## Résumé

- **systemd** est le gestionnaire de services standard sous Linux
- **`systemctl`** est la commande principale pour gérer les services
- **Démarrer/arrêter** : `systemctl start/stop [service]`
- **Redémarrer** : `systemctl restart [service]`
- **Statut** : `systemctl status [service]`
- **Activer au démarrage** : `systemctl enable [service]`
- **Désactiver au démarrage** : `systemctl disable [service]`
- **Journaux** : `journalctl -u [service]`
- **Lister les services** : `systemctl list-units --type=service`

La maîtrise de systemd est essentielle pour administrer un système Linux moderne. Les commandes vues dans cette leçon vous permettront de gérer efficacement les services de votre système.