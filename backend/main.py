from fastapi import FastAPI
from .routes.auth_routes import router as auth_router
from .routes.branch_routes import router as branch_routes
from .routes.shipment_routes import router as shipment_routes
from .routes.users_routes import router as users_routes
from .routes.payment_routes import router as payment_routes
from.routes.courier_routes import router as courier_routes
from.routes.vehicle_routes import router as vehicle_routes
from .dependencies import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(branch_routes)
app.include_router(shipment_routes)
app.include_router(users_routes)
app.include_router(payment_routes)
app.include_router(courier_routes)
app.include_router(vehicle_routes)
