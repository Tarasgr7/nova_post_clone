from .branches import branches
from .couriers import couriers
from .routes import routes
from .workers import worker
from .users import users
from fastapi import APIRouter
from fastapi_pagination import add_pagination

admin_api_router=APIRouter()


admin_api_router.include_router(branches.router,tags=["admin_branches"],prefix="/branches")
admin_api_router.include_router(couriers.router,tags=["admin_couriers"],prefix="/couriers")
admin_api_router.include_router(routes.router,tags=["admin_routes"],prefix="/routes")
admin_api_router.include_router(worker.router,tags=["admin_workers"], prefix="/workers")
admin_api_router.include_router(users.router,tags=["admin_users"], prefix="/users")
add_pagination(admin_api_router)
