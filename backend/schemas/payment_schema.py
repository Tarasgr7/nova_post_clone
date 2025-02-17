from pydantic import BaseModel


class PaymentCreate(BaseModel):
  amount: float
  payment_method: str = "card" # card, cash, postpaid
  payment_status: str = "pending"  # paid, pending, failed