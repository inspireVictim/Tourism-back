from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class PartnerTourCreate(BaseModel):
    partner_id: int
    category_id: int
    title: str
    description: str
    price: float = Field(gt=0)
    destination: str
    start_date: datetime
    end_date: datetime
    slots_available: int = Field(gt=0)


class PromotionalTourCreate(BaseModel):
    partner_id: int
    tour_id: int
    discount_percent: float = Field(gt=0, le=90)
    expires_at: Optional[datetime] = None


class PromotionalTourOut(BaseModel):
    id: int
    tour_id: int
    discount_percent: float
    promo_price: float
    is_active: bool
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TourMarketplaceOut(BaseModel):
    id: int
    title: str
    description: str
    destination: str
    price: float
    category: Optional[str] = None
    partner_name: str
    slots_available: int
    promo_price: Optional[float] = None
    discount_percent: Optional[float] = None


class PurchaseCreate(BaseModel):
    user_id: int
    tour_id: int
    seats: int = Field(default=1, gt=0)


class PaymentOut(BaseModel):
    id: int
    user_id: int
    tour_id: int
    seats: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
