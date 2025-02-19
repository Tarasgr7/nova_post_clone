from .admin import api
from .auth_routes import router as auth_router
from .courier_endpoints import router as courier_router
from .user_endpoints import router as user_router
from .worker_endpoints import router as worker_router
from .shipment_routes import router as shipment_router
from fastapi import APIRouter
from fastapi_pagination import add_pagination

api_router= APIRouter()

api_router.include_router(api.admin_api_router, tags=["admin"], prefix="/api/v1/admin")
api_router.include_router(auth_router, tags=["auth_endpoints"], prefix="/api/v1/auth")
api_router.include_router(courier_router, tags=["courier_endpoints"], prefix="/api/v1/courier")
api_router.include_router(user_router, tags=["users_endpoints"], prefix="/api/v1/users")
api_router.include_router(worker_router, tags=["worker_endpoints"], prefix="/api/v1/worker")
api_router.include_router(shipment_router, tags=["shipment_endpoints"], prefix="/api/v1/shipment")
add_pagination(api_router)

