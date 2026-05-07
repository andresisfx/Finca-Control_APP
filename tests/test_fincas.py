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
    Debe crear la finca exitosamente usando el token inyectado.
    También mostramos un print() para simular screen.debug()
    """
    finca_data = {
        "nombre": "Finca La Esperanza",
        "usuario_id": str(uuid.uuid4())
    }
    
    # Aquí es donde inyectamos los headers que nos dio nuestro fixture
    response = client.post("/api/v1/fincas/", json=finca_data, headers=auth_headers)
    
    # Hacemos "screen.debug()"
    print("\n--- DATA DEVUELTA POR LA API (test_crear_finca) ---")
    print(response.json())
    print("---------------------------------------------------\n")
    
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
    
    # Hacemos "screen.debug()"
    print("\n--- MIS FINCAS DEVUELTAS POR LA API ---")
    print(data)
    print("----------------------------------------\n")
    
    # Sabemos que la respuesta debe ser una lista (Array) y tener al menos un elemento
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["nombre"] == "Finca Los Pinos"

