#!/bin/bash

# Load environment variables
set -a
source ../.env
set +a

# Function to check if a command was successful
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

# Pull latest code
echo "Pulling latest code..."
git pull
check_status "Failed to pull latest code"

# Build and start containers
echo "Building and starting containers..."
docker-compose build
check_status "Failed to build containers"

docker-compose up -d
check_status "Failed to start containers"

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run database migrations (if needed)
echo "Running database migrations..."
docker-compose exec api flask db upgrade
check_status "Failed to run database migrations"

# Check services health
echo "Checking service health..."
docker-compose ps
check_status "Service health check failed"

echo "Deployment completed successfully!"