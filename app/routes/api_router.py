from fastapi import APIRouter
from app.routes import (
    user_routes, finca_routes, animal_routes, evento_routes, 
    vendedor_routes, produccion_routes, comprador_routes, 
    quincena_routes, precio_leche_routes, entrega_routes
)

# Router principal que engloba todos los demás routers de la API
api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(finca_routes.router, prefix="/fincas", tags=["Fincas"])
api_router.include_router(animal_routes.router, prefix="/animales", tags=["Animales"])
api_router.include_router(evento_routes.router, prefix="/eventos", tags=["Eventos"])
api_router.include_router(vendedor_routes.router, prefix="/vendedores", tags=["Vendedores"])
api_router.include_router(produccion_routes.router, prefix="/produccion", tags=["Produccion Diaria"])
api_router.include_router(comprador_routes.router, prefix="/compradores", tags=["Compradores"])
api_router.include_router(quincena_routes.router, prefix="/quincenas", tags=["Quincenas"])
api_router.include_router(precio_leche_routes.router, prefix="/precios", tags=["Precios de Leche"])
api_router.include_router(entrega_routes.router, prefix="/entregas", tags=["Entregas"])
