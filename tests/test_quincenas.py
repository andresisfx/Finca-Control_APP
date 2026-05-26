import uuid
from fastapi.testclient import TestClient


def test_crear_quincena(client: TestClient, auth_headers: dict, finca_test: dict):
    quincena_data = {
        "fecha_inicio": "2026-02-01",
        "fecha_fin": "2026-02-15",
        "finca_id": finca_test["id"],
    }

    response = client.post("/api/v1/quincenas/", json=quincena_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["fecha_inicio"] == "2026-02-01"
    assert data["fecha_fin"] == "2026-02-15"
    assert data["finca_id"] == finca_test["id"]
    assert "id" in data


def test_leer_quincenas_por_finca(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    client.post(
        "/api/v1/quincenas/",
        json={"fecha_inicio": "2026-03-01", "fecha_fin": "2026-03-15", "finca_id": finca_id},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/quincenas/",
        json={"fecha_inicio": "2026-03-16", "fecha_fin": "2026-03-31", "finca_id": finca_id},
        headers=auth_headers,
    )

    response = client.get(f"/api/v1/quincenas/finca/{finca_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obtener_quincena_por_id(client: TestClient, auth_headers: dict, quincena_test: dict):
    quincena_id = quincena_test["id"]

    response = client.get(f"/api/v1/quincenas/{quincena_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == quincena_id


def test_obtener_quincena_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/quincenas/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Quincena no encontrada"


def test_actualizar_quincena(client: TestClient, auth_headers: dict, quincena_test: dict):
    quincena_id = quincena_test["id"]

    response = client.put(
        f"/api/v1/quincenas/{quincena_id}",
        json={"fecha_fin": "2026-01-20"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fecha_fin"] == "2026-01-20"
    assert data["id"] == quincena_id


def test_actualizar_quincena_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/quincenas/99999",
        json={"fecha_fin": "2026-01-20"},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_eliminar_quincena(client: TestClient, auth_headers: dict, finca_test: dict):
    create_resp = client.post(
        "/api/v1/quincenas/",
        json={"fecha_inicio": "2026-04-01", "fecha_fin": "2026-04-15", "finca_id": finca_test["id"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    quincena_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/quincenas/{quincena_id}", headers=auth_headers)

    assert response.status_code == 204

    response_get = client.get(f"/api/v1/quincenas/{quincena_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_eliminar_quincena_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/quincenas/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_quincena_finca_inexistente(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/quincenas/",
        json={
            "fecha_inicio": "2026-05-01",
            "fecha_fin": "2026-05-15",
            "finca_id": str(uuid.uuid4()),
        },
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Finca no encontrada"


def test_crear_quincena_fechas_invalidas(client: TestClient, auth_headers: dict, finca_test: dict):
    response = client.post(
        "/api/v1/quincenas/",
        json={
            "fecha_inicio": "2026-05-15",
            "fecha_fin": "2026-05-01",
            "finca_id": finca_test["id"],
        },
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "La fecha de fin no puede ser anterior a la fecha de inicio"


def test_crear_quincena_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/quincenas/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_quincena_sin_token(client: TestClient, finca_test: dict):
    response_post = client.post(
        "/api/v1/quincenas/",
        json={"fecha_inicio": "2026-06-01", "fecha_fin": "2026-06-15", "finca_id": finca_test["id"]},
    )
    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/quincenas/finca/{finca_test['id']}")
    assert response_get.status_code == 401
