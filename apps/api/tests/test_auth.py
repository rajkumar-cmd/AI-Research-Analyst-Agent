from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import Settings, get_settings
from app.core.database import Base, get_db
from app.main import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    test_settings = Settings(
        database_url="sqlite://",
        jwt_secret_key="test-secret-key-that-is-long-enough",
        api_cors_origins=["http://localhost:3000"],
    )

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_settings() -> Settings:
        return test_settings

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = override_get_settings

    with TestClient(app) as test_client:
        yield test_client


def test_signup_sets_session_cookie_and_returns_user(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "name": "Rajkumar Pradhan",
            "email": "rajkumar@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["user"]["email"] == "rajkumar@example.com"
    assert payload["user"]["role"] == "user"
    assert "research_agent_os_session" in response.cookies


def test_signup_rejects_duplicate_email(client: TestClient) -> None:
    payload = {
        "name": "Rajkumar Pradhan",
        "email": "rajkumar@example.com",
        "password": "StrongPass123",
    }
    assert client.post("/api/v1/auth/signup", json=payload).status_code == 201

    response = client.post("/api/v1/auth/signup", json=payload)

    assert response.status_code == 409


def test_signin_and_me_return_current_user(client: TestClient) -> None:
    signup_payload = {
        "name": "Rajkumar Pradhan",
        "email": "rajkumar@example.com",
        "password": "StrongPass123",
    }
    client.post("/api/v1/auth/signup", json=signup_payload)

    signin_response = client.post(
        "/api/v1/auth/signin",
        json={"email": "rajkumar@example.com", "password": "StrongPass123"},
    )
    assert signin_response.status_code == 200

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "rajkumar@example.com"


def test_signin_rejects_invalid_password(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/signup",
        json={
            "name": "Rajkumar Pradhan",
            "email": "rajkumar@example.com",
            "password": "StrongPass123",
        },
    )

    response = client.post(
        "/api/v1/auth/signin",
        json={"email": "rajkumar@example.com", "password": "WrongPass123"},
    )

    assert response.status_code == 401


def test_logout_clears_session_cookie(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/signup",
        json={
            "name": "Rajkumar Pradhan",
            "email": "rajkumar@example.com",
            "password": "StrongPass123",
        },
    )

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 204
    assert response.headers["set-cookie"].startswith("research_agent_os_session=")
