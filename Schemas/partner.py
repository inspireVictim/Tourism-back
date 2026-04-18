from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class PartnerBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    address: str  # Адрес офиса агентства
    rating: float = 0.0

class PartnerCreate(PartnerBase):
    contact_email: str
    phone_number: str

class PartnerOut(PartnerBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True