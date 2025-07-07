#!/bin/bash
# quick-start.sh - Quick setup for local dev

set -e

echo "Support Intelligence API - Quick Start"
echo "==============================================="

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo "Docker not running. Please start Docker."
    exit 1
fi

# Copy .env if needed
if [ ! -f .env ]; then
    echo "Copying .env.example to .env"
    cp .env.example .env
    echo "Edit .env to set your OpenAI API key if you want AI features."
fi

# Start services
echo "Starting Docker Compose..."
docker-compose up --build -d

# Wait for DB (just a basic wait, not perfect)
echo "Waiting for DB to be ready..."
sleep 10

# Run migrations
echo "Running migrations..."
docker-compose exec app alembic upgrade head

# Seed DB (optional, comment out if not needed)
echo "Seeding DB with sample data..."
docker-compose exec app python scripts/seed_db.py

echo ""
echo "Setup done!"
echo "API docs: http://localhost:8000/docs"
echo "Health:   http://localhost:8000/health"
echo ""
echo "To stop:  docker-compose down"
echo "To test:  docker-compose exec app pytest"
echo ""

# Quick health check
if command -v curl > /dev/null; then
    status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
    if [ "$status" = "200" ]; then
        echo "API is up!"
    else
        echo "API health check failed. Check logs: docker-compose logs app"
    fi
fi