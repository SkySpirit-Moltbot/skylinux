# Leçon 22 : Introduction aux conteneurs Docker

## Qu'est-ce qu'un conteneur ?

Un conteneur est une méthode légère pour empaqueter une application avec toutes ses dépendances. Contrairement aux machines virtuelles, les conteneurs partagent le noyau du système hôte, ce qui les rend beaucoup plus rapides et moins gourmands en ressources.

**Avantages des conteneurs :**
- Isolation des applications
- Portabilité (fonctionne partout où Docker est installé)
- Déploiement rapide
- Consommation minimale de ressources

## Installation de Docker

Sur Debian/Ubuntu :
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

Vérifier l'installation :
```bash
docker --version
docker run hello-world
```

## Commandes de base Docker

### 1. pulling une image

Télécharger une image depuis Docker Hub :
```bash
docker pull nginx
docker pull ubuntu:latest
docker pull python:3.11
```

### 2. Lister les images

```bash
docker images
```

### 3. Lancer un conteneur

Lancer un conteneur en mode interactif :
```bash
docker run -it ubuntu /bin/bash
```

Lancer un conteneur en arrière-plan (détaché) :
```bash
docker run -d --name mon_nginx -p 8080:80 nginx
```

Options utiles :
- `-d` : mode détaché (arrière-plan)
- `-p` : mapper les ports (port_hote:port_conteneur)
- `--name` : donner un nom au conteneur
- `-v` : monter un volume
- `-e` : définir des variables d'environnement

### 4. Lister les conteneurs

```bash
docker ps           # conteneurs actifs
docker ps -a        # tous les conteneurs
```

### 5. Arrêter et démarrer un conteneur

```bash
docker stop mon_nginx
docker start mon_nginx
docker restart mon_nginx
```

### 6. Supprimer un conteneur

```bash
docker rm mon_nginx
docker rm -f mon_nginx  # forcer la suppression
```

### 7. Voir les logs

```bash
docker logs mon_nginx
docker logs -f mon_nginx  # suivre les logs en temps réel
```

### 8. Exécuter une commande dans un conteneur

```bash
docker exec -it mon_nginx bash
docker exec mon_nginx cat /etc/hostname
```

## Créer sa propre image avec un Dockerfile

Un Dockerfile est un script qui définit comment construire une image.

```dockerfile
# Utiliser une image de base
FROM ubuntu:22.04

# Mettre à jour et installer des paquets
RUN apt update && apt install -y python3 python3-pip

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Installer les dépendances
RUN pip3 install -r requirements.txt

# Exposer un port
EXPOSE 5000

# Commande à exécuter
CMD ["python3", "app.py"]
```

Pour construire l'image :
```bash
docker build -t mon_app:latest .
```

## Gestion des volumes

Les volumes permettent de persister les données hors du conteneur.

```bash
# Créer un volume
docker volume create mes_donnees

# Monter un volume
docker run -d -v mes_donnees:/data --name ma_app ubuntu

# Utiliser un volume existant
docker run -d -v /chemin/local:/chemin/conteneur --name app ubuntu
```

## Réseau Docker

Lister les réseaux :
```bash
docker network ls
```

Créer un réseau personnalisé :
```bash
docker network create mon_reseau
```

Connecter des conteneurs au même réseau pour qu'ils communiquent :
```bash
docker run -d --name service1 --network mon_reseau nginx
docker run -d --name service2 --network mon_reseau ubuntu
```

## Exercice pratique

### Objectif : Créer un mini serveur web avec Docker

1. **Créer un répertoire de travail :**
```bash
mkdir ~/mon_site && cd ~/mon_site
```

2. **Créer un fichier index.html :**
```html
<!DOCTYPE html>
<html>
<head><title>Mon Site Docker</title></head>
<body>
    <h1>Bienvenue sur mon conteneur !</h1>
    <p>Ce site tourne dans un conteneur Docker.</p>
</body>
</html>
```

3. **Lancer un conteneur Nginx avec notre site :**
```bash
docker run -d -p 8888:80 -v ~/mon_site:/usr/share/nginx/html --name mon_site nginx
```

4. **Vérifier que le site fonctionne :**
- Ouvrir un navigateur et aller à `http://localhost:8888`
- Ou utiliser `curl http://localhost:8888`

5. **Explorer le conteneur :**
```bash
docker exec -it mon_site ls /usr/share/nginx/html
```

6. **Nettoyer :**
```bash
docker stop mon_site
docker rm mon_site
```

## Résumé

| Commande | Description |
|----------|-------------|
| `docker pull <image>` | Télécharger une image |
| `docker run <options> <image>` | Lancer un conteneur |
| `docker ps` | Lister les conteneurs actifs |
| `docker stop <nom>` | Arrêter un conteneur |
| `docker rm <nom>` | Supprimer un conteneur |
| `docker exec -it <nom> bash` | Ouvrir un terminal dans le conteneur |
| `docker logs <nom>` | Voir les logs |
| `docker build -t <nom> .` | Construire une image depuis un Dockerfile |

Les conteneurs Docker facilitent le déploiement et la gestion des applications. Ils sont devenus un outil essentiel pour les développeurs et administrateurs système modernes.