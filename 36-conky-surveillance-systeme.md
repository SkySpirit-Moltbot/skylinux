# Conky — Surveillance Système sur le Bureau

## Qu'est-ce que Conky ?

**Conky** est un outil de surveillance système léger et ultra-configurable qui affiche des informations en temps réel directement sur le bureau. Contrairement aux widgets lourds, Conky tourne avec un impact minimal sur les ressources.

**Utilisations courantes :**
- CPU, RAM, Swap utilisés
- Espace disque
- Températures (CPU, GPU, disques)
- Réseau (débit upload/download)
- Batterie (sur portable)
- Processus les plus gourmands
- Date, heure, météo
- et bien plus encore...

---

## 1. Installation

```bash
# Debian / Ubuntu / Linux Mint
sudo apt install conky

# Vérifier la version
conky --version
```

---

## 2. Lancement et Arrêt Rapide

```bash
# Lancer Conky (premier lancement)
conky

# Lancer avec un fichier de config précis
conky -c ~/.config/conky/ma-config.conf

# Arrêter tous les Conky
killall conky
```

Par défaut, Conky utilise le fichier `~/.conkyrc` (ou `/etc/conky/conky.conf`).

---

## 3. Structure d'un Fichier de Config

Un fichier Conky a **deux sections** principales :

```
# ======== SECTION 1 : PARAMÈTRES GÉNÉRAUX ========
# Position, taille, transparence, couleurs...

# ======== SECTION 2 : CONTENU (TEXT/GRAPHICS) ========
# Ce qui s'affiche à l'écran
```

**Exemple minimaliste complet :**

```bash
conky.config = {
    update_interval = 1,
    double_buffer = true,
    no_buffers = true,
    use_xft = true,
    font = 'DejaVu Sans:size=10',
    alignment = 'top_right',
    gap_x = 10,
    gap_y = 10,
    own_window = true,
    own_window_class = 'Conky',
    own_window_argb_visual = true,
    own_window_argb_value = 150,
    own_window_type = 'desktop',
   own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',
};

conky.text = [[
${color grey}Hostname:${color} $nodename
${color grey}Kernel:${color} $kernel
${color grey}Uptime:${color} $uptime
${color grey}CPU:${color} $cpu%
${color grey}RAM:${color} $mem / $memmax
${color grey}Swap:${color} $swap / $swapmax
${color grey}Disk (root):${color} $fs_used / $fs_size
${color grey}Download:${color} $downspeed
${color grey}Upload:${color} $upspeed
]]
```

---

## 4. Les Paramètres Essentiels

### Position et Apparence

| Paramètre | Rôle | Exemple |
|---|---|---|
| `alignment` | Position sur l'écran | `top_right`, `bottom_left`, `middle_middle` |
| `gap_x / gap_y` | Marge depuis le bord | `gap_x = 10`, `gap_y = 50` |
| `own_window = true` | Fenêtre propre (pas un vrai cadre) | — |
| `own_window_argb_visual = true` | Transparence ARGB | — |
| `own_window_argb_value` | Niveau de transparence (0-255) | `150` = semi-transparent |
| `own_window_type` | Type de fenêtre | `desktop`, `dock`, `normal` |
| `double_buffer = true` | Évite le clignotement (important !) | — |
| `use_xft = true` | Police anti-aliasée | — |
| `font` | Police par défaut | `'DejaVu Sans:size=10'` |
| `update_interval` | Rafraîchissement (secondes) | `1` = chaque seconde |

### Couleurs Prédéfinies

```
${color grey}    → gris
${color red}     → rouge
${color green}   → vert
${color blue}    → bleu
${color yellow}  → jaune
${color cyan}    → cyan
${color orange}  → orange
${color white}   → blanc
```

Définir une couleur personnalisée :
```
${color #FF6600}
```

---

## 5. Variables Systèmes (les Plus Utilisées)

### Système

| Variable | Description |
|---|---|
| `$nodename` | Nom de la machine |
| `$kernel` | Version du noyau |
| `$uptime` | Temps depuis le dernier démarrage |
| `$uptime_short` | Uptime condensé (plus court) |
| `$time` | Heure locale |
| `$utc_time` | Heure UTC |
| `$date` | Date courante |

### CPU

