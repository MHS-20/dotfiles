#!/bin/bash

echo "Starting Docker deep clean..."

# 1. Stop all running containers (you can't delete images/volumes in use)
if [ "$(docker ps -q)" ]; then
    echo "Stopping running containers..."
    docker stop $(docker ps -q)
fi

# 2. Remove all containers
if [ "$(docker ps -aq)" ]; then
    echo "Removing all containers..."
    docker rm $(docker ps -aq)
fi

# 3. Remove all images
if [ "$(docker images -q)" ]; then
    echo "Deleting all images..."
    docker rmi -f $(docker images -q)
fi

# 4. Remove all volumes
if [ "$(docker volume ls -q)" ]; then
    echo "Deleting all volumes..."
    docker volume rm $(docker volume ls -q)
fi

# 5. Final system prune to catch networks and build cache
echo "Cleaning up remaining networks and cache..."
docker system prune -a --volumes -f

echo "Docker is now empty."
