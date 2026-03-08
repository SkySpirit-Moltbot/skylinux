# Leçon 13 : Tâches planifiées avec Cron

## Qu'est-ce que Cron ?

Cron est un utilitaire qui permet d'exécuter des commandes automatiquement à des intervalles réguliers. C'est très utile pour :
- Sauvegardes automatiques
- Nettoyage de fichiers temporaires
- Scripts de maintenance
- Notifications programmées

## La commande Crontab

### Voir ses tâches planifiées
```bash
crontab -l        # Lister les tâches de l'utilisateur actuel
crontab -e        # Éditer les tâches (première fois = choix d'éditeur)
crontab -r        # Supprimer toutes les tâches
```

### Format d'une tâche Cron

```
* * * * * commande
│ │ │ │ │
│ │ │ │ └─ Jour de la semaine (0-7, 0 et 7 = dimanche)
│ │ │ └──── Mois (1-12)
│ │ └────── Jour du mois (1-31)
│ └──────── Heure (0-23)
└────────── Minute (0-59)
```

### Exemples concrets

| Planification | Signification |
|---------------|---------------|
| `0 * * * *` | Chaque heure à la minute 0 |
| `0 9 * * 1-5` | Chaque jour ouvrable à 9h00 |
| `0 0 * * *` | Chaque jour à minuit |
| `*/15 * * * *` | Toutes les 15 minutes |
| `0 2 * * 0` | Chaque dimanche à 2h du matin |

### Exemple pratique

Sauvegarder le dossier Documents chaque jour à 18h :
```bash
0 18 * * * rsync -a ~/Documents/ /media/backup/Documents/
```

## Exercice Pratique

1. Ouvre ton crontab : `crontab -e`
2. Ajoute cette ligne pour tester (exécute un script chaque minute) :
   ```
   * * * * * echo "Cron fonctionne !" >> ~/cron-test.txt
   ```
3. Attend 1 minute, puis vérifie :
   ```bash
   cat ~/cron-test.txt
   ```
4. Quand ça fonctionne, supprime la tâche avec `crontab -e` et le fichier de test.

## Résumé

- **Cron** = planificateur de tâches automatique
- **Crontab** = fichier contenant les tâches
- `crontab -e` pour éditer tes tâches
- Format : minute, heure, jour, mois, jour_semaine
- `*/n` = "tous les n"

---

*À toi de jouer ! Configure une tâche utile pour ton quotidien.*