| Variable | Description |
|---|---|
| `$cpu` | Utilisation CPU totale (%) |
| `$cpu cpu0` | Utilisation cœur 0 |
| `$cpubar` | Bargraphique CPU |
| `$freq` | Fréquence CPU actuelle (GHz) |
| `$freq_g` | Fréquence CPU en GHz |

### Mémoire

| Variable | Description |
|---|---|
| `$mem` | RAM utilisée |
| `$memmax` | RAM totale |
| `$memperc` | Pourcentage RAM utilisée |
| `$membar` | Bargraphique RAM |
| `$swap` | Swap utilisée |
| `$swapmax` | Swap totale |
| `$swapperc` | Pourcentage Swap |

### Disques

| Variable | Description |
|---|---|
| `$fs_used / $fs_size` | Espace utilisé / total d'un point de montage |
| `$fs_used_perc` | Pourcentage utilisé |
| `$fs_bar` | Bargraphique |
| `$diskio_read` | Débit lecture disque |
| `$diskio_write` | Débit écriture disque |

### Réseau

| Variable | Description |
|---|---|
| `$upspeed` | Vitesse upload actuelle |
| `$upspeedf` | Vitesse upload (flottant) |
| `$downspeed` | Vitesse download actuelle |
| `$downspeedf` | Vitesse download (flottant) |
| `$totaldown` | Total téléchargé |
| `$totalup` | Total uploadé |
| `$net` | Adresse IP |

**Attention :** L'interface réseau change selon ta distro. Vérifie avec `ip a`. Remplace `eth0` par la tienne (ex: `enp3s0`, `wlan0`).

```
${upspeed eth0}
${downspeed eth0}
```

### Processus

| Variable | Description |
|---|---|
| `$processes` | Nombre total de processus |
| `$running_processes` | Processus actifs |
| `$top name 1` | Processus le plus CPU (nom) |
| `$top cpu 1` | % CPU du premier processus |
| `$top mem 1` | % RAM du premier processus |

---

## 6. Formatage et Alignement

### Bargraphiques

```
${membar 5, 150}    → barre RAM, 5 pixels de haut, 150px de large
${cpubar 5, 100}    → barre CPU
${fs_bar 5, /}      → barre espace disque /
```

### Texte aligné (tableaux dans Conky)

```
${alignc} Centré
${alignr} Aligné à droite
${alignl} Aligné à gauche
```

### Sauts de ligne

```
${goto X}           → Se positionner à X pixels du bord gauche
${voffset Y}        → Décaler verticalement de Y pixels
${offset X}         → Décaler horizontalement de X pixels
```

### Exemple de tableau formaté :

```
${color grey}CPU${goto 50}${color}${goto 90}${alignr}${color grey}RAM${color}
${color grey}$cpu%${goto 50}${membar 5, 90}${goto 150}${color grey}$memperc%${color}
```

---

## 7. Exemple Complet : Bureau Complet

```bash
conky.config = {
    update_interval = 2,
    double_buffer = true,
    no_buffers = true,
    use_xft = true,
    font = 'DejaVu Sans:size=9',
    alignment = 'top_right',
    gap_x = 10,
    gap_y = 10,
    own_window = true,
    own_window_class = 'Conky',
    own_window_argb_visual = true,
    own_window_argb_value = 180,
    own_window_type = 'desktop',
    own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',
    default_color = 'e0e0e0',
    color1 = '00d9ff',   -- cyan
    color2 = 'a855f7',   -- violet
};

conky.text = [[
${color1}╔══════════════════╗${color}
${color1}║  ${color2}SYSTÈME${color1}         ║${color}
${color grey}Hostname : ${color}$nodename
${color grey}Kernel   : ${color}$kernel
${color grey}Uptime   : ${color}$uptime

${color1}╔══════════════════╗${color}
${color1}║  ${color2}CPU${color1}              ║${color}
${color grey}Usage     : ${color}$cpu%
${color grey}$cpubar
${color grey}Fréquence : ${color}$freq_g GHz

${color1}╔══════════════════╗${color}
${color1}║  ${color2}MÉMOIRE${color1}           ║${color}
${color grey}RAM       : ${color}$mem / $memmax
${color grey}$membar
${color grey}Swap      : ${color}$swap / $swapmax

${color1}╔══════════════════╗${color}
${color1}║  ${color2}DISQUES${color1}           ║${color}
${color grey}/ (root)  : ${color}$fs_used / $fs_size
${color grey}$fs_bar

${color1}╔══════════════════╗${color}
${color1}║  ${color2}RÉSEAU${color1}            ║${color}
${color grey}Download  : ${color}$downspeed
${color grey}Upload    : ${color}$upspeed
${color grey}Total Dn  : ${color}$totaldown
${color grey}Total Up  : ${color}$totalup

${color1}╔══════════════════╗${color}
${color1}║  ${color2}TOP 3 CPU${color1}         ║${color}
${color grey}1. ${color}$top name 1 ${color}$top cpu 1%
${color grey}2. ${color}$top name 2 ${color}$top cpu 2%
${color grey}3. ${color}$top name 3 ${color}$top cpu 3%

${color1}╔══════════════════╗${color}
${color1}║  ${color2}TOP 3 RAM${color1}         ║${color}
${color grey}1. ${color}$top_mem name 1 ${color}$top_mem mem 1%
${color grey}2. ${color}$top_mem name 2 ${color}$top_mem mem 2%
${color grey}3. ${color}$top_mem name 3 ${color}$top_mem mem 3%

${color1}╔══════════════════╗${color}
${color1}║  ${color2}DATE & HEURE${color1}     ║${color}
${color grey}$date
${color grey}$time
]]
```

