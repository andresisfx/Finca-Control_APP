import pytest
import uuid
from fastapi.testclient import TestClient

def test_crear_finca_sin_token(client: TestClient):
    """
    Debe fallar (401) porque el usuario no envía el JWT en los headers.
    """
    finca_data = {
        "nombre": "Finca Intrusa",
        "usuario_id": str(uuid.uuid4())
    }
    
    response = client.post("/api/v1/fincas/", json=finca_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_crear_finca_con_token(client: TestClient, auth_headers: dict):
    """
    Debe crear la finca exitosamente usando el token inyectado
    y la respuesta debe contener id, nombre y usuario_id.
    """
    finca_data = {
        "nombre": "Finca La Esperanza",
        "usuario_id": str(uuid.uuid4())
    }
    
    # Aquí es donde inyectamos los headers que nos dio nuestro fixture
    response = client.post("/api/v1/fincas/", json=finca_data, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Finca La Esperanza"
    assert "id" in data
    assert "usuario_id" in data

def test_leer_mis_fincas(client: TestClient, auth_headers: dict):
    """
    Debe devolver una lista con las fincas que le pertenecen al usuario.
    """
    # 1. Creamos una finca primero para asegurarnos de que la lista no esté vacía
    finca_data = {
        "nombre": "Finca Los Pinos",
        "usuario_id": str(uuid.uuid4())
    }
    client.post("/api/v1/fincas/", json=finca_data, headers=auth_headers)
    
    # 2. Leemos la lista de fincas del usuario
    response = client.get("/api/v1/fincas/mis-fincas", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()

    # Sabemos que la respuesta debe ser una lista (Array) y tener al menos un elemento
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["nombre"] == "Finca Los Pinos"


def test_obtener_finca_por_id(client: TestClient, auth_headers: dict, finca_test: dict):
    # Act
    response = client.get(f"/api/v1/fincas/{finca_test['id']}", headers=auth_headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == finca_test["id"]
    assert data["nombre"] == finca_test["nombre"]


def test_obtener_finca_inexistente(client: TestClient, auth_headers: dict):
    # Act
    response = client.get(f"/api/v1/fincas/{uuid.uuid4()}", headers=auth_headers)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Finca no encontrada"


def test_actualizar_finca(client: TestClient, auth_headers: dict, finca_test: dict):
    # Act
    response = client.put(
        f"/api/v1/fincas/{finca_test['id']}",
        json={"nombre": "Nombre Actualizado"},
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nombre Actualizado"
    assert data["id"] == finca_test["id"]


def test_actualizar_finca_inexistente(client: TestClient, auth_headers: dict):
    # Act
    response = client.put(
        f"/api/v1/fincas/{uuid.uuid4()}",
        json={"nombre": "X"},
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Finca no encontrada"


def test_eliminar_finca(client: TestClient, auth_headers: dict, finca_test: dict):
    # Arrange
    finca_id = finca_test["id"]

    # Act
    response = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)

    # Assert
    assert response.status_code == 204

    # Verificar que ya no existe
    response_get = client.get(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert response_get.status_code == 404


def test_endpoints_finca_sin_token(client: TestClient):
    # GET /api/v1/fincas/mis-fincas
    response = client.get("/api/v1/fincas/mis-fincas")
    assert response.status_code == 401

    # POST /api/v1/fincas/
    response = client.post("/api/v1/fincas/", json={"nombre": "X", "usuario_id": str(uuid.uuid4())})
    assert response.status_code == 401

    # GET /api/v1/fincas/{id}
    response = client.get(f"/api/v1/fincas/{uuid.uuid4()}")
    assert response.status_code == 401

