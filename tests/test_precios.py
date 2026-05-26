import pytest
from fastapi.testclient import TestClient


def test_crear_precio(client: TestClient, auth_headers: dict, quincena_test: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    }

    response = client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["quincena_id"] == quincena_test["id"]
    assert float(data["precio_compra"]) == 1500.50
    assert float(data["precio_venta"]) == 2000.00


def test_listar_precios_por_quincena(client: TestClient, auth_headers: dict, quincena_test: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    }
    client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)

    response = client.get(f"/api/v1/precios/quincena/{quincena_test['id']}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["quincena_id"] == quincena_test["id"]


def test_obtener_precio_por_id(client: TestClient, auth_headers: dict, quincena_test: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    }
    create_response = client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)
    precio_id = create_response.json()["id"]

    response = client.get(f"/api/v1/precios/{precio_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == precio_id


def test_obtener_precio_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/precios/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Precio de leche no encontrado"


def test_actualizar_precio(client: TestClient, auth_headers: dict, quincena_test: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    }
    create_response = client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)
    precio_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/precios/{precio_id}",
        json={"precio_compra": 1800.00},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert float(data["precio_compra"]) == 1800.00


def test_actualizar_precio_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/precios/99999",
        json={"precio_compra": 1800.00},
        headers=auth_headers
    )

    assert response.status_code == 404


def test_eliminar_precio(client: TestClient, auth_headers: dict, quincena_test: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    }
    create_response = client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)
    precio_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/precios/{precio_id}", headers=auth_headers)

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/precios/{precio_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_eliminar_precio_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/precios/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_precio_quincena_inexistente(client: TestClient, auth_headers: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": 99999
    }

    response = client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Quincena no encontrada"


def test_crear_precio_duplicado_por_quincena(client: TestClient, auth_headers: dict, quincena_test: dict):
    precio_data = {
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    }
    client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)

    response = client.post("/api/v1/precios/", json=precio_data, headers=auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Ya existe un registro de precio para esta quincena. Actualícelo en su lugar."


def test_crear_precio_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/precios/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_precios_sin_token(client: TestClient, quincena_test: dict):
    response_post = client.post("/api/v1/precios/", json={
        "precio_compra": 1500.50,
        "precio_venta": 2000.00,
        "quincena_id": quincena_test["id"]
    })

    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/precios/quincena/{quincena_test['id']}")

    assert response_get.status_code == 401
