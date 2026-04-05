# Leçon 46 : Priorité des processus avec nice et renice

Dans cette leçon, tu vas apprendre à contrôler la priorité d'exécution des processus sous Linux. Quand ton système est sollicité par plusieurs tâches, savoir ajuster leur priorité te permet de garantir que les processus critiques obtiennent les ressources nécessaires.

---

## 1. Pourquoi ajuster la priorité ?

Linux attribue une **priorité** (nice value) à chaque processus. Plus la valeur est basse, plus le processus est "gentil" — il cède du temps CPU aux autres. Plus elle est haute, plus il est prioritaire.

Par défaut, la plupart des processus ont une nice value de **0**. Tu peux la faire varier de **-20** (très prioritaire) à **+19** (très conciliant).

**Cas d'usage courants :**
- Lancer une sauvegarde intensive en arrière-plan sans ralentir ton travail
- Donner plus de priorité à un serveur web qu'à une tâche de logs
- Empêcher un script lourd de monopoliser le CPU sur un serveur de production

---

## 2. La commande `nice`

`nice` permet de lancer un programme avec une priorité modifiée dès le départ.

### Syntaxe de base

```bash
nice -n <valeur> <commande>
```

| Nice value | Comportement |
|------------|-------------|
| `-20` | Processus très prioritaire (nécessite root) |
| `0` | Priorité par défaut |
| `+19` | Processus très "gentil", obtient le CPU en dernier |

### Exemples concrets

```bash
# Lancer une commande avec nice +10 (peu prioritaire)
nice -n 10 ./mon-script-lourd.sh

# Lancer une sauvegarde avec nice +15
nice -n 15 tar -czf /backup/home.tar.gz /home/

# Lancer un encodeur vidéo en arrière-plan, peu prioritaire
nice -n 19 ffmpeg -i video.mp4 sortie.mkv &

# Lancer un serveur avec haute priorité (root requis)
sudo nice -n -10 systemctl start mon-service
```

> **⚠️ Important :** Seules les valeurs positives (0 à +19) sont accessibles aux utilisateurs normaux. Les valeurs négatives (-1 à -20) nécessitent les droits root.

---

## 3. Modifier la priorité d'un processus en cours : `renice`

Parfois, tu veux changer la priorité d'un processus qui tourne déjà — sans l'arrêter. C'est là qu'intervient `renice`.

### Syntaxe

```bash
renice <niveau> -p <PID>
renice <niveau> -u <utilisateur>
renice <niveau> -g <groupe>
```

### Exemples concrets

```bash
# Voir la priorité actuelle d'un processus
ps -o pid,ni,comm | grep nom_du_processus

# Augmenter la nice value (moins prioritaire) d'un processus
renice +15 -p 1234

# Baisser la nice value (plus prioritaire) — root requis
sudo renice -10 -p 1234

# Modifier la priorité de TOUS les processus d'un utilisateur
renice +10 -u david

# Trouver le PID d'un processus
ps aux | grep compression
# Puis :
renice +5 -p <PID>
```

### Tableau récapitulatif des options

| Option | Description | Exemple |
|--------|-------------|---------|
| `-p <PID>` | Cible un processus par son PID | `renice +10 -p 5678` |
| `-u <utilisateur>` | Cible tous les processus d'un utilisateur | `renice +5 -u www-data` |
| `-g <groupe>` | Cible tous les processus d'un groupe | `renice +5 -g developers` |

---

## 4. Visualiser les priorités en temps réel

### Avec `top`

```bash
top
```

Dans la sortie de `top`, la colonne **NI** affiche la nice value de chaque processus. Tu peux also changer la priorité directement dans `top` :

1. Lance `top`
2. Tape `r`
3. Entre le PID du processus
4. Entre la nouvelle nice value
5. Tape Entrée

### Avec `htop`

```bash
htop
```

`htop` est plus visuel. La nice value est affichée et tu peux la modifier avec la touche **r** (renice).

### Avec `ps`

```bash
# Lister processus avec nice value
ps -eo pid,ni,ppid,cmd --sort=ni

# Processus les plus "gentils" (+19)
ps -eo pid,ni,cmd --sort=-ni | head -10

# Processus les plus prioritaires (-20 à 0)
ps -eo pid,ni,cmd --sort=ni | head -10
```

---

## 5. Utilisation avancée

### Lancer un service systemd avec une nice value spécifique

Édite le fichier service ou utilise override :

```bash
sudo systemctl edit mon-service
```

Puis ajoute :

```ini
[Service]
Nice=10
```

### Combiner nice avec nohup (processus robuste)

```bash
# Lancer un script lourd, même si on se déconnecte
nohup nice -n 15 ./backup-quotidien.sh > /var/log/backup.log 2>&1 &
```

### Vérifier l'impact avec `time`

```bash
# Mesurer le temps d'exécution avec une priorité modifiée
time nice -n 10 ./mon-script.sh
```

---

## 6. Exercices pratiques

### Exercice 1 : Lancer un processus peu prioritaire

1. Ouvre deux terminaux
2. Dans le premier, lance une boucle infinie qui utilise le CPU :
   ```bash
   yes > /dev/null &
   ```
3. Observe l'utilisation CPU avec `top`
4. Dans le second terminal, lance la même commande avec `nice -n 19` :
   ```bash
   nice -n 19 yes > /dev/null &
   ```
5. Observe la différence de priorité dans `top` (colonne NI)

### Exercice 2 : Modifier la priorité d'un processus en cours

1. Lance un processus consommateur :
   ```bash
   python3 -c "while True: pass" &
   ```
2. Note son PID
3. Modifie sa nice value :
   ```bash
   renice +15 -p <PID>
   ```
4. Vérifie le changement avec `ps -o pid,ni,cmd | grep python3`

### Exercice 3 : Protéger un processus critique

1. Lance un "serveur simulés" avec une priorité élevée :
   ```bash
   sudo nice -n -5 ./script-critique.sh
   ```
2. Lance simultanément un script lourd avec une priorité basse
3. Observe comment le script critique garde le contrôle du CPU

---

## 7. Récapitulatif

| Commande | Rôle |
|----------|------|
| `nice -n <val> <cmd>` | Lancer une commande avec une priorité donnée |
| `renice <val> -p <PID>` | Modifier la priorité d'un processus en cours |
| `renice <val> -u <user>` | Modifier la priorité de tous les processus d'un utilisateur |
| `ps -o pid,ni,cmd` | Afficher les processus avec leur nice value |
| `top` / `htop` | Visualiser et modifier les priorités en interactif |

**Astuce finale :** En règle générale, utilise des nice values positives pour les tâches de fond non critiques. Garde les valeurs négatives pour les processus système essentiels ou les services qui ne doivent jamais être ralentis.

---

*Dans la prochaine leçon, nous aborderons un autre sujet fondamental pour maîtriser Linux.*
