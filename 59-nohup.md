# Leçon 59 : nohup — Exécuter des commandes persistantes

`nohup` (no hangup) protège une commande de la déconnexion. Si tu fermes le terminal, la commande continue de tourner.

## 1. Le problème

```bash
# Tu lances un script long dans un terminal SSH...
./traitement_long.sh

# ...la connexion SSH coupe → le script est TUÉ
# Dommage si ça faisait 3 heures que ça tournait !
```

## 2. La solution : nohup

```bash
# La commande survit à la déconnexion
nohup ./traitement_long.sh &

# Sortie redirigée automatiquement vers nohup.out
```

Que fait `nohup` exactement ?
- Ignore le signal `SIGHUP` (envoyé à la déconnexion)
- Redirige stdout/stderr vers `nohup.out` si pas déjà redirigés
- Ne bloque pas le terminal si utilisé avec `&`

## 3. Utilisation pratique

```bash
# Lancer un script long
nohup ./backup_complet.sh > backup.log 2>&1 &

# Voir le PID (numéro de processus)
echo $!
# → 12345

# Vérifier qu'il tourne toujours
ps -p 12345

# Voir les logs en direct
tail -f backup.log

# Arrêter proprement
kill 12345
```

## 4. nohup vs screen vs tmux

| Outil | Usage | Quand |
|-------|-------|-------|
| `nohup` | Commande unique, feu et oublie | Scripts batch, une tâche |
| `screen` | Session ré-attachable | Travail interactif long |
| `tmux` | Session ré-attachable moderne | Développement, multitâche |

```bash
# nohup : tu n'as pas besoin de te reconnecter
nohup ./script.sh > log.txt 2>&1 &

# tmux : tu veux pouvoir te reconnecter et voir l'état
tmux new -s travail
./script_interactif.sh
# Ctrl+B D pour détacher, tmux attach -t travail pour revenir
```

## 5. Astuce : bien logger

```bash
# Rediriger TOUTE la sortie (stdout + stderr)
nohup ./script.sh > /tmp/script.log 2>&1 &

# Avec la date dans le nom du log
nohup ./script.sh > "/tmp/script_$(date +%Y%m%d_%H%M).log" 2>&1 &

# Vérifier que ça tourne
jobs -l
```

## 6. Exercices pratiques

1. **Test nohup** — Lance `nohup sleep 120 &` puis vérifie que le processus existe avec `ps`
2. **Déconnexion** — Connecte-toi en SSH, lance `nohup sleep 300 &`, déconnecte-toi, reconnecte et vérifie avec `ps`
3. **Logs** — Lance un script avec nohup et vérifie le contenu de `nohup.out`
