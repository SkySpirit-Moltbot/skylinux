# Leçon 35 : Optimisation du démarrage avec systemd-analyze

Dans cette leçon, tu vas découvrir comment analyser et optimiser le temps de démarrage de ton système Linux grâce à systemd-analyze. Un démarrage lent peut cacher des services inutiles ou des configurations problématiques.

---

## 1. Qu'est-ce que systemd-analyze ?

systemd-analyze est un outil fourni avec systemd qui permet de mesurer et diagnostiquer le temps nécessaire au démarrage du système. Il montre exactement combien de temps chaque étape prend, du firmware BIOS/UEFI jusqu'à l'écran de connexion.

Ce qu'on peut analyser :
- Temps total du démarrage
- Durée du firmware (BIOS/UEFI)
- Durée du chargeur d'amorçage (GRUB)
- Durée du-userspace (services systemd)
- Durée du gestionnaire de connexion (GDM, LightDM...)

---

## 2. Analyse basique du démarrage

### Voir le temps total

```bash
systemd-analyze
```

Exemple de sortie :

Lecture :
- kernel → Temps de chargement du noyau Linux
- userspace → Temps nécessaire pour démarrer tous les services
- graphical.target → Moment où l'interface graphique apparaît

### Voir le détail par service

```bash
systemd-analyze blame
```

Cette commande liste tous les services dans l'ordre décroissant de leur temps de démarrage :

Les services en haut de la liste sont les plus longs — c'est là qu'il faut chercher des optimisations.

---

## 3. Visualisation graphique

### Générer un SVG du démarrage

```bash
systemd-analyze plot > demarrage.svg
```

Puis ouvre le fichier avec un navigateur :

```bash
xdg-open demarrage.svg
```

Tu obtiens une timeline visuelle montrant chaque service sur une barre temporelle. C'est idéal pour identifier en un coup d'œil où le temps est perdu.

### Voir les services critiques

```bash
systemd-analyze critical-chain
```

Affiche la chaîne critique — le chemin le plus long de services dépendants qui détermine la durée totale du démarrage :

---

## 4. Optimiser le démarrage

### Identifier et désactiver les services inutiles

Si un service inconnu prend beaucoup de temps, vérifie son utilité :

```bash
# Voir la description d'un service
systemctl status mon-service.service
```

Pour désactiver un service inutile (exemple avec bluetooth si tu n'en as pas besoin) :

```bash
# Désactiver un service au démarrage
sudo systemctl disable bluetooth.service

# Masquer complètement (ne peut plus être démarré)
sudo systemctl mask bluetooth.service
```

### Réduire le timeout de GRUB

```bash
# Éditer la config GRUB
sudo nano /etc/default/grub
```

Modifie ces lignes :

Puis applique :

```bash
sudo update-grub
```

### Activer les services en parallèle

Systemd parallélise automatiquement les services, mais tu peux vérifier qu'un service n'attend pas inutilement :

```bash
# Voir pourquoi un service tarde
systemctl show nginx.service | grep After
```

---

## 5. systemd-analyze verify

Vérifie la validité de tes fichiers d'unités systemd :

```bash
systemd-analyze verify /chemin/vers/mon-service.service
```

Cela détecte les erreurs de syntaxe ou les options inconnues.

---

## 6. Autres commandes utiles
| Commande | Description |
| --- | --- |
| systemd-analyze time | Affiche les temps de démarrage |
| systemd-analyze blame | Liste les services par temps |
| systemd-analyze plot | Génère un SVG de la timeline |
| systemd-analyze critical-chain | Affiche la chaîne critique |
| systemd-analyze dot | Génère un graphe des dépendances |
| systemd-analyze dump | Affiche l'état complet des services |

---

## Exercice pratique

Objectif : Analyse ton propre système et identifie une optimisation possible.

Étapes :
1. Ouvre un terminal et exécute systemd-analyze pour voir ton temps de démarrage total.
2. Exécute systemd-analyze blame pour identifier les 5 services les plus lents.
3. Génère un SVG avec systemd-analyze plot > ~/demarrage.svg et ouvre-le.
4. Choisis un service non essentiel et désactive-le avec sudo systemctl disable nom.service.
5. Redémarre et compare le temps avec systemd-analyze.

---

## Résumé
- systemd-analyze mesure le temps de démarrage du système
- systemd-analyze blame liste les services par durée décroissante
- systemd-analyze plot génère une visualisation SVG de la timeline
- systemd-analyze critical-chain montre la chaîne critique des dépendances
- Désactiver les services inutiles accélère le démarrage
- Réduire le timeout GRUB élimine un délai fixe au démarrage
- Toujours vérifier la description d'un service avant de le désactiver
