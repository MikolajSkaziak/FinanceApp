import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.db import get_db
from backend.models.Base import Base

# TEST CONFIGURATION
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

# TESTS
def test_register_user_success():
    """Test poprawnej rejestracji użytkownika"""

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword"
    }
    

    response = client.post("/auth/register", json=user_data)
    

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_user_duplicate_username():
    """Test rejestracji z istniejącą nazwą użytkownika"""
    user_data = {
        "username": "existinguser",
        "email": "existing@example.com",
        "password": "TestPassword123!"
    }
    client.post("/auth/register", json=user_data)

    duplicate_user_data = {
        "username": "existinguser",  
        "email": "new@example.com",
        "password": "TestPassword123!"
    }
    response = client.post("/auth/register", json=duplicate_user_data)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

def test_register_user_duplicate_email():
    """Test rejestracji z istniejącym emailem"""
    user_data = {
        "username": "user1",
        "email": "same@example.com",
        "password": "TestPassword123!"
    }
    client.post("/auth/register", json=user_data)

    duplicate_user_data = {
        "username": "user2",
        "email": "same@example.com",  
        "password": "TestPassword123!"
    }
    response = client.post("/auth/register", json=duplicate_user_data)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

def test_login_success():
    """Test poprawnego logowania"""
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "TestPassword"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": "loginuser",
        "password": "TestPassword"
    }
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Test logowania z błędnym hasłem"""
    user_data = {
        "username": "loginuser2",
        "email": "login2@example.com",
        "password": "CorrectPassword"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": "loginuser2",
        "password": "WrongPassword" 
    }
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_user():
    """Test logowania nieistniejącego użytkownika"""
    login_data = {
        "username": "nonexistent",
        "password": "SomePassword"
    }
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_get_me_success():
    """Test pobierania danych użytkownika z tokenem"""
    user_data = {
        "username": "meuser",
        "email": "me@example.com",
        "password": "TestPassword"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": "meuser",
        "password": "TestPassword"
    }
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    response = client.get(f"/auth/me?token={token}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"

def test_get_me_invalid_token():
    """Test pobierania danych z nieprawidłowym tokenem"""
    response = client.get("/auth/me?token=invalid_token")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_me_no_token():
    """Test pobierania danych bez tokena"""
    response = client.get("/auth/me")
    
    assert response.status_code == 422 