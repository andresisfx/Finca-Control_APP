from fastapi import APIRouter, Depends
from app.routes import (
    user_routes, finca_routes, animal_routes, evento_routes, 
    vendedor_routes, produccion_routes, comprador_routes, 
    quincena_routes, precio_leche_routes, entrega_routes, auth_routes
)
from app.api.deps import get_current_user

# Router principal que engloba todos los demás routers de la API
api_router = APIRouter()

# 1. Router Público (Rutas que NO requieren Token)
api_router_public = APIRouter()
api_router_public.include_router(auth_routes.router, prefix="/auth", tags=["Autenticación"])
api_router_public.include_router(user_routes.router, prefix="/users", tags=["Usuarios"])

# 2. Router Protegido (TODAS las rutas aquí exigirán Token JWT)
api_router_protected = APIRouter(
    dependencies=[Depends(get_current_user)]
)
api_router_protected.include_router(finca_routes.router, prefix="/fincas", tags=["Fincas"])
api_router_protected.include_router(animal_routes.router, prefix="/animales", tags=["Animales"])
api_router_protected.include_router(evento_routes.router, prefix="/eventos", tags=["Eventos"])
api_router_protected.include_router(vendedor_routes.router, prefix="/vendedores", tags=["Vendedores"])
api_router_protected.include_router(produccion_routes.router, prefix="/produccion", tags=["Produccion Diaria"])
api_router_protected.include_router(comprador_routes.router, prefix="/compradores", tags=["Compradores"])
api_router_protected.include_router(quincena_routes.router, prefix="/quincenas", tags=["Quincenas"])
api_router_protected.include_router(precio_leche_routes.router, prefix="/precios", tags=["Precios de Leche"])
api_router_protected.include_router(entrega_routes.router, prefix="/entregas", tags=["Entregas"])

# Finalmente agregamos los dos sub-routers al router principal exportado
api_router.include_router(api_router_public)
api_router.include_router(api_router_protected)
