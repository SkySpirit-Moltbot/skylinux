# Leçon 46 : Signaux, erreurs et gestion d'interruption dans les scripts Bash

Dans cette leçon, tu vas apprendre à rendre tes scripts Bash robustes : intercepter les signaux (Ctrl+C), gérer les erreurs, quitter proprement et nettoyer les fichiers temporaires. Quand un script est interrompu ou échoue, c'est souvent parce qu'il n'a pas été conçu pour gérer ces situations.

---

## 1. Qu'est-ce qu'un signal ?

Un **signal** est un message envoyé par le système ou par un utilisateur à un processus en cours d'exécution. C'est une forme de communication entre processus — et entre toi et tes scripts.

### Les signaux les plus courants

| Signal | Numéro | Signification | Action par défaut |
|--------|--------|---------------|-------------------|
| `SIGINT` (Ctrl+C) | 2 | Interruption par l'utilisateur | Termine le processus |
| `SIGTERM` | 15 | Demande d'arrêt propre | Termine le processus |
| `SIGKILL` | 9 | Arrêt forcé | Termine immédiatement (impossible à intercepter) |
| `SIGHUP` | 1 | Le terminal a été fermé | Le processus se termine ou se reconfigure |
| `SIGEXIT` | 0 | Sortie normale du script | — |

Quand tu tapes `Ctrl+C` dans un terminal, tu envoies un `SIGINT` au processus en avant-plan. Par défaut, cela termine le programme. Mais avec `trap`, tu peux décider ce qui se passe à la place.

---

## 2. La commande `trap` — intercepter les signaux

`trap` te permet d'exécuter une commande (ou une fonction) quand un signal précis est reçu. C'est indispensable pour nettoyer proprement.

### Syntaxe de base

```bash
trap 'commande' SIGNAL
trap 'fonction' SIGNAL1 SIGNAL2
```

### Exemple fondamental : nettoyer à la sortie

```bash
#!/bin/bash

# Fonction de nettoyage
nettoyer() {
    echo "Nettoyage en cours..."
    rm -f /tmp/mon-script.lock
    rm -f /tmp/mon-script.tmp
    echo "Programme terminé proprement."
}

# Intercepter Ctrl+C (SIGINT) et sortie normale (EXIT)
trap nettoyer EXIT INT TERM

echo "Mon script tourne... (Ctrl+C pour arrêter)"
sleep 30
```

**Ce qui se passe :**
- Le script démarre et enregistre la fonction `nettoyer`
- Quand tu fais `Ctrl+C` → `SIGINT` → `nettoyer` s'exécute → le lockfile est supprimé
- Quand le script finit normalement → `EXIT` → `nettoyer` s'exécute aussi

> **💡 Bonnes pratiques :** Utilise toujours `trap` pour supprimer les fichiers temporaires et libérer les ressources (locks, sockets, connexions).

---

## 3. Gérer les erreurs avec `set -e` et `set -u`

### Quitter dès qu'une commande échoue : `set -e`

Par défaut, Bash continue l'exécution même si une commande échoue. `set -e` change ce comportement.

```bash
#!/bin/bash
set -e  # Quitte immédiatement si une commande échoue

echo "Création du dossier..."
mkdir /tmp/mon-projet
cd /tmp/mon-projet
echo "Projet créé."
```

Si `mkdir` échoue (droits insuffisants, disque plein), le script s'arrête là.

### Quitter sur variable non définie : `set -u`

```bash
#!/bin/bash
set -u

echo "Salutation pour $NOM"  # Si $NOM n'existe pas → erreur
```

Sans `set -u`, Bash remplace `$NOM` par une chaîne vide sans protester. Avec `set -u`, le script s'arrête.

### Combinaison recommandée

```bash
#!/bin/bash
set -euo pipefail
```

| Option | Rôle |
|--------|------|
| `-e` | Quitte sur erreur |
| `-u` | Quitte sur variable non définie |
| `-o pipefail` | Quitte si une commande dans un pipe échoue (pas seulement la dernière) |

---

## 4. Vérifier les codes de retour

Chaque commande retourne un **code de sortie** : `0` = succès, `!= 0` = erreur.

```bash
# Lancer une commande et tester son résultat
mkdir /backup || { echo "Échec de la création du dossier"; exit 1; }

# Ou avec if
if grep -q "error" /var/log/syslog; then
    echo "Des erreurs ont été trouvées !"
fi

# Capturer le code de sortie dans une variable
ls /etc/passwd
resultat=$?
echo "Code de sortie de ls : $resultat"  # 0 si succès
```

---

## 5. Exemple complet : script robuste de sauvegarde

