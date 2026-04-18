from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username = str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active = bool

    class Config:
        from_attributes = True


        