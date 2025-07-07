# Support Intelligence API

AI-powered support ticket classification API built with FastAPI.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (or use Docker)

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database settings

# Run migrations
alembic upgrade head

# Optional: Seed with sample data
python scripts/seed_db.py

# Start server
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
API docs: http://localhost:8000/docs



## API Endpoints

- `POST /api/v1/requests` - Create support ticket
- `GET /api/v1/requests/{id}` - Get specific ticket
- `GET /api/v1/requests` - List all tickets (with optional filters)
- `GET /api/v1/stats` - Get ticket statistics

## Development


### Commands

```bash
# Run tests
pytest

# Database migrations
alembic upgrade head

# Seed database
python scripts/seed_db.py

# Code formatting
black app/ tests/
```

### Example Usage

```bash
# Create a ticket
curl -X POST "http://localhost:8000/api/v1/requests" \
  -H "Content-Type: application/json" \
  -d '{"text": "The app crashes on startup"}'

# Get all tickets
curl "http://localhost:8000/api/v1/requests"
```

## Testing

```bash
pytest
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for classification | No |