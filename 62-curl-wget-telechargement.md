# Leçon 62 : curl et wget — Télécharger depuis le terminal

Deux outils pour télécharger des fichiers et interagir avec des API web. `curl` est le plus polyvalent, `wget` excelle pour le téléchargement récursif.

## 1. wget — Télécharger simplement

```bash
# Télécharger un fichier
wget https://example.com/fichier.zip

# Avec un nom différent
wget -O mon_fichier.zip https://example.com/fichier.zip

# Reprendre un téléchargement interrompu
wget -c https://example.com/gros_fichier.iso

# Télécharger en arrière-plan
wget -b https://example.com/fichier.zip
# Logs dans wget.log

# Télécharger tout un site (miroir)
wget -r -l 2 -p https://example.com/docs/
# -r : récursif, -l 2 : profondeur max 2, -p : ressources nécessaires

# Limiter la vitesse (500 Ko/s)
wget --limit-rate=500k https://example.com/gros.iso
```

## 2. curl — L'outil universel

```bash
# Télécharger un fichier (avec son nom d'origine)
curl -O https://example.com/fichier.zip

# Avec un nom personnalisé
curl -o local.zip https://example.com/fichier.zip

# Suivre les redirections
curl -L https://bit.ly/some-short-link

# Voir les en-têtes HTTP
curl -I https://example.com

# Mode silencieux + barre de progression
curl -sS -O https://example.com/fichier.zip

# Télécharger plusieurs fichiers
curl -O https://example.com/fichier1.zip -O https://example.com/fichier2.zip
```

## 3. curl + API REST

```bash
# Requête GET (défaut)
curl https://api.github.com/users/torvalds

# Requête POST avec JSON
curl -X POST https://api.example.com/data \
  -H "Content-Type: application/json" \
  -d '{"nom":"test","valeur":42}'

# Avec authentification
curl -u username:password https://api.example.com/private

# Token Bearer
curl -H "Authorization: Bearer ton_token" https://api.example.com/data

# Sauvegarder les en-têtes de réponse
curl -D headers.txt https://example.com
```

## 4. curl pour debugger

```bash
# Voir toute la transaction HTTP (très utile !)
curl -v https://example.com

# Mesurer le temps de réponse
curl -w "\nTemps total: %{time_total}s\n" -o /dev/null -s https://example.com

# Tester différents verbes HTTP
curl -X PUT https://example.com/resource/1
curl -X DELETE https://example.com/resource/1
```

## 5. curl vs wget

| Fonctionnalité | curl | wget |
|---------------|------|------|
| Téléchargement simple | ✅ | ✅ |
| API REST (POST, JSON, auth) | ✅ | ❌ |
| Téléchargement récursif | ❌ | ✅ |
| Reprise de téléchargement | -C - | -c |
| Par défaut sur toutes les distros | ✅ | Pas toujours |

## 6. Exercices pratiques

1. **wget** — Télécharge une page web avec `wget` et vérifie le fichier créé
2. **curl** — Télécharge le même fichier avec `curl -O`
3. **API** — Teste `curl https://api.github.com/users/torvalds` et observe le JSON
4. **Debug** — Utilise `curl -I` pour voir les en-têtes HTTP d'un site
