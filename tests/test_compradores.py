import uuid
from fastapi.testclient import TestClient


def test_crear_comprador(client: TestClient, auth_headers: dict, finca_test: dict):
    comprador_data = {
        "nombre": "Comprador Nuevo",
        "telefono": "3201234567",
        "finca_id": finca_test["id"],
    }

    response = client.post("/api/v1/compradores/", json=comprador_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Comprador Nuevo"
    assert data["finca_id"] == finca_test["id"]
    assert "id" in data


def test_leer_compradores_por_finca(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    client.post(
        "/api/v1/compradores/",
        json={"nombre": "Comprador Lista 1", "finca_id": finca_id},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/compradores/",
        json={"nombre": "Comprador Lista 2", "finca_id": finca_id},
        headers=auth_headers,
    )

    response = client.get(f"/api/v1/compradores/finca/{finca_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(c["finca_id"] == finca_id for c in data)


def test_obtener_comprador_por_id(client: TestClient, auth_headers: dict, comprador_test: dict):
    comprador_id = comprador_test["id"]

    response = client.get(f"/api/v1/compradores/{comprador_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == comprador_id


def test_obtener_comprador_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/compradores/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Comprador no encontrado"


def test_actualizar_comprador(client: TestClient, auth_headers: dict, comprador_test: dict):
    comprador_id = comprador_test["id"]

    response = client.put(
        f"/api/v1/compradores/{comprador_id}",
        json={"nombre": "Comprador Actualizado"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Comprador Actualizado"
    assert data["id"] == comprador_id


def test_actualizar_comprador_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/compradores/99999",
        json={"nombre": "No existe"},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_eliminar_comprador(client: TestClient, auth_headers: dict, finca_test: dict):
    create_resp = client.post(
        "/api/v1/compradores/",
        json={"nombre": "Comprador a Eliminar", "finca_id": finca_test["id"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    comprador_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/compradores/{comprador_id}", headers=auth_headers)

    assert response.status_code == 204

    response_get = client.get(f"/api/v1/compradores/{comprador_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_eliminar_comprador_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/compradores/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_comprador_finca_inexistente(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/compradores/",
        json={"nombre": "Comprador Sin Finca", "finca_id": str(uuid.uuid4())},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Finca no encontrada"


def test_crear_comprador_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/compradores/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_comprador_sin_token(client: TestClient, finca_test: dict):
    response_post = client.post(
        "/api/v1/compradores/",
        json={"nombre": "Sin Token", "finca_id": finca_test["id"]},
    )
    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/compradores/finca/{finca_test['id']}")
    assert response_get.status_code == 401
