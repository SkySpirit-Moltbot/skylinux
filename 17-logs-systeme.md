# Leçon 17 : Les logs système

## Objectif

Découvrir comment consulter et analyser les journaux système sous Linux.

## Pourquoi les logs ?

Les fichiers de log (journaux) contiennent l'historique de tout ce qui se passe sur votre système : connexions, erreurs, services démarrés, etc. C'est essentiel pour dépanner et surveiller votre machine.

## Où trouvent-on les logs ?

La plupart des logs sont dans **/var/log/** :

- `/var/log/syslog` ou `/var/log/messages` – messages généraux du système
- `/var/log/auth.log` – connexions et authentifications
- `/var/log/dmesg` – messages du noyau (boot)
- `/var/log/nginx/` ou `/var/log/apache2/` – logs des serveurs web
- `/var/log/apt/` – historique des installations de paquets

## Commandes de base

### Lire un log en direct (suivre les nouvelles lignes)
```bash
tail -f /var/log/syslog
```

### Voir les dernières lignes d'un fichier
```bash
tail -n 20 /var/log/syslog
```

### Rechercher un mot dans un log
```bash
grep "error" /var/log/syslog
grep -i "failed" /var/log/auth.log
```

### Compter les occurrences
```bash
grep -c "error" /var/log/syslog
```

### Voir les logs en temps réel avec journalctl (systemd)
```bash
journalctl -xe                    # voir les dernières entrées
journalctl -u nginx.service       # logs d'un service spécifique
journalctl --since "1 hour ago"   # depuis 1 heure
journalctl -b                     # logs depuis le dernier démarrage
```

## Exemple pratique

Imaginons qu'un service ne démarre pas. Voici la démarche :

1. Vérifier le statut du service :
```bash
sudo systemctl status nginx
```

2. Consulter les logs du service :
```bash
sudo journalctl -u nginx -n 50
```

3. Chercher les erreurs :
```bash
sudo journalctl -u nginx | grep -i error
```

## Exercice

1. Affiche les 10 dernières lignes de `/var/log/syslog`
2. Recherche toutes les occurrences du mot "failed" dans `/var/log/auth.log`
3. Utilise `journalctl` pour voir les logs de ta session actuelle

## Résumé

| Commande | Utilité |
|----------|---------|
| `tail -f` | Suivre un log en direct |
| `tail -n X` | Afficher les X dernières lignes |
| `grep` | Rechercher dans un fichier |
| `journalctl` | Consulter les logs systemd |
| `less` | Naviguer dans un gros fichier (`q` pour quitter) |

Les logs sont tes alliés pour comprendre ce qui se passe et résoudre les problèmes !
