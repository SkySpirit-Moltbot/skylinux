# Leçon 45 : Planification de tâches avec at et batch

Dans cette leçon, tu vas apprendre à planifier des **tâches ponctuelles** avec `at` et `batch`. Contrairement à cron qui répète des tâches, `at` exécute une commande **une seule fois** à un moment précis. `batch` attend que la charge du système soit assez basse pour lancer ta tâche.

---

## 1. Préparer le terrain

### Installer at

```bash
sudo apt update
sudo apt install at -y
```

### Démarrer le service

```bash
sudo systemctl enable atd
sudo systemctl start atd
```

### Vérifier que ça fonctionne

```bash
at -V
# at version 3.2.4
```

---

## 2. La commande `at`

`at` planifie une commande pour qu'elle s'exécute **une seule fois**, à l'heure que tu indiques.

### Syntaxe de base

```bash
at <heure> [jour mois [année]]
```

### Formats d'heure courants

| Format | Exemple | Signification |
|--------|---------|---------------|
| `HH:MM` | `14:30` | Aujourd'hui à 14h30 (ou demain si passé) |
| `now + N minutes` | `now + 5 minutes` | Dans 5 minutes |
| `now + N hours` | `now + 2 hours` | Dans 2 heures |
| `now + N days` | `now + 3 days` | Dans 3 jours |
| `tomorrow` | `tomorrow 10am` | Demain à 10h |
| `noon` | `noon` | Aujourd'hui à midi |
| `midnight` | `midnight` | Aujourd'hui à minuit |
| `teatime` | `teatime 4pm` | Aujourd'hui à 16h (heure du thé) |
| `JJ.MM.AAAA` | `25.12.2026 09:00` | 25 décembre 2026 à 9h |
| `Mois JJ année` | `jan 15 2027 14:00` | 15 janvier 2027 à 14h |

---

## 3. Utiliser `at` pas à pas

### Exemple 1 : Exécution dans 2 minutes

```bash
at now + 2 minutes
```
Tu verras un prompt `at>` — tape ta commande puis `Ctrl+D` :

```
at> echo "La tâche a exécuté $(date)" >> ~/test_at.log
at> <EOT>
job 1 at Mon Apr  6 08:15:00 2026
```

### Exemple 2 : À une heure précise

```bash
at 17:30
```
```
at> echo "C'est l'heure !" | tee ~/alerte_17h30.txt
at> <EOT>
job 2 at Mon Apr  6 17:30:00 2026
```

### Exemple 3 : Demain à 9h

```bash
at 9am tomorrow
```
```
at> /home/utilisateur/scripts/backup_rapide.sh
at> <EOT>
job 3 at Tue Apr  7 09:00:00 2026
```

### Exemple 4 : Avec un script complet

```bash
at 20:00 <<EOF
tar -czf /backup/home_$(date +%Y%m%d).tar.gz /home/utilisateur/
echo "Sauvegarde terminée" | mail -s "Backup" utilisateur@email.com
EOF
```

---

## 4. Syntaxe alternative par tube

Planifier sans entrer dans le mode interactif :

```bash
# Avec un tube (pipe)
echo "/home/utilisateur/scripts/rapport.sh" | at 10am tomorrow

# Avec un here-doc via fichier
cat << 'CMDS' | at now + 1 hour
mkdir -p ~/archives/$(date +%Y%m%d)
cp ~/Documents/*.pdf ~/archives/$(date +%Y%m%d)/
CMDS
```

---

## 5. `batch` — exécution quand le système est calme

`batch` lance ta commande quand la **charge moyenne** du système descend sous 1.5 (par défaut). C'est idéal pour les tâches lourdes qu'on veut faire tourner aux heures creuses.

```bash
batch
```
```
at> tar -czf /backup/plein_backup.tar.gz /home/
at> <EOT>
job 5 at Mon Apr  6 08:20:00 2026
```

La任务 s'exécutera dès que la charge le permet.

### Changer le seuil de charge

```bash
# Lancer quand la charge est sous 0.8
echo "script_lourd.sh" | at -q b -b 0.8
```

### Files de priorité (queues)

`at` utilise des files (queues) обозначенные par une lettre :

| Queue | Nice value | Usage |
|-------|------------|-------|
| `a` à `z` | -20 à +19 | File `a` = très prioritaire, `z` = très patient |

```bash
# Queue b (normal)
at -q b 10pm tomorrow

# Queue c (patient)
at -q c 2am
```

---

## 6. Gérer les tâches planifiées

### Lister les tâches en attente

```bash
atq
# 3   Mon Apr  7 09:00:00 2026 a utilisateur
# 5   Mon Apr  6 08:20:00 2026 a root
```

La premièr colonne est le **numéro de job**.

### Supprimer une tâche

```bash
# Par numéro de job
atrm 3

# Supprimer plusieurs
atrm 2 5
```

### Alternative avec `atq` + `atrm`

```bash
# Supprimer le job 7
atrm 7
```

---

## 7. La commande `at` avec les permissions

### Qui peut utiliser `at` ?

Par défaut, tout le monde. Pour的限制er :

```bash
# Lister les fichiers de contrôle
ls /etc/at*

# Autoriser un utilisateur
sudo echo "utilisateur" > /etc/at.allow

# Interdire un utilisateur
sudo echo "utilisateur" >> /etc/at.deny
```

---

## 8. Différences entre `at` et `cron`

| Critère | `at` | `cron` |
|---------|------|--------|
| Fréquence | Une seule fois | Récurrente |
| Persistance | Job supprimé après exécution | Reste configuré |
| Charge système | `batch` peut en tenir compte | Non |
| Cas d'usage | Tâche unique programmée | Automatisation récurrente |
| Dépendances | Non (utilise `at` + `sleep` pour temporiser) | Oui avec `anacron` ou scripts |

---

## 9. Exercice pratique

### Exercice : Planifier une sauvegarde unique

**Objectif :** Créer une sauvegarde de ton répertoire `~/Documents` à exécuter dans 5 minutes.

```bash
# 1. Vérifie que at est installé et le service actif
sudo systemctl status atd

# 2. Planifie la tâche
at now + 5 minutes
```

Dans le prompt `at>`, tape :
```
mkdir -p ~/backup_unique
tar -czf ~/backup_unique/docs_backup_$(date +%H%M).tar.gz ~/Documents/
echo "Sauvegarde terminée le $(date)" > ~/backup_unique/rapport.txt
```

Puis `Ctrl+D` pour valider.

```bash
# 3. Vérifie que le job est dans la queue
atq

# 4. Après quelques minutes, vérifie que ça a fonctionné
ls ~/backup_unique/
cat ~/backup_unique/rapport.txt
```

**Bonus :** Supprime le job avec `atrm <numéro>` AVANT qu'il ne s'exécute, puis reprogramme-le pour demain à 8h avec `at 8am tomorrow`.

---

## 10. Récapitulatif

| Commande | Description |
|----------|-------------|
| `at <heure>` | Planifier une tâche pour un moment précis |
| `at now + N minutes` | Exécuter dans N minutes |
| `at tomorrow HH:MM` | Exécuter demain à l'heure indiquée |
| `batch` | Exécuter quand la charge système est basse |
| `atq` | Lister les jobs en attente |
| `atrm <job>` | Supprimer un job |
| `Ctrl+D` | Valider et quitter le mode interactif |

`at` est parfait pour les tâches uniques : un redémarrage différé, un script qui ne doit tourner qu'une fois, ou une action à faire hors des heures de bureau. `batch` complète le tableau en s'adaptant à la charge réelle de ta machine. ⏰
