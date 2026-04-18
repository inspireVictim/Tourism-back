from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

class PartnerBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    address: str  # Адрес офиса агентства
    rating: float = 0.0

class PartnerCreate(PartnerBase):
    contact_email: EmailStr
    phone_number: str
    password: str


class PartnerLogin(BaseModel):
    contact_email: EmailStr
    password: str

class PartnerOut(PartnerBase):
    id: int
    contact_email: EmailStr
    phone_number: str
    is_active: bool
    
    class Config:
        from_attributes = True