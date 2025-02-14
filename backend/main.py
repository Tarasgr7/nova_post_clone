from fastapi import FastAPI
from .routes.auth_routes import router as auth_router
from .routes.branch_routes import router as branch_routes
from .dependencies import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(branch_routes)
