# Leçon 25 : Docker Compose et orchestration de containers

## Introduction

Docker Compose est un outil qui permet de définir et gérer des applications multi-containers. Au lieu de lancer chaque container séparément avec des commandes longues, vous描述ez toute votre stack dans un fichier YAML et vous lancez tout avec une seule commande.

## Installation de Docker Compose

### Via apt (Debian/Ubuntu)

```bash
# Installation
sudo apt update
sudo apt install docker-compose

# Vérifier la version
docker-compose --version
```

### Via Python pip

```bash
sudo pip install docker-compose
```

### Utiliser Docker Compose v2 (recommandé)

```bash
# Docker Compose est maintenant un plugin
docker compose version
```

## Le fichier docker-compose.yml

### Structure de base

```yaml
version: '3.8'

services:
  nom_du_service:
    image: nom_image
    container_name: mon_conteneur
    ports:
      - "8080:80"
    volumes:
      - ./data:/app/data
    environment:
      - ENV_VAR=valeur
    depends_on:
      - autre_service
    restart: always
    networks:
      - mon_reseau

networks:
  mon_reseau:
    driver: bridge

volumes:
  mon_volume:
```

### Exemple : Stack web simple

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    restart: always

  app:
    build: .
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/madb

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=madb
    restart: always

volumes:
  postgres_data:
```

## Commandes de base

### Lancer et arrêter

```bash
# Lancer tous les services
docker-compose up -d

# Lancer avec reconstruction
docker-compose up -d --build

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Arrêter et supprimer les images
docker-compose down --rmi local
```

### Gestion des services

```bash
# Voir le statut
docker-compose ps

# Voir les logs
docker-compose logs
docker-compose logs -f
docker-compose logs -f app

# Exécuter une commande dans un service
docker-compose exec app ls -la
docker-compose exec db psql -U user -d madb

# Voir les processus
docker-compose top
```

### Manipulation des services

```bash
# Redémarrer un service
docker-compose restart app

# Recréer un service
docker-compose recreate app

# Mettre à l'échelle un service (swarm mode requis pour plusieurs instances)
docker-compose up -d --scale app=3

# Pause / Unpause
docker-compose pause
docker-compose unpause
```

## Variables d'environnement

### Fichier .env

Créez un fichier `.env` à la racine du projet :

```
POSTGRES_USER=monuser
POSTGRES_PASSWORD=monpassword
POSTGRES_DB=mabasededonnees
NGINX_PORT=8080
```

### Utilisation dans docker-compose.yml

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}

  web:
    image: nginx:alpine
    ports:
      - "${NGINX_PORT}:80"
```

### Variables d'environnement supplémentaires

```yaml
services:
  app:
    environment:
      - NODE_ENV=production
      - DEBUG=false
    env_file:
      - ./variables.env
```

## Networks et Volumes nommés

### Networks personnalisés

```yaml
version: '3.8'

services:
  frontend:
    image: nginx:alpine
    networks:
      - frontend_network

  backend:
    image: node:alpine
    networks:
      - frontend_network
      - backend_network

  db:
    image: postgres:15-alpine
    networks:
      - backend_network

networks:
  frontend_network:
    driver: bridge
  backend_network:
    driver: bridge
    internal: true  # Pas d'accès internet
```

### Volumes nommés

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Bind mounts (chemins locaux)

```yaml
services:
  web:
    image: nginx:alpine
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

## Healthchecks et dépendances

### Healthcheck

```yaml
services:
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d madb"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
```

### Dépendances simples

```yaml
services:
  app:
    depends_on:
      - db
      - redis
    # db et redis démarreront avant app
```

## Commandes avancées

### Build personnalisé

```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.prod
      args:
        - BUILD_VERSION=1.0
```

```bash
docker-compose build
docker-compose build --no-cache
```

### Override de configuration

```bash
# Utiliser un fichier spécifique
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Fichier de développement
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Mode interactif

```bash
# Lancer sans detached mode
docker-compose up

# Avec logs en temps réel
docker-compose up --remove-orphans
```

## Exemple : Stack complète

```yaml
version: '3.8'

services:
  reverse_proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - webapp
    networks:
      - frontend

  webapp:
    build: ./webapp
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/madb
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - frontend
      - backend
    restart: always

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=madb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d madb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7-alpine
    networks:
      - backend
    restart: always

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres_data:
```

## Résumé des commandes

| Commande | Utilité |
|----------|---------|
| `docker-compose up -d` | Lancer les services en arrière-plan |
| `docker-compose down` | Arrêter les services |
| `docker-compose ps` | Voir le statut des services |
| `docker-compose logs -f` | Voir les logs en temps réel |
| `docker-compose exec service cmd` | Exécuter une commande |
| `docker-compose build` | Construire les images |
| `docker-compose restart service` | Redémarrer un service |
| `docker-compose -f file.yml up` | Utiliser un fichier spécifique |

## Exercice pratique

1. Créez un fichier `docker-compose.yml` avec un serveur web Nginx et une application Node.js
2. Configurez un volume partagé entre les deux services
3. Ajoutez un healthcheck sur l'application
4. Testez les commandes `up`, `down`, `logs` et `exec`
5. Créez un fichier `.env` et utilisez des variables d'environnement
6. Expérimentez avec plusieurs fichiers compose et l'option `-f`

## Conclusion

Docker Compose simplifie considérablement la gestion des applications multi-containers. Au lieu de lancer des commandes complexes, vous décrivez votre infrastructure dans un fichier YAML versionnable. C'est indispensable pour le développement local et très utile pour les déploiements de petite ou moyenne échelle.