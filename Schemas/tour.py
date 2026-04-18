from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TourBase(BaseModel):
    title: str
    description: str
    price: float
    destination: str # Куда едем
    start_date: datetime
    end_date: datetime
    slots_available: int # Сколько мест осталось

class TourCreate(TourBase):
    partner_id: int # ID агентства, которое размещает тур

class TourOut(TourBase):
    id: int
    partner_id: int

    class Config:
        from_attributes = True