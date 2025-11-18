#!/bin/bash
# filepath: deploy.sh
# chmod +x deploy.sh # Make executable

echo "Pulling latest changes..."
git pull origin main

echo "Building and deploying..."
docker-compose down
docker-compose up -d --build

echo "Cleaning up old images..."
docker image prune -f

echo "Deployment complete!"
docker-compose ps
