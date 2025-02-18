from .branches import branches
from .couriers import couriers
from .routes import routes
from .workers import worker
from fastapi import APIRouter
from fastapi_pagination import add_pagination

admin_api_router=APIRouter()


admin_api_router.include_router(branches.router,tags=["branches"],prefix="/branches")
admin_api_router.include_router(couriers.router,tags=["couriers"],prefix="/couriers")
admin_api_router.include_router(routes.router,tags=["routes"],prefix="/routes")
admin_api_router.include_router(worker.router,tags=["workers"], prefix="/workers")
add_pagination(admin_api_router)
