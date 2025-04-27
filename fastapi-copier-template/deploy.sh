#!/bin/bash

set -e

echo "🔵 Building multi-platform image and pushing to registry..."
docker buildx build --platform linux/amd64,linux/arm64 -t aminrx/public-api . --push

echo "🛠️ Pulling the latest pushed image..."
docker pull aminrx/public-api

echo "🚀 Bringing services up with docker-compose..."
docker-compose up -d --force-recreate

echo "✅ Deployment complete and services are updated!"
