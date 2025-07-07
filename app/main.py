from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.requests import router as requests_router
from app.database import engine, Base
from app.config import settings
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create tables
Base.metadata.create_all(bind=engine)

# fastapi app
app = FastAPI(
    title="Customer Support Intelligence API",
    description="AI-powered customer support request classification and automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# cors setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: configure for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: add rate limiting
# TODO: add request logging

# routes
app.include_router(requests_router, prefix=settings.API_PREFIX)
# TODO: add api versioning strategy

@app.get("/")
async def root():
    """root endpoint"""
    return {
        "message": "Support Intelligence API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """health check"""
    return {
        "status": "healthy", 
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)