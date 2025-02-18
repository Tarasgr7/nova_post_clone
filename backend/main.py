from fastapi import FastAPI
from .endpoints.auth_routes import router as auth_router
from .endpoints.shipment_routes import router as shipment_routes
from .endpoints.user_endpoints import router as users_routes
from .endpoints.payment_routes import router as payment_routes
from .endpoints.worker_endpoints import router as worker_endpoints_routes
from.endpoints.courier_endpoints import router as courier_endpoints_routes
from .endpoints import api
from .dependencies import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(auth_router)
# app.include_router(users_routes)
# app.include_router(shipment_routes)
# app.include_router(payment_routes)
# app.include_router(worker_endpoints_routes)
# app.include_router(courier_endpoints_routes)
app.include_router(api.api_router,tags=['api/v1'],prefix='/api/v1')