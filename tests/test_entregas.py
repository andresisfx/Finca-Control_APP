import pytest
from fastapi.testclient import TestClient


def test_crear_entrega(client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": comprador_test["id"],
        "quincena_id": quincena_test["id"]
    }

    response = client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["comprador_id"] == comprador_test["id"]
    assert data["quincena_id"] == quincena_test["id"]
    assert float(data["litros"]) == 300.0


def test_listar_entregas_por_quincena(client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": comprador_test["id"],
        "quincena_id": quincena_test["id"]
    }
    client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)

    response = client.get(f"/api/v1/entregas/quincena/{quincena_test['id']}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obtener_entrega_por_id(client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": comprador_test["id"],
        "quincena_id": quincena_test["id"]
    }
    create_response = client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)
    entrega_id = create_response.json()["id"]

    response = client.get(f"/api/v1/entregas/{entrega_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == entrega_id


def test_obtener_entrega_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/entregas/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Entrega no encontrada"


def test_actualizar_entrega(client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": comprador_test["id"],
        "quincena_id": quincena_test["id"]
    }
    create_response = client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)
    entrega_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/entregas/{entrega_id}",
        json={"litros": 500.0},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert float(data["litros"]) == 500.0


def test_actualizar_entrega_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/entregas/99999",
        json={"litros": 500.0},
        headers=auth_headers
    )

    assert response.status_code == 404


def test_eliminar_entrega(client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": comprador_test["id"],
        "quincena_id": quincena_test["id"]
    }
    create_response = client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)
    entrega_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/entregas/{entrega_id}", headers=auth_headers)

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/entregas/{entrega_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_eliminar_entrega_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/entregas/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_entrega_comprador_inexistente(client: TestClient, auth_headers: dict, quincena_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": 99999,
        "quincena_id": quincena_test["id"]
    }

    response = client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Comprador no encontrado"


def test_crear_entrega_quincena_inexistente(client: TestClient, auth_headers: dict, comprador_test: dict):
    entrega_data = {
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": comprador_test["id"],
        "quincena_id": 99999
    }

    response = client.post("/api/v1/entregas/", json=entrega_data, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Quincena no encontrada"


def test_crear_entrega_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/entregas/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_entrega_sin_token(client: TestClient, quincena_test: dict):
    response_post = client.post("/api/v1/entregas/", json={
        "fecha": "2026-01-05",
        "litros": 300.0,
        "comprador_id": 1,
        "quincena_id": quincena_test["id"]
    })

    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/entregas/quincena/{quincena_test['id']}")

    assert response_get.status_code == 401
