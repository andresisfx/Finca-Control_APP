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

def test_login_wrong_password(client: TestClient):
    """
    Prueba el fallo de login por contraseña incorrecta.
    """
    # Intentar hacer login de un usuario que no existe
    login_data = {
        "username": "noexiste@finca.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login/access-token", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Correo o contraseña incorrectos"
