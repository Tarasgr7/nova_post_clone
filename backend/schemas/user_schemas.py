from pydantic import BaseModel, EmailStr
from typing import Optional

from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: RoleEnum = RoleEnum.USER  # 🔥 Додаємо роль

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    role: RoleEnum

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
