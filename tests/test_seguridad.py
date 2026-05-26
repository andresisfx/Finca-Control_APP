import uuid
from fastapi.testclient import TestClient


def test_seguridad_fincas_sin_token(client: TestClient):
    fake_uuid = str(uuid.uuid4())
    assert client.post("/api/v1/fincas/", json={}).status_code == 401
    assert client.get("/api/v1/fincas/mis-fincas").status_code == 401
    assert client.get(f"/api/v1/fincas/{fake_uuid}").status_code == 401
    assert client.put(f"/api/v1/fincas/{fake_uuid}", json={}).status_code == 401
    assert client.delete(f"/api/v1/fincas/{fake_uuid}").status_code == 401


def test_seguridad_animales_sin_token(client: TestClient):
    fake_uuid = str(uuid.uuid4())
    assert client.post("/api/v1/animales/", json={}).status_code == 401
    assert client.get(f"/api/v1/animales/finca/{fake_uuid}").status_code == 401
    assert client.get("/api/v1/animales/99999").status_code == 401
    assert client.put("/api/v1/animales/99999", json={}).status_code == 401
    assert client.delete("/api/v1/animales/99999").status_code == 401


def test_seguridad_eventos_sin_token(client: TestClient):
    assert client.post("/api/v1/eventos/", json={}).status_code == 401
    assert client.get("/api/v1/eventos/animal/99999").status_code == 401
    assert client.get("/api/v1/eventos/99999").status_code == 401
    assert client.put("/api/v1/eventos/99999", json={}).status_code == 401
    assert client.delete("/api/v1/eventos/99999").status_code == 401


def test_seguridad_vendedores_sin_token(client: TestClient):
    fake_uuid = str(uuid.uuid4())
    assert client.post("/api/v1/vendedores/", json={}).status_code == 401
    assert client.get(f"/api/v1/vendedores/finca/{fake_uuid}").status_code == 401
    assert client.get("/api/v1/vendedores/99999").status_code == 401
    assert client.put("/api/v1/vendedores/99999", json={}).status_code == 401
    assert client.delete("/api/v1/vendedores/99999").status_code == 401


def test_seguridad_produccion_sin_token(client: TestClient):
    assert client.post("/api/v1/produccion/", json={}).status_code == 401
    assert client.get("/api/v1/produccion/vendedor/99999").status_code == 401
    assert client.get("/api/v1/produccion/99999").status_code == 401
    assert client.put("/api/v1/produccion/99999", json={}).status_code == 401
    assert client.delete("/api/v1/produccion/99999").status_code == 401


def test_seguridad_compradores_sin_token(client: TestClient):
    fake_uuid = str(uuid.uuid4())
    assert client.post("/api/v1/compradores/", json={}).status_code == 401
    assert client.get(f"/api/v1/compradores/finca/{fake_uuid}").status_code == 401
    assert client.get("/api/v1/compradores/99999").status_code == 401
    assert client.put("/api/v1/compradores/99999", json={}).status_code == 401
    assert client.delete("/api/v1/compradores/99999").status_code == 401


def test_seguridad_quincenas_sin_token(client: TestClient):
    fake_uuid = str(uuid.uuid4())
    assert client.post("/api/v1/quincenas/", json={}).status_code == 401
    assert client.get(f"/api/v1/quincenas/finca/{fake_uuid}").status_code == 401
    assert client.get("/api/v1/quincenas/99999").status_code == 401
    assert client.put("/api/v1/quincenas/99999", json={}).status_code == 401
    assert client.delete("/api/v1/quincenas/99999").status_code == 401


def test_seguridad_precios_sin_token(client: TestClient):
    assert client.post("/api/v1/precios/", json={}).status_code == 401
    assert client.get("/api/v1/precios/quincena/99999").status_code == 401
    assert client.get("/api/v1/precios/99999").status_code == 401
    assert client.put("/api/v1/precios/99999", json={}).status_code == 401
    assert client.delete("/api/v1/precios/99999").status_code == 401


def test_seguridad_entregas_sin_token(client: TestClient):
    assert client.post("/api/v1/entregas/", json={}).status_code == 401
    assert client.get("/api/v1/entregas/quincena/99999").status_code == 401
    assert client.get("/api/v1/entregas/99999").status_code == 401
    assert client.put("/api/v1/entregas/99999", json={}).status_code == 401
    assert client.delete("/api/v1/entregas/99999").status_code == 401


def test_seguridad_users_sin_token(client: TestClient):
    fake_uuid = str(uuid.uuid4())
    assert client.get("/api/v1/users/").status_code == 401
    assert client.get(f"/api/v1/users/{fake_uuid}").status_code == 401
    assert client.put(f"/api/v1/users/{fake_uuid}", json={}).status_code == 401
    assert client.delete(f"/api/v1/users/{fake_uuid}").status_code == 401
