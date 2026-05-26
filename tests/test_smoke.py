import uuid
from fastapi.testclient import TestClient


def test_smoke_auth(client: TestClient):
    client.post("/api/v1/users/", json={
        "email": "smoke_auth@finca.com",
        "nombre": "Smoke Auth User",
        "password": "smokepassword"
    })
    response = client.post("/api/v1/auth/login/access-token", data={
        "username": "smoke_auth@finca.com",
        "password": "smokepassword"
    })
    assert response.status_code < 500


def test_smoke_fincas(client: TestClient, auth_headers: dict, finca_test: dict):
    response = client.get("/api/v1/fincas/mis-fincas", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_animales(client: TestClient, auth_headers: dict, finca_test: dict):
    response = client.get(f"/api/v1/animales/finca/{finca_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_vendedores(client: TestClient, auth_headers: dict, finca_test: dict):
    response = client.get(f"/api/v1/vendedores/finca/{finca_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_compradores(client: TestClient, auth_headers: dict, finca_test: dict):
    response = client.get(f"/api/v1/compradores/finca/{finca_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_quincenas(client: TestClient, auth_headers: dict, finca_test: dict):
    response = client.get(f"/api/v1/quincenas/finca/{finca_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_eventos(client: TestClient, auth_headers: dict, animal_test: dict):
    response = client.get(f"/api/v1/eventos/animal/{animal_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_precios(client: TestClient, auth_headers: dict, quincena_test: dict):
    response = client.get(f"/api/v1/precios/quincena/{quincena_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_produccion(client: TestClient, auth_headers: dict, vendedor_test: dict):
    response = client.get(f"/api/v1/produccion/vendedor/{vendedor_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_entregas(client: TestClient, auth_headers: dict, quincena_test: dict):
    response = client.get(f"/api/v1/entregas/quincena/{quincena_test['id']}", headers=auth_headers)
    assert response.status_code < 500


def test_smoke_users(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code < 500
