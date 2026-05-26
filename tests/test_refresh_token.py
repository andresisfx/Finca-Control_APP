import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _register_and_login(client: TestClient, email: str, password: str = "testpassword123") -> dict:
    """Crea un usuario y devuelve el dict completo de tokens del login."""
    client.post("/api/v1/users/", json={
        "email": email,
        "nombre": "Test User",
        "password": password,
    })
    login_resp = client.post("/api/v1/auth/login/access-token", data={
        "username": email,
        "password": password,
    })
    assert login_resp.status_code == 200, f"Login fallido: {login_resp.json()}"
    return login_resp.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_login_retorna_ambos_tokens(client: TestClient):
    # Arrange
    email = "user_login_ambos@test.com"

    # Act
    tokens = _register_and_login(client, email)

    # Assert
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"]
    assert tokens["refresh_token"]


def test_login_refresh_token_almacenado_en_db(client: TestClient, db_session: Session):
    # Arrange
    email = "user_db_check@test.com"
    tokens = _register_and_login(client, email)
    refresh_token_value = tokens["refresh_token"]

    # Act
    import hashlib
    token_hash = hashlib.sha256(refresh_token_value.encode()).hexdigest()
    db_token = db_session.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()

    # Assert
    assert db_token is not None
    assert db_token.revoked is False


def test_refresh_exitoso_retorna_nuevo_par(client: TestClient):
    # Arrange
    email = "user_refresh_exitoso@test.com"
    tokens = _register_and_login(client, email)
    refresh_token = tokens["refresh_token"]

    # Act
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["refresh_token"]


def test_nuevo_access_token_es_valido(client: TestClient):
    # Arrange
    email = "user_nuevo_access@test.com"
    tokens = _register_and_login(client, email)
    refresh_token = tokens["refresh_token"]

    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    new_access_token = refresh_resp.json()["access_token"]

    # Act
    response = client.get(
        "/api/v1/fincas/mis-fincas",
        headers={"Authorization": f"Bearer {new_access_token}"},
    )

    # Assert
    assert response.status_code == 200


def test_token_rotation_token_antiguo_invalido(client: TestClient):
    # Arrange
    email = "user_rotation@test.com"
    tokens = _register_and_login(client, email)
    original_refresh_token = tokens["refresh_token"]

    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": original_refresh_token})
    assert refresh_resp.status_code == 200

    # Act
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": original_refresh_token})

    # Assert
    assert response.status_code == 401


def test_refresh_con_token_invalido(client: TestClient):
    # Arrange
    token_invalido = "esto.no.es.un.token.valido"

    # Act
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": token_invalido})

    # Assert
    assert response.status_code == 401


def test_refresh_con_token_revocado(client: TestClient):
    # Arrange
    email = "user_refresh_revocado@test.com"
    tokens = _register_and_login(client, email)
    refresh_token = tokens["refresh_token"]

    logout_resp = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout_resp.status_code == 204

    # Act
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == 401


def test_refresh_body_vacio(client: TestClient):
    # Arrange / Act
    response = client.post("/api/v1/auth/refresh", json={})

    # Assert
    assert response.status_code == 422


def test_logout_exitoso(client: TestClient):
    # Arrange
    email = "user_logout_exitoso@test.com"
    tokens = _register_and_login(client, email)
    refresh_token = tokens["refresh_token"]

    # Act
    response = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == 204
    assert response.content == b""


def test_logout_y_refresh_falla(client: TestClient):
    # Arrange
    email = "user_logout_refresh@test.com"
    tokens = _register_and_login(client, email)
    refresh_token = tokens["refresh_token"]

    logout_resp = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout_resp.status_code == 204

    # Act
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == 401


def test_logout_con_token_invalido(client: TestClient):
    # Arrange
    token_invalido = "token.completamente.invalido"

    # Act
    response = client.post("/api/v1/auth/logout", json={"refresh_token": token_invalido})

    # Assert
    assert response.status_code == 401


def test_logout_con_token_ya_revocado(client: TestClient):
    # Arrange
    email = "user_doble_logout@test.com"
    tokens = _register_and_login(client, email)
    refresh_token = tokens["refresh_token"]

    first_logout = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert first_logout.status_code == 204

    # Act
    response = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == 401


def test_logout_body_vacio(client: TestClient):
    # Arrange / Act
    response = client.post("/api/v1/auth/logout", json={})

    # Assert
    assert response.status_code == 422
