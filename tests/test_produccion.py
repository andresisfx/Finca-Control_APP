import pytest
from fastapi.testclient import TestClient


def test_crear_produccion(client: TestClient, auth_headers: dict, vendedor_test: dict):
    produccion_data = {
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    }

    response = client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["vendedor_id"] == vendedor_test["id"]
    assert float(data["litros"]) == 50.5


def test_listar_producciones_por_vendedor(client: TestClient, auth_headers: dict, vendedor_test: dict):
    produccion_data = {
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    }
    client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)

    response = client.get(f"/api/v1/produccion/vendedor/{vendedor_test['id']}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obtener_produccion_por_id(client: TestClient, auth_headers: dict, vendedor_test: dict):
    produccion_data = {
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    }
    create_response = client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)
    produccion_id = create_response.json()["id"]

    response = client.get(f"/api/v1/produccion/{produccion_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produccion_id


def test_obtener_produccion_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/produccion/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Registro de producción no encontrado"


def test_actualizar_produccion(client: TestClient, auth_headers: dict, vendedor_test: dict):
    produccion_data = {
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    }
    create_response = client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)
    produccion_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/produccion/{produccion_id}",
        json={"litros": 75.0},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert float(data["litros"]) == 75.0


def test_actualizar_produccion_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/produccion/99999",
        json={"litros": 75.0},
        headers=auth_headers
    )

    assert response.status_code == 404


def test_eliminar_produccion(client: TestClient, auth_headers: dict, vendedor_test: dict):
    produccion_data = {
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    }
    create_response = client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)
    produccion_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/produccion/{produccion_id}", headers=auth_headers)

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/produccion/{produccion_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_eliminar_produccion_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/produccion/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_produccion_vendedor_inexistente(client: TestClient, auth_headers: dict):
    produccion_data = {
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": 99999
    }

    response = client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Vendedor no encontrado"


def test_crear_produccion_duplicada(client: TestClient, auth_headers: dict, vendedor_test: dict):
    produccion_data = {
        "fecha": "2026-03-15",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    }
    client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)

    response = client.post("/api/v1/produccion/", json=produccion_data, headers=auth_headers)

    assert response.status_code == 400
    assert "El vendedor ya tiene un registro de leche" in response.json()["detail"]


def test_actualizar_produccion_fecha_duplicada(client: TestClient, auth_headers: dict, vendedor_test: dict):
    prod1_data = {
        "fecha": "2026-03-10",
        "litros": 40.0,
        "vendedor_id": vendedor_test["id"]
    }
    prod2_data = {
        "fecha": "2026-03-11",
        "litros": 45.0,
        "vendedor_id": vendedor_test["id"]
    }
    client.post("/api/v1/produccion/", json=prod1_data, headers=auth_headers)
    create_response = client.post("/api/v1/produccion/", json=prod2_data, headers=auth_headers)
    prod2_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/produccion/{prod2_id}",
        json={"fecha": "2026-03-10"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El vendedor ya tiene otro registro para esta nueva fecha"


def test_crear_produccion_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/produccion/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_produccion_sin_token(client: TestClient, vendedor_test: dict):
    response_post = client.post("/api/v1/produccion/", json={
        "fecha": "2026-03-01",
        "litros": 50.5,
        "vendedor_id": vendedor_test["id"]
    })

    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/produccion/vendedor/{vendedor_test['id']}")

    assert response_get.status_code == 401
