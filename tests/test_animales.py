import uuid
import pytest
from fastapi.testclient import TestClient

def test_crear_animal(client: TestClient, auth_headers: dict, finca_test: dict):
    """
    Prueba la creación de un Animal asegurándose de que esté enlazado a la Finca.
    """
    finca_id = finca_test["id"]
    
    animal_data = {
        "codigo": "VACA-001",
        "nombre": "Lola",
        "finca_id": finca_id
    }
    
    response = client.post("/api/v1/animales/", json=animal_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["codigo"] == "VACA-001"
    assert data["nombre"] == "Lola"
    assert data["finca_id"] == finca_id
    assert "id" in data

def test_leer_animales_por_finca(client: TestClient, auth_headers: dict, finca_test: dict):
    """
    Debe listar todos los animales asociados a una finca específica.
    """
    finca_id = finca_test["id"]
    
    # Creamos un par de animales
    animal_data_1 = {"codigo": "VACA-002", "nombre": "Margarita", "finca_id": finca_id}
    animal_data_2 = {"codigo": "VACA-003", "nombre": "Pinta", "finca_id": finca_id}
    
    client.post("/api/v1/animales/", json=animal_data_1, headers=auth_headers)
    client.post("/api/v1/animales/", json=animal_data_2, headers=auth_headers)
    
    # Consultamos la lista
    response = client.get(f"/api/v1/animales/finca/{finca_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2
    # Comprobar que pertenecen a la finca correcta
    assert all(animal["finca_id"] == finca_id for animal in data)

def test_actualizar_animal(client: TestClient, auth_headers: dict, finca_test: dict):
    """
    Prueba que se pueda actualizar un animal existente.
    """
    finca_id = finca_test["id"]
    
    # Crear un animal base
    animal_data = {"codigo": "VACA-OLD", "nombre": "Vieja", "finca_id": finca_id}
    response_create = client.post("/api/v1/animales/", json=animal_data, headers=auth_headers)
    animal_id = response_create.json()["id"]
    
    # Nuevos datos
    update_data = {
        "codigo": "VACA-NEW",
        "nombre": "Renovada"
    }
    
    response_update = client.put(f"/api/v1/animales/{animal_id}", json=update_data, headers=auth_headers)
    
    assert response_update.status_code == 200
    data = response_update.json()
    
    assert data["id"] == animal_id
    assert data["codigo"] == "VACA-NEW"
    assert data["nombre"] == "Renovada"


def test_obtener_animal_por_id(client: TestClient, auth_headers: dict, finca_test: dict):
    # Arrange
    finca_id = finca_test["id"]
    create_resp = client.post(
        "/api/v1/animales/",
        json={"codigo": "GET-001", "nombre": "Recuperada", "finca_id": finca_id},
        headers=auth_headers
    )
    assert create_resp.status_code == 201
    animal_id = create_resp.json()["id"]

    # Act
    response = client.get(f"/api/v1/animales/{animal_id}", headers=auth_headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == animal_id


def test_obtener_animal_inexistente(client: TestClient, auth_headers: dict):
    # Act
    response = client.get("/api/v1/animales/99999", headers=auth_headers)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Animal no encontrado"


def test_eliminar_animal(client: TestClient, auth_headers: dict, finca_test: dict):
    # Arrange
    finca_id = finca_test["id"]
    create_resp = client.post(
        "/api/v1/animales/",
        json={"codigo": "DELETE-01", "finca_id": finca_id},
        headers=auth_headers
    )
    assert create_resp.status_code == 201
    animal_id = create_resp.json()["id"]

    # Act
    response = client.delete(f"/api/v1/animales/{animal_id}", headers=auth_headers)

    # Assert
    assert response.status_code == 204

    # Verificar que ya no existe
    response_get = client.get(f"/api/v1/animales/{animal_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_eliminar_animal_inexistente(client: TestClient, auth_headers: dict):
    # Act
    response = client.delete("/api/v1/animales/99999", headers=auth_headers)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Animal no encontrado"


def test_crear_animal_codigo_duplicado(client: TestClient, auth_headers: dict, finca_test: dict):
    # Arrange
    finca_id = finca_test["id"]
    payload = {"codigo": "DUP-001", "finca_id": finca_id}
    client.post("/api/v1/animales/", json=payload, headers=auth_headers)

    # Act: crear otro animal con el mismo codigo en la misma finca
    response = client.post("/api/v1/animales/", json=payload, headers=auth_headers)

    # Assert
    assert response.status_code == 400
    assert "DUP-001" in response.json()["detail"]


def test_crear_animal_finca_inexistente(client: TestClient, auth_headers: dict):
    # Act
    response = client.post(
        "/api/v1/animales/",
        json={"codigo": "FINCA-404", "finca_id": str(uuid.uuid4())},
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Finca no encontrada"


def test_crear_animal_body_invalido(client: TestClient, auth_headers: dict):
    # Act
    response = client.post("/api/v1/animales/", json={}, headers=auth_headers)

    # Assert
    assert response.status_code == 422


def test_actualizar_solo_nombre(client: TestClient, auth_headers: dict, finca_test: dict):
    # Arrange
    finca_id = finca_test["id"]
    create_resp = client.post(
        "/api/v1/animales/",
        json={"codigo": "SOLO-NOMBRE", "nombre": "Original", "finca_id": finca_id},
        headers=auth_headers
    )
    assert create_resp.status_code == 201
    animal_id = create_resp.json()["id"]

    # Act
    response = client.put(
        f"/api/v1/animales/{animal_id}",
        json={"nombre": "Actualizado"},
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Actualizado"
    assert data["codigo"] == "SOLO-NOMBRE"


def test_actualizar_animal_inexistente(client: TestClient, auth_headers: dict):
    # Act
    response = client.put(
        "/api/v1/animales/99999",
        json={"nombre": "X"},
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Animal no encontrado"
