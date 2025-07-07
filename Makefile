.PHONY: help install test lint format run docker-build docker-up migrate seed clean

# Default target
help:
	@echo "Support Intelligence API - Development Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install       - Install Python dependencies"
	@echo "  migrate       - Run database migrations"
	@echo "  seed          - Seed database with sample data"
	@echo ""
	@echo "Development Commands:"
	@echo "  run           - Start development server"
	@echo "  test          - Run test suite"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  lint          - Run code linting"
	@echo "  format        - Format code with black"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-up     - Start with Docker Compose"
	@echo "  docker-down   - Stop Docker services"
	@echo "  docker-logs   - View Docker logs"
	@echo ""
	@echo "Database Commands:"
	@echo "  db-reset      - Reset database (WARNING: destroys data)"
	@echo "  db-shell      - Open database shell"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  clean         - Clean temporary files"

# Setup commands
install:
	pip install -r requirements.txt

migrate:
	alembic upgrade head

seed:
	python scripts/seed_db.py

# Development commands
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

lint:
	flake8 app/ tests/
	mypy app/ --ignore-missing-imports

format:
	black app/ tests/ scripts/
	isort app/ tests/ scripts/

# Docker commands
docker-build:
	docker build -t support-api:latest .

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

# Database commands
db-reset:
	@echo "WARNING: This will destroy all data. Are you sure? [y/N]" && read ans && [ $${ans:-N} = y ]
	alembic downgrade base
	alembic upgrade head

db-shell:
	docker-compose exec db psql -U user -d support_db

# Cleanup commands
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# Development setup (run this first)
setup: install migrate seed
	@echo "Setup complete! Run 'make run' to start the server."

# Production build
build-prod: clean test docker-build
	@echo "Production build complete!"