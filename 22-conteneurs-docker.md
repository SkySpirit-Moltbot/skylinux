# Leçon 22 : Conteneurs Docker

## Introduction

Docker est une plateforme de conteneurisation qui permet d'empaqueter une application avec toutes ses dépendances. Les conteneurs sont légers, rapides et portables.

**Pourquoi utiliser Docker ?**
- Isolation des applications
- Portabilité (fonctionne partout)
- Déploiement rapide
- Ressources minimales

## Installation de Docker

### Sur Debian/Ubuntu
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### Vérifier l'installation
```bash
docker --version
docker-compose --version
docker run hello-world
```

## Concepts fondamentaux

### Images vs Conteneurs
- **Image** : Modèle en lecture seule (template)
- **Conteneur** : Instance en cours d'exécution d'une image

### Docker Hub
Registre public contenant des milliers d'images prédéfinies.

## Commandes de base

### Gestion des images
```bash
# Télécharger une image
docker pull nginx
docker pull ubuntu:22.04
docker pull python:3.11

# Lister les images locales
docker images
docker images -a

# Supprimer une image
docker rmi nginx
docker rmi -f nginx
```

### Lancer des conteneurs
```bash
# Mode interactif
docker run -it ubuntu /bin/bash

# Mode détaché (arrière-plan)
docker run -d --name mon_nginx -p 8080:80 nginx

# Avec variables d'environnement
docker run -d --name ma_db -e MYSQL_ROOT_PASSWORD=mdp123 mysql

# Avec volume persisté
docker run -d -v /data:/app --name mon_app ubuntu

# Avec restart automatique
docker run -d --restart=always --name nginx nginx
```

### Options courantes
| Option | Description |
|--------|-------------|
| `-d` | Mode détaché |
| `-p` | Mapping de ports (hôte:conteneur) |
| `--name` | Nom du conteneur |
| `-v` | Volume |
| `-e` | Variable d'environnement |
| `--restart` | Politique de redémarrage |
| `--network` | Réseau Docker |

### Gestion des conteneurs
```bash
# Lister les conteneurs
docker ps              # actifs
docker ps -a          # tous
docker ps -q          # juste les IDs

# Arrêter/démarrer
docker stop mon_nginx
docker start mon_nginx
docker restart mon_nginx

# Supprimer
docker rm mon_nginx
docker rm -f mon_nginx   # forcer

# Voir les logs
docker logs mon_nginx
docker logs -f mon_nginx     # temps réel
docker logs --tail 100 mon_nginx

# Exécuter une commande
docker exec -it mon_nginx bash
docker exec mon_nginx cat /etc/hostname

# Inspecter un conteneur
docker inspect mon_nginx
docker stats mon_nginx   # ressources en temps réel
```

## Créer une image personnalisée

### Le Dockerfile

```dockerfile
# Commentaire
FROM ubuntu:22.04

# Mise à jour et installation
RUN apt update && apt install -y python3 python3-pip

# Variable d'environnement
ENV APP_ENV=production

# Répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
COPY . .

# Exposer un port
EXPOSE 5000

# Commande par défaut
CMD ["python3", "app.py"]
```

### Instructions courantes du Dockerfile
| Instruction | Description |
|-------------|-------------|
| FROM | Image de base |
| RUN | Commande à exécuter |
| COPY | Copier des fichiers |
| WORKDIR | Répertoire de travail |
| ENV | Variable d'environnement |
| EXPOSE | Port à exposer |
| CMD | Commande par défaut |
| ENTRYPOINT | Point d'entrée |

### Construire et utiliser son image
```bash
# Construire l'image
docker build -t mon_app:latest .

# Vérifier
docker images | grep mon_app

# Lancer
docker run -d -p 5000:5000 --name mon_app mon_app:latest
```

## Les volumes

### Types de volumes

1. **Volumes nommés**
```bash
docker volume create mes_donnees
docker run -d -v mes_donnees:/data --name app ubuntu
```

2. **Bind mounts (répertoire hôte)**
```bash
docker run -d -v ~/mon_repertoire:/app --name app ubuntu
```

