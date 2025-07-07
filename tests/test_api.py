import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

# test db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# import app after db setup
from app.main import app
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_request():
    """basic create test"""
    response = client.post(
        "/api/v1/requests",
        json={"text": "my app crashed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["body"] == "my app crashed"

def test_create_request_with_subject_body():
    """test subject/body format"""
    response = client.post(
        "/api/v1/requests",
        json={
            "subject": "Billing Issue",
            "body": "I was charged twice"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Billing Issue"
    assert data["body"] == "I was charged twice"

def test_get_request():
    """basic get test"""
    # create first
    create_response = client.post(
        "/api/v1/requests",
        json={"text": "test request"}
    )
    request_id = create_response.json()["id"]
    
    # get it
    response = client.get(f"/api/v1/requests/{request_id}")
    assert response.status_code == 200
    assert response.json()["id"] == request_id

def test_filter_by_category():
    """test category filtering"""
    # create technical request
    client.post("/api/v1/requests", json={"text": "server crashed with memory error"})
    
    response = client.get("/api/v1/requests?category=technical")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

def test_get_stats():
    """test stats endpoint"""
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert "technical" in data
    assert "billing" in data
    assert "general" in data
    assert "total" in data

def test_validation_error():
    """test input validation"""
    response = client.post("/api/v1/requests", json={})
    assert response.status_code == 422

@pytest.fixture(autouse=True)
def cleanup_database():
    """clean up after tests"""
    yield
    # cleanup logic here if needed