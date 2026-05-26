import uuid
from fastapi.testclient import TestClient


def test_crear_vendedor(client: TestClient, auth_headers: dict, finca_test: dict):
    vendedor_data = {
        "nombre": "Vendedor Nuevo",
        "telefono": "3109876543",
        "finca_id": finca_test["id"],
    }

    response = client.post("/api/v1/vendedores/", json=vendedor_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Vendedor Nuevo"
    assert data["finca_id"] == finca_test["id"]
    assert "id" in data


def test_leer_vendedores_por_finca(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    client.post(
        "/api/v1/vendedores/",
        json={"nombre": "Vendedor Lista 1", "finca_id": finca_id},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/vendedores/",
        json={"nombre": "Vendedor Lista 2", "finca_id": finca_id},
        headers=auth_headers,
    )

    response = client.get(f"/api/v1/vendedores/finca/{finca_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(v["finca_id"] == finca_id for v in data)


def test_obtener_vendedor_por_id(client: TestClient, auth_headers: dict, vendedor_test: dict):
    vendedor_id = vendedor_test["id"]

    response = client.get(f"/api/v1/vendedores/{vendedor_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vendedor_id


def test_obtener_vendedor_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/vendedores/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Vendedor no encontrado"


def test_actualizar_vendedor(client: TestClient, auth_headers: dict, vendedor_test: dict):
    vendedor_id = vendedor_test["id"]

    response = client.put(
        f"/api/v1/vendedores/{vendedor_id}",
        json={"nombre": "Vendedor Actualizado"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Vendedor Actualizado"
    assert data["id"] == vendedor_id


def test_actualizar_vendedor_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/vendedores/99999",
        json={"nombre": "No existe"},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_eliminar_vendedor(client: TestClient, auth_headers: dict, finca_test: dict):
    create_resp = client.post(
        "/api/v1/vendedores/",
        json={"nombre": "Vendedor a Eliminar", "finca_id": finca_test["id"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    vendedor_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/vendedores/{vendedor_id}", headers=auth_headers)

    assert response.status_code == 204

    response_get = client.get(f"/api/v1/vendedores/{vendedor_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_eliminar_vendedor_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/vendedores/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_vendedor_finca_inexistente(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/vendedores/",
        json={"nombre": "Vendedor Sin Finca", "finca_id": str(uuid.uuid4())},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Finca no encontrada"


def test_crear_vendedor_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/vendedores/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_vendedor_sin_token(client: TestClient, finca_test: dict):
    response_post = client.post(
        "/api/v1/vendedores/",
        json={"nombre": "Sin Token", "finca_id": finca_test["id"]},
    )
    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/vendedores/finca/{finca_test['id']}")
    assert response_get.status_code == 401