3. **tmpfs (en mémoire)**
```bash
docker run -d --tmpfs /tmp --name app ubuntu
```

### Gestion des volumes
```bash
# Lister
docker volume ls

# Inspecter
docker volume inspect mon_volume

# Supprimer
docker volume rm mon_volume
docker volume prune  # nettoyer les volumes inutilisés
```

## Réseau Docker

### Créer un réseau
```bash
# Lister les réseaux
docker network ls

# Créer un réseau personnalisé
docker network create mon_reseau

# Créer avec driver spécifique
docker network create --driver bridge mon_reseau
```

### Connecter des conteneurs
```bash
# Lancer sur un réseau
docker run -d --network mon_reseau --name web nginx
docker run -d --network mon_reseau --name db mysql

# Les conteneurs peuvent maintenant se contacter par nom
```

### DNS automatique
Les conteneurs sur le même réseau peuvent se trouver par leur nom.

## Docker Compose

Docker Compose permet de définir et exécuter des applications multi-conteneurs.

### Le fichier docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - api
    networks:
      - frontend
      - backend

  api:
    build: ./api
    environment:
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=mdp123
      - POSTGRES_DB=mondb
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  db_data:
```

### Commandes Docker Compose
```bash
# Lancer tous les services
docker-compose up
docker-compose up -d          # détaché

# Arrêter
docker-compose down
docker-compose down -v         # supprimer aussi les volumes

# Logs
docker-compose logs -f
docker-compose logs -f web     # service spécifique

# Statut
docker-compose ps
docker-compose top

# Reconstruire
docker-compose build
docker-compose up --build
```

## Cas d'usage pratiques

### 1. Serveur web Nginx
```bash
docker run -d -p 80:80 --name nginx nginx:alpine
```

### 2. Base de données PostgreSQL
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=mdp123 \
  -e POSTGRES_DB=mondb \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15
```

### 3. Serveur de développement Python
```bash
docker run -it -p 5000:5000 -v $(pwd):/app python:3.11 sh -c "pip install flask && cd /app && flask run --host=0.0.0.0"
```

### 4. Monitoring avec Prometheus
```bash
docker run -d -p 9090:9090 --name prometheus prom/prometheus
```

## Bonnes pratiques

### Sécurité
```bash
# Ne pas exécuter en root
USER nobody

# Scanner les vulnérabilités
docker scan mon_image

# Utiliser des images officielles
docker pull nginx:latest
```

### Optimisation
```bash
# Combiner les couches RUN
RUN apt update && apt install -y package1 package2 && rm -rf /var/lib/apt/lists/*

# Utiliser des images légères
docker pull alpine
docker pull nginx:alpine

# Nettoyer les caches
docker builder prune
```

### Utiliser .dockerignore
```
.git
node_modules
__pycache__
*.log
.env
```

## Dépannage

```bash
# Voir tous les conteneurs (même arrêtés)
docker ps -a

# Logs en temps réel
docker logs -f --tail 50 conteneur

# Ressources utilisées
docker stats

# Entrer dans le conteneur
docker exec -it conteneur bash

# Inspecter la configuration
docker inspect conteneur

# Voir les processus
docker top conteneur

# Redémarrer un conteneur planté
docker restart conteneur

# Nettoyer tout
docker system prune -a
```

## Résumé des commandes

| Commande | Action |
|----------|--------|
| `docker pull image` | Télécharger une image |
| `docker run -d -p 80:80 --name nom image` | Lancer un conteneur |
| `docker ps` | Lister les conteneurs actifs |
| `docker stop nom` | Arrêter |
| `docker rm nom` | Supprimer |
| `docker exec -it nom bash` | Terminal dans le conteneur |
| `docker logs -f nom` | Voir les logs |
| `docker build -t nom .` | Construire une image |
| `docker-compose up -d` | Lancer une application |
| `docker volume create nom` | Créer un volume |
| `docker network create nom` | Créer un réseau |

## Aller plus loin

- Docker Swarm pour l'orchestration
- Kubernetes pour la production
- Portainer pour une interface graphique
- GitLab CI/CD pour l'intégration continue

