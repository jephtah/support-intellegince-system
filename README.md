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

### With More Time
- **Authentication** — I’d start with JWT, but probably add role-based auth once multi-user access is needed.
- **Rate limiting** — Redis-backed to avoid accidental DoS if someone spams the AI endpoints.
- **Caching** — To save API cost, but I'd only add this once we know requests are repeatable enough.

### In Prod:
- **Security headers** - I'd add CORS, CSP, etc.
- **CI/CD pipeline** - If we're deploying this, important for automated testing and deployment
- **Error tracking** - I'd add Sentry for production monitoring
- **Health checks** - Need proper health endpoints for container orchestration
- **Secrets management** - Should move from env vars to a proper secrets manager

### Code Quality
- **More granular tests** - I'd add more edge case testing and error scenarios
- **Type checking** - Could add mypy for better type safety
- **API documentation** - Should validate the OpenAPI spec in CI

The current implementation prioritizes functionality. I focused on getting a working MVP quickly. With real usage, I'd revisit these areas and maybe more.