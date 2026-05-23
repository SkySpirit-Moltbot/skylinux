# Leçon 59 : Leçon 70 : nohup — Exécuter des commandes persistantes

### 1. Le problème : les signaux et la déconnexion

Sous Linux, quand un terminal se ferme, il envoie un signal SIGHUP (Signal Hang UP) à tous les processus enfants. Ce signal cause normalement l'arrêt du processus. C'est un mécanisme historiqueherited du temps où les terminaux étaient des machines physiques.

### 2. La solution : nohup

nohup protège un processus contre le signal SIGHUP. Le processus continuera à tourner même si le terminal est fermé.

### 3. Où va la sortie ?

Par défaut, nohup redirige la sortie standard vers nohup.out. Vous pouvez changer ce comportement :

### 5. nohup vs disown vs screen

Il existe plusieurs ways de détacher un processus :

### Résumé

nohup commande & — Lance une commande immune au signal SIGHUP

Par défaut, la sortie va dans nohup.out

Redirigez la sortie vers un fichier ou /dev/null selon vos besoins

Vérifiez avec ps aux | grep que le processus tourne toujours

Pour un contrôle plus avancé, utilisez screen ou tmux (voir leçons 27 et 41)