```bash
#!/bin/bash
#
# sauvegarde-robuste.sh — Exemple de script avec gestion de signaux et d'erreurs
#

set -euo pipefail

# Répertoires
SOURCE="/home/david/documents"
DEST="/tmp/backup-$(date +%Y%m%d).tar.gz"
LOCKFILE="/tmp/sauvegarde.lock"

# Fonction de nettoyage
cleanup() {
    local exit_code=$?
    rm -f "$LOCKFILE"
    if [ $exit_code -ne 0 ]; then
        echo "Sauvegarde échouée (code: $exit_code)" >&2
    fi
    exit $exit_code
}

# Intercepter les signaux
trap cleanup EXIT INT TERM

# Vérifier qu'une seule instance tourne
if [ -f "$LOCKFILE" ]; then
    echo "Une sauvegarde est déjà en cours. Quittez l'autre instance."
    exit 1
fi

# Créer le lockfile
echo $$ > "$LOCKFILE"

# Corps du script
echo "Sauvegarde de $SOURCE vers $DEST..."
tar -czf "$DEST" "$SOURCE" && echo "Sauvegarde terminée : $DEST"

# Supprimer le lockfile avant de quitter (cleanup le fait, mais explicite)
rm -f "$LOCKFILE"
```

**Points clés de ce script :**
- `set -euo pipefail` → arrêt sur erreur, variable manquante ou pipe cassé
- `trap cleanup EXIT INT TERM` → nettoyage systématique (lock + message)
- Lockfile → empêche deux sauvegardes simultanées
- Code de sortie explicite avec `local exit_code=$?`

---

## 6. Les signaux dans la pratique

### Envoyer un signal manuellement

```bash
# Voir les signaux disponibles
kill -l

# Envoyer SIGTERM à un processus (demande polie)
kill -15 1234

# Envoyer SIGKILL (forcé)
kill -9 1234

# Envoyer un signal à tous les processus d'un nom
pkill -f "mon-script.sh"
```

### Tester un signal dans un script

```bash
#!/bin/bash
trap 'echo "Signal reçu !"' INT

echo "En attente... (Ctrl+C pour tester)"
while true; do
    sleep 1
done
```

---

## 7. Récapitulatif des options de `set`

| Option | Description |
|--------|-------------|
| `set -e` | Quitte si une commande échoue |
| `set -u` | Quitte si une variable est indéfinie |
| `set -o pipefail` | Quitte si une commande dans un pipe échoue |
| `set -x` | Affiche chaque commande avant de l'exécuter (debug) |
| `set -n` | Lit le script sans exécuter (syntax check only) |

Pour le debug, tu peux aussi utiliser `bash -x mon-script.sh`.

---

## 8. Exercice pratique

**Objectif :** Créer un script `monitoring.sh` qui surveille l'espace disque et qui :
1. Quitte proprement sur Ctrl+C (affiche un message d'au revoir)
2. Supprime son fichier lock à la sortie
3. Utilise `set -euo pipefail`
4. Vérifie l'espace disque et affiche une alerte si > 80%

```bash
#!/bin/bash
# Objectif : créer ce script

# 1. Ajouter set -euo pipefail
# 2. Créer un lockfile /tmp/monitoring.lock
# 3. Écrire une fonction cleanup() qui supprime le lock
# 4. Intercepter EXIT, INT, TERM
# 5. Vérifier l'espace disque : df / | grep -v Filesystem | awk '{print $5}' | tr -d '%'
# 6. Si > 80%, afficher "Alerte : espace disque faible !"
# 7. Boucle infinie avec sleep 10
```

**Solution indicative :**

```bash
#!/bin/bash
set -euo pipefail

LOCKFILE="/tmp/monitoring.lock"

cleanup() {
    rm -f "$LOCKFILE"
    echo "Script arrêté. Au revoir !"
}
trap cleanup EXIT INT TERM

if [ -f "$LOCKFILE" ]; then
    echo "Le script tourne déjà."
    exit 1
fi
echo $$ > "$LOCKFILE"

echo " Surveillance disque... (Ctrl+C pour arrêter)"
while true; do
    usage=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
    if [ "$usage" -gt 80 ]; then
        echo " Alerte : espace disque à ${usage}% !"
    fi
    sleep 10
done
```

---

## Résumé

| Concept | Commande / Outil | À retenir |
|---------|-----------------|-----------|
| Intercepter les signaux | `trap 'fonction' SIG` | Nettoyer les ressources à la sortie |
| Quitter sur erreur | `set -e` | Utile pour les scripts critiques |
| Quitter sur variable manquante | `set -u` | Évite les bugs silencieux |
| Pipe échecs | `set -o pipefail` | Détecte les erreurs dans les pipes |
| Code de sortie | `$?` | 0 = succès, != 0 = erreur |
| Debug | `bash -x script.sh` | Affiche chaque commande |

Un script qui gère ses signaux et ses erreurs, c'est un script **professionnel**. Même si ton serveur coupe, ton script aura le temps de nettoyer ses fichiers temporaires et de préserver ses données.
