# auth_service/schemas.py
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}  # Позволяет создавать из ORM-объекта

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"