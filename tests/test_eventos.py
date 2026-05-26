from fastapi.testclient import TestClient


def test_crear_evento(client: TestClient, auth_headers: dict, animal_test: dict):
    evento_data = {
        "tipo": "vacunacion",
        "nota": "Primera vacuna del año",
        "animal_id": animal_test["id"],
    }

    response = client.post("/api/v1/eventos/", json=evento_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == "vacunacion"
    assert data["nota"] == "Primera vacuna del año"
    assert data["animal_id"] == animal_test["id"]
    assert "id" in data
    assert "fecha" in data


def test_leer_eventos_por_animal(client: TestClient, auth_headers: dict, animal_test: dict):
    animal_id = animal_test["id"]
    client.post(
        "/api/v1/eventos/",
        json={"tipo": "celo", "animal_id": animal_id},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/eventos/",
        json={"tipo": "parto", "animal_id": animal_id},
        headers=auth_headers,
    )

    response = client.get(f"/api/v1/eventos/animal/{animal_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obtener_evento_por_id(client: TestClient, auth_headers: dict, animal_test: dict):
    create_resp = client.post(
        "/api/v1/eventos/",
        json={"tipo": "monta", "animal_id": animal_test["id"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    evento_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/eventos/{evento_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == evento_id


def test_obtener_evento_inexistente(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/eventos/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Evento no encontrado"


def test_actualizar_evento(client: TestClient, auth_headers: dict, animal_test: dict):
    create_resp = client.post(
        "/api/v1/eventos/",
        json={"tipo": "vacunacion", "animal_id": animal_test["id"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    evento_id = create_resp.json()["id"]

    response = client.put(
        f"/api/v1/eventos/{evento_id}",
        json={"tipo": "enfermedad"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "enfermedad"
    assert data["id"] == evento_id


def test_actualizar_evento_inexistente(client: TestClient, auth_headers: dict):
    response = client.put(
        "/api/v1/eventos/99999",
        json={"tipo": "enfermedad"},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_eliminar_evento(client: TestClient, auth_headers: dict, animal_test: dict):
    create_resp = client.post(
        "/api/v1/eventos/",
        json={"tipo": "servicio", "animal_id": animal_test["id"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    evento_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/eventos/{evento_id}", headers=auth_headers)

    assert response.status_code == 204

    response_get = client.get(f"/api/v1/eventos/{evento_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_eliminar_evento_inexistente(client: TestClient, auth_headers: dict):
    response = client.delete("/api/v1/eventos/99999", headers=auth_headers)

    assert response.status_code == 404


def test_crear_evento_animal_inexistente(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/eventos/",
        json={"tipo": "vacunacion", "animal_id": 99999},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Animal no encontrado"


def test_crear_evento_tipo_invalido(client: TestClient, auth_headers: dict, animal_test: dict):
    response = client.post(
        "/api/v1/eventos/",
        json={"tipo": "invalido", "animal_id": animal_test["id"]},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_crear_evento_body_invalido(client: TestClient, auth_headers: dict):
    response = client.post("/api/v1/eventos/", json={}, headers=auth_headers)

    assert response.status_code == 422


def test_endpoints_evento_sin_token(client: TestClient, animal_test: dict):
    response_post = client.post(
        "/api/v1/eventos/",
        json={"tipo": "vacunacion", "animal_id": animal_test["id"]},
    )
    assert response_post.status_code == 401

    response_get = client.get(f"/api/v1/eventos/animal/{animal_test['id']}")
    assert response_get.status_code == 401
