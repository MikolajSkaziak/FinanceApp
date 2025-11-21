from fastapi.testclient import TestClient
from backend.app.main import app
from backend.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

# ---- Setup test DB ----
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Zastąpienie zależności get_db testową bazą
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ---- Testy ----

def test_register_and_login():
    # Rejestracja użytkownika (TWÓJ endpoint -> query params, nie JSON)
    response = client.post("/auth/register?username=testuser&email=testuser@example.com&password=testpass")
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

    # Logowanie użytkownika (OAuth2PasswordRequestForm -> x-www-form-urlencoded)
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_user():
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Nieprawidłowy login lub hasło"


def test_access_protected_route():
    # Rejestracja
    client.post("/auth/register?username=protecteduser&email=protected@example.com&password=securepass")

    # Logowanie
    response = client.post(
        "/auth/login",
        data={
            "username": "protecteduser",
            "password": "securepass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = response.json()["access_token"]

    # Dostęp do chronionego endpointu
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
