import pytest
from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    """
    Prueba el registro de un nuevo usuario.
    """
    # Datos del usuario (body)
    user_data = {
        "email": "test@finca.com",
        "nombre": "Granjero Test",
        "password": "supersecretpassword"
    }

    # Hacemos la petición POST al endpoint de registro
    response = client.post("/api/v1/users/", json=user_data)
    
    # Afirmaciones (Equivalente a expect().toBe() en Jest)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == "test@finca.com"
    assert data["nombre"] == "Granjero Test"
    assert "id" in data
    
    # Comprobar que no devuelve el password en la respuesta
    assert "password" not in data

def test_login_success(client: TestClient):
    """
    Prueba el inicio de sesión exitoso.
    """
    # 1. Primero creamos el usuario
    client.post("/api/v1/users/", json={
        "email": "login@finca.com",
        "nombre": "Granjero Login",
        "password": "supersecretpassword"
    })
    
    # 2. Intentamos hacer Login
    # OAuth2 requiere que los datos se envíen como 'data' (form-data), no como 'json'
    login_data = {
        "username": "login@finca.com",
        "password": "supersecretpassword"
    }
    response = client.post("/api/v1/auth/login/access-token", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Debe devolver el access_token
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_usuario_inexistente(client: TestClient):
    """
    Un usuario que no existe en la DB debe recibir 401.
    """
    login_data = {
        "username": "noexiste@finca.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login/access-token", data=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Correo o contraseña incorrectos"


def test_login_password_incorrecta(client: TestClient):
    """
    Un usuario que existe pero envía la password incorrecta debe recibir 401.
    """
    # Crear usuario primero
    client.post("/api/v1/users/", json={
        "email": "existe@finca.com",
        "nombre": "Usuario Existente",
        "password": "passwordcorrecta"
    })

    login_data = {
        "username": "existe@finca.com",
        "password": "passwordincorrecta"
    }
    response = client.post("/api/v1/auth/login/access-token", data=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Correo o contraseña incorrectos"


def test_registro_email_duplicado(client: TestClient):
    # Arrange: crear usuario con email X
    user_data = {
        "email": "duplicado@finca.com",
        "nombre": "Granjero Duplicado",
        "password": "supersecretpassword"
    }
    client.post("/api/v1/users/", json=user_data)

    # Act: intentar crear otro usuario con el mismo email X
    response = client.post("/api/v1/users/", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado."


def test_registro_body_vacio(client: TestClient):
    # Act
    response = client.post("/api/v1/users/", json={})

    # Assert
    assert response.status_code == 422


def test_registro_email_invalido(client: TestClient):
    # Act
    response = client.post("/api/v1/users/", json={
        "email": "no-es-un-email",
        "nombre": "Granjero Invalido",
        "password": "supersecretpassword"
    })

    # Assert
    assert response.status_code == 422


def test_token_malformado_rechazado(client: TestClient):
    # Act
    response = client.get(
        "/api/v1/fincas/mis-fincas",
        headers={"Authorization": "Bearer token_corrupto"}
    )

    # Assert
    assert response.status_code == 401
