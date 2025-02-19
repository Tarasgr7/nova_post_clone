from fastapi import status,HTTPException
from ..models.shipment_model import Shipment
from ..models.route_model import Route 

def check_branch(route,shipment):
  if route.branch_from != shipment.branch_from:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Поточна локація посилки ��з номером : {shipment.tracking_number} має бути відповідною до пошти замовлення")
  if route.branch_to != shipment.branch_to:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Цінцева локація посилки ��з номером : {shipment.tracking_number} має бути відповідною до пошти на яку відправлялось замовлення")