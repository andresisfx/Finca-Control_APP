import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.db.session import get_db
from app.models.base import Base

# 1. Configurar Base de Datos SQLite temporal en memoria para los tests
# Esta base de datos es 100% independiente de tu PostgreSQL y se borra al terminar
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    #Permite la concurrencia, ya que por defecto, la conexión a la base de datos solo puede ser usada por el mismo hilo (thread) que la creó.
    connect_args={"check_same_thread": False},
    #No crea varias conexiones, solo una para todo el test.
    poolclass=StaticPool,
)

#crea una “fábrica de sesiones” de SQLAlchemy ORM

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#crea una sesión por test.


@pytest.fixture(scope="function")
def db_session():
    """
    Crea una nueva base de datos limpia para CADA test.
    Equivalente a beforeEach() en Jest.
    """
    # “Crea todas las tablas usando este engine”.
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()

    # yiels significa “usa esta sesión de DB mientras corre el test”.
    # cuando acabe el test ejecuta el finally
    try:
        yield db
    finally:
        db.close()
        # Borra las tablas al terminar el test (limpieza)
        # metadata guarda informacion de tablas relaciones, columnas y constraints.
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture del Cliente HTTP (Equivalente a supertest en Jest).
    Sobrescribe la dependencia de Base de Datos para que la API use la SQLite temporal en lugar de Postgres.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    #“Cuando FastAPI intente usar get_db, usa override_get_db en su lugar”
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def auth_headers(client: TestClient):
    """
    Crea un usuario, hace login y devuelve los headers de autorización
    listos para ser inyectados en las peticiones a rutas protegidas.
    """
    client.post("/api/v1/users/", json={
        "email": "granjero_auth@finca.com",
        "nombre": "Granjero Autenticado",
        "password": "testpassword"
    })

    response = client.post("/api/v1/auth/login/access-token", data={
        "username": "granjero_auth@finca.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def finca_test(client: TestClient, auth_headers: dict):
    """
    Crea una Finca de pruebas asociada al usuario autenticado
    y devuelve los datos de la Finca (incluyendo su ID).
    Depende de auth_headers para tener permisos.
    """
    import uuid
    finca_data = {
        "nombre": "Finca Base Tests",
        "usuario_id": str(uuid.uuid4()) # El servidor ignora este valor y usa el ID del usuario autenticado (requerido por el schema Pydantic)
    }

    response = client.post("/api/v1/fincas/", json=finca_data, headers=auth_headers)
    assert response.status_code == 201, "Error creando la finca base para los tests"

    return response.json()


@pytest.fixture(scope="function")
def animal_test(client: TestClient, auth_headers: dict, finca_test: dict):
    """Animal base reutilizable para tests que requieren un animal existente."""
    data = {"codigo": "ANIMAL-BASE", "nombre": "Animal Base Tests", "finca_id": finca_test["id"]}
    response = client.post("/api/v1/animales/", json=data, headers=auth_headers)
    assert response.status_code == 201, "Error creando el animal base para los tests"
    return response.json()

@pytest.fixture(scope="function")
def vendedor_test(client: TestClient, auth_headers: dict, finca_test: dict):
    """Vendedor base reutilizable para tests que requieren un vendedor existente."""
    data = {"nombre": "Vendedor Base Tests", "telefono": "3001234567", "finca_id": finca_test["id"]}
    response = client.post("/api/v1/vendedores/", json=data, headers=auth_headers)
    assert response.status_code == 201, "Error creando el vendedor base para los tests"
    return response.json()

@pytest.fixture(scope="function")
def comprador_test(client: TestClient, auth_headers: dict, finca_test: dict):
    """Comprador base reutilizable para tests que requieren un comprador existente."""
    data = {"nombre": "Comprador Base Tests", "finca_id": finca_test["id"]}
    response = client.post("/api/v1/compradores/", json=data, headers=auth_headers)
    assert response.status_code == 201, "Error creando el comprador base para los tests"
    return response.json()

@pytest.fixture(scope="function")
def quincena_test(client: TestClient, auth_headers: dict, finca_test: dict):
    """Quincena base reutilizable para tests que requieren una quincena existente."""
    data = {"fecha_inicio": "2026-01-01", "fecha_fin": "2026-01-15", "finca_id": finca_test["id"]}
    response = client.post("/api/v1/quincenas/", json=data, headers=auth_headers)
    assert response.status_code == 201, "Error creando la quincena base para los tests"
    return response.json()
