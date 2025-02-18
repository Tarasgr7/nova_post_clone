from .admin import api
from .auth_routes import router as auth_router
from .courier_endpoints import router as courier_router
from .user_endpoints import router as user_router
from .worker_endpoints import router as worker_router
from fastapi import APIRouter
from fastapi_pagination import add_pagination

api_router= APIRouter()

api_router.include_router(api.admin_api_router, tags=["admin"], prefix="/admin")
api_router.include_router(auth_router, tags=["auth"], prefix="/auth")
api_router.include_router(courier_router, tags=["courier"], prefix="/courier")
api_router.include_router(user_router, tags=["users"], prefix="/users")
api_router.include_router(worker_router, tags=["worker"], prefix="/worker")
add_pagination(api_router)

