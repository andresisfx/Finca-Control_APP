from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes.api_router import api_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API para FincaControl",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas bajo el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de FincaControl",
        "docs": "/docs",
        "redoc": "/redoc"
    }
