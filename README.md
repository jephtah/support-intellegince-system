# Support Intelligence API

AI-powered support ticket classification API built with FastAPI.

## Setup

```bash
# install deps
pip install -r requirements.txt

# setup env
cp .env.example .env
# edit .env with your settings

# run
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

## API

- POST `/api/v1/requests` - create ticket
- GET `/api/v1/requests/{id}` - get ticket  
- GET `/api/v1/requests` - list tickets
- GET `/api/v1/stats` - get stats

Docs at `/docs` when running.

## Notes

- uses openai for classification (fallback to rules if no key)
- stores tickets in postgres
- basic auth/security for prod
- TODO: add docker health checks
- TODO: add deployment scripts