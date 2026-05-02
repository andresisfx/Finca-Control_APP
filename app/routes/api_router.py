from fastapi import APIRouter
from app.routes import user_routes, finca_routes, animal_routes, evento_routes

# Router principal que engloba todos los demás routers de la API
api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(finca_routes.router, prefix="/fincas", tags=["Fincas"])
api_router.include_router(animal_routes.router, prefix="/animales", tags=["Animales"])
api_router.include_router(evento_routes.router, prefix="/eventos", tags=["Eventos"])
