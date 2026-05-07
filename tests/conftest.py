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
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Crea una nueva base de datos limpia para CADA test.
    Equivalente a beforeEach() en Jest.
    """
    # Crea las tablas
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Borra las tablas al terminar el test (limpieza)
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture del Cliente HTTP (Equivalente a supertest en Jest).
    Sobrescribe la dependencia de Base de Datos para que la API
    use la SQLite temporal en lugar de Postgres.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def auth_headers(client: TestClient):
    """
    Crea un usuario, hace login y devuelve los headers de autorización
    listos para ser inyectados en las peticiones a rutas protegidas.
    """
    # 1. Crear el usuario
    client.post("/api/v1/users/", json={
        "email": "granjero_auth@finca.com",
        "nombre": "Granjero Autenticado",
        "password": "testpassword"
    })
    
    # 2. Hacer login
    response = client.post("/api/v1/auth/login/access-token", data={
        "username": "granjero_auth@finca.com",
        "password": "testpassword"
    })
    
    token = response.json()["access_token"]
    
    # 3. Retornar el header Bearer
    return {"Authorization": f"Bearer {token}"}

