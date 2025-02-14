import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("service")

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/delivery_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



from .models.branch_model import Branch
from .models.vehicle_model import Vehicle
from .models.courier_model import Courier
from .models.shipment_model import Shipment, ShipmentStatus
from .models.route_model import Route
from .models.payment_model import Payment
