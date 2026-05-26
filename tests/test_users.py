import uuid
from fastapi.testclient import TestClient


def test_listar_usuarios(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/users/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for user in data:
        assert "password" not in user


def test_obtener_usuario_por_id(client: TestClient, auth_headers: dict):
    create_resp = client.post(
        "/api/v1/users/",
        json={"email": "buscar@finca.com", "nombre": "Usuario Buscable", "password": "secret123"},
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/users/{user_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "buscar@finca.com"
    assert "password" not in data


def test_obtener_usuario_inexistente(client: TestClient, auth_headers: dict):
    response = client.get(f"/api/v1/users/{uuid.uuid4()}", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_actualizar_usuario(client: TestClient, auth_headers: dict):
    create_resp = client.post(
        "/api/v1/users/",
        json={"email": "actualizar@finca.com", "nombre": "Nombre Original", "password": "secret123"},
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    response = client.put(
        f"/api/v1/users/{user_id}",
        json={"nombre": "Nombre Actualizado"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nombre Actualizado"
    assert data["id"] == user_id
    assert "password" not in data


def test_actualizar_usuario_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        f"/api/v1/users/{uuid.uuid4()}",
        json={"nombre": "No existe"},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_actualizar_email_duplicado(client: TestClient, auth_headers: dict):
    client.post(
        "/api/v1/users/",
        json={"email": "primero@finca.com", "nombre": "Primero", "password": "secret123"},
    )
    create_resp2 = client.post(
        "/api/v1/users/",
        json={"email": "segundo@finca.com", "nombre": "Segundo", "password": "secret123"},
    )
    assert create_resp2.status_code == 201
    user_id2 = create_resp2.json()["id"]

    response = client.put(
        f"/api/v1/users/{user_id2}",
        json={"email": "primero@finca.com"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está en uso."


def test_eliminar_usuario(client: TestClient, auth_headers: dict):
    create_resp = client.post(
        "/api/v1/users/",
        json={"email": "eliminar@finca.com", "nombre": "Para Eliminar", "password": "secret123"},
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/users/{user_id}", headers=auth_headers)

    assert response.status_code == 204

    response_get = client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_eliminar_usuario_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete(f"/api/v1/users/{uuid.uuid4()}", headers=auth_headers)

    assert response.status_code == 404


def test_endpoints_users_protegidos_sin_token(client: TestClient):
    response_list = client.get("/api/v1/users/")
    assert response_list.status_code == 401

    response_get = client.get(f"/api/v1/users/{uuid.uuid4()}")
    assert response_get.status_code == 401
