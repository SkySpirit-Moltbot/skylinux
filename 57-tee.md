# Leçon 57 : tee — Lire depuis l'entrée et écrire partout

`tee` lit l'entrée standard et la copie à la fois vers la sortie standard ET vers un ou plusieurs fichiers. Pense à un "T" de plomberie qui divise le flux.

## 1. Le principe

```bash
commande | tee fichier.txt
# → le résultat s'affiche à l'écran ET s'écrit dans le fichier
```

## 2. Utilisation de base

```bash
# Voir ET sauvegarder la sortie d'une commande
ls -la | tee liste_fichiers.txt

# Ajouter à la fin d'un fichier existant (-a = append)
echo "Nouvelle entrée" | tee -a journal.log

# Écrire dans plusieurs fichiers à la fois
dmesg | tee log1.txt log2.txt log3.txt
```

## 3. Cas pratiques

```bash
# Logger une commande interactive (compilation, script long)
./configure 2>&1 | tee build.log
make 2>&1 | tee -a build.log

# Debug : voir ce qui passe dans un pipe
cat fichier.csv | grep -i erreur | tee /tmp/erreurs.txt | wc -l
# → affiche le nombre ET sauvegarde les erreurs dans /tmp

# Enregistrer une session de terminal
script -c "bash" session.log
# Alternative à tee pour capturer TOUTE la session
```

## 4. tee + sudo pour écrire dans des fichiers protégés

```bash
# ❌ Ne marche pas : la redirection est faite par le shell utilisateur
echo "options" > /etc/modprobe.d/options.conf

# ✅ tee avec sudo fait l'écriture en root
echo "options" | sudo tee /etc/modprobe.d/options.conf

# Sans afficher le résultat à l'écran
echo "options" | sudo tee /etc/modprobe.d/options.conf > /dev/null
```

## 5. Exercices pratiques

1. **Journal** — Lance `dmesg` et enregistre la sortie dans un fichier tout en la voyant défiler
2. **Sudo** — Ajoute une ligne dans `/etc/hosts` avec `echo ... | sudo tee -a`
3. **Multi** — Écris la date du jour dans 3 fichiers différents avec un seul tee
