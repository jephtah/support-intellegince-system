from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# TODO: add connection pooling config

# base class for models 
Base = declarative_base()

def get_db():
    """db dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()