---

## 8. Lancer Conky au Démarrage

### Méthode automatique (Debian/Ubuntu)

```bash
# Créer le dossier de config
mkdir -p ~/.config/conky

# Copier ou créer ta config
cp ma-config.conf ~/.config/conky/default.conf

# Créer un lanceur automatique
cat > ~/.config/autostart/conky.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Conky
Exec=conky -c ~/.config/conky/default.conf
X-GNOME-Autostart-enabled=true
EOF
```

### Méthode alternative (systemd user)

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/conky.service << 'EOF'
[Unit]
Description=Conky System Monitor

[Service]
ExecStart=/usr/bin/conky -c ~/.config/conky/default.conf
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now conky
```

---

## 9. Diagnostic et Erreurs Courantes

### Conky clignote

→ Ajouter `double_buffer = true` dans la section config.

### Conky apparaît par-dessus les fenêtres

→ Modifier `own_window_type` :
```bash
own_window_type = 'desktop'   # le plus stable
# ou
own_window_type = 'dock'      # alternative
```

### Transparence ne fonctionne pas

→ Assure-toi d'avoir `own_window_argb_visual = true` ET `own_window_argb_value` avec une valeur < 255.

### Informations réseau absentes

→ Vérifie le nom de ton interface :
```bash
ip a
```
Puis remplace `eth0` par le bon nom dans ta config.

### Conky ne se lance pas

```bash
# Mode verbose pour voir les erreurs
conky -c ~/.config/conky/default.conf -v
```

### Impossible de fermer un Conky

```bash
killall conky
```

---

## 10. Astuces Avancées

### Plusieurs instances (multi-monitor)

```bash
# Monitor 1 (gauche)
conky -c ~/.config/conky/gauche.conf &

# Monitor 2 (droite)
conky -c ~/.config/conky/droite.conf &
```

### Intégrer la météo

```bash
${execi 300 curl -s "wttr.in/Tavannes?format=3"}
```

L'option `execi 300` exécute la commande toutes les 300 secondes (5 min).

### Coloration conditionnelle

```bash
${if_match ${cpu}>80}${color red}${cpu}%${color}${else}${color grey}${cpu}%${endif}
```

Affiche le % CPU en rouge s'il dépasse 80%.

### Inclure un script Lua (graphiques)

Conky supporte les scripts Lua pour dessiner des graphiques circulaires, jauges, etc. (avancé).

---

## Résumé

| Concept | Commande / Valeur |
|---|---|
| Installer | `sudo apt install conky` |
| Lancer | `conky` ou `conky -c <fichier>` |
| Stopper | `killall conky` |
| Config par défaut | `~/.conkyrc` |
| Transparence | `own_window_argb_value = 150` |
| Position | `alignment = 'top_right'` |
| Rafraîchissement | `update_interval = 2` |
| Template couleurs | `grey`, `red`, `green`, `cyan`... |

---

Conky est un outil puissant mais qui peut sembler intimidant au début. Le secret : commence simple, puis ajoute les variables une par une. Un bon fichier de config bien commenté vaut mieux qu'un fichier complexe et mystérieux.

*Leçon créée avec ❤️ pour SkyLinux*
