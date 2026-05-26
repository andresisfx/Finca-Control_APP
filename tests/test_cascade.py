import uuid
from fastapi.testclient import TestClient


def test_cascade_finca_elimina_animales(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    animal_resp = client.post("/api/v1/animales/", json={
        "codigo": "CASCADE-A",
        "finca_id": finca_id
    }, headers=auth_headers)
    assert animal_resp.status_code == 201
    animal_id = animal_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/animales/{animal_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_finca_elimina_eventos_via_animal(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    animal_resp = client.post("/api/v1/animales/", json={
        "codigo": "CASCADE-B",
        "finca_id": finca_id
    }, headers=auth_headers)
    assert animal_resp.status_code == 201
    animal_id = animal_resp.json()["id"]

    evento_resp = client.post("/api/v1/eventos/", json={
        "tipo": "vacunacion",
        "animal_id": animal_id
    }, headers=auth_headers)
    assert evento_resp.status_code == 201
    evento_id = evento_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/eventos/{evento_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_finca_elimina_vendedores(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    vendedor_resp = client.post("/api/v1/vendedores/", json={
        "nombre": "Vendedor Cascade",
        "finca_id": finca_id
    }, headers=auth_headers)
    assert vendedor_resp.status_code == 201
    vendedor_id = vendedor_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/vendedores/{vendedor_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_finca_elimina_producciones_via_vendedor(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    vendedor_resp = client.post("/api/v1/vendedores/", json={
        "nombre": "Vendedor Cascade Prod",
        "finca_id": finca_id
    }, headers=auth_headers)
    assert vendedor_resp.status_code == 201
    vendedor_id = vendedor_resp.json()["id"]

    prod_resp = client.post("/api/v1/produccion/", json={
        "fecha": "2026-06-01",
        "litros": 10.0,
        "vendedor_id": vendedor_id
    }, headers=auth_headers)
    assert prod_resp.status_code == 201
    prod_id = prod_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/produccion/{prod_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_finca_elimina_compradores(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    comprador_resp = client.post("/api/v1/compradores/", json={
        "nombre": "Comprador Cascade",
        "finca_id": finca_id
    }, headers=auth_headers)
    assert comprador_resp.status_code == 201
    comprador_id = comprador_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/compradores/{comprador_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_finca_elimina_quincenas(client: TestClient, auth_headers: dict, finca_test: dict):
    finca_id = finca_test["id"]
    quincena_resp = client.post("/api/v1/quincenas/", json={
        "fecha_inicio": "2026-06-01",
        "fecha_fin": "2026-06-15",
        "finca_id": finca_id
    }, headers=auth_headers)
    assert quincena_resp.status_code == 201
    quincena_id = quincena_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/fincas/{finca_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/quincenas/{quincena_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_animal_elimina_eventos(client: TestClient, auth_headers: dict, animal_test: dict):
    animal_id = animal_test["id"]
    evento_resp = client.post("/api/v1/eventos/", json={
        "tipo": "vacunacion",
        "animal_id": animal_id
    }, headers=auth_headers)
    assert evento_resp.status_code == 201
    evento_id = evento_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/animales/{animal_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/eventos/{evento_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_vendedor_elimina_producciones(client: TestClient, auth_headers: dict, vendedor_test: dict):
    vendedor_id = vendedor_test["id"]
    prod_resp = client.post("/api/v1/produccion/", json={
        "fecha": "2026-06-01",
        "litros": 10.0,
        "vendedor_id": vendedor_id
    }, headers=auth_headers)
    assert prod_resp.status_code == 201
    prod_id = prod_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/vendedores/{vendedor_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/produccion/{prod_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_comprador_elimina_entregas(
    client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict
):
    comprador_id = comprador_test["id"]
    quincena_id = quincena_test["id"]
    entrega_resp = client.post("/api/v1/entregas/", json={
        "fecha": "2026-06-05",
        "litros": 100.0,
        "comprador_id": comprador_id,
        "quincena_id": quincena_id
    }, headers=auth_headers)
    assert entrega_resp.status_code == 201
    entrega_id = entrega_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/compradores/{comprador_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/entregas/{entrega_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_quincena_elimina_precios(client: TestClient, auth_headers: dict, quincena_test: dict):
    quincena_id = quincena_test["id"]
    precio_resp = client.post("/api/v1/precios/", json={
        "precio_compra": 1500.00,
        "precio_venta": 2000.00,
        "quincena_id": quincena_id
    }, headers=auth_headers)
    assert precio_resp.status_code == 201
    precio_id = precio_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/quincenas/{quincena_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/precios/{precio_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cascade_quincena_elimina_entregas(
    client: TestClient, auth_headers: dict, comprador_test: dict, quincena_test: dict
):
    comprador_id = comprador_test["id"]
    quincena_id = quincena_test["id"]
    entrega_resp = client.post("/api/v1/entregas/", json={
        "fecha": "2026-06-05",
        "litros": 100.0,
        "comprador_id": comprador_id,
        "quincena_id": quincena_id
    }, headers=auth_headers)
    assert entrega_resp.status_code == 201
    entrega_id = entrega_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/quincenas/{quincena_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    response = client.get(f"/api/v1/entregas/{entrega_id}", headers=auth_headers)
    assert response.status_code == 404
