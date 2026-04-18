import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import text

from Core.env_loader import load_env_file
from db.database import engine, get_db, Base

from Schemas.marketplace import (
    CategoryCreate,
    CategoryOut,
    PartnerTourCreate,
    PaymentOut,
    PromotionalTourCreate,
    PromotionalTourOut,
    PurchaseCreate,
    TourMarketplaceOut,
)
from Schemas.ai_chat import AIConsultRequest, AIConsultResponse
from Schemas.partner import PartnerCreate, PartnerLogin, PartnerOut
from Schemas.tour import TourOut, TourCreate
from Schemas.user import UserCreate, UserLogin, UserOut

from Services import (
    ai_consult_service,
    auth_service,
    marketplace_service,
    partner_service,
    tour_service,
)

from Models import database as models  # noqa: F401

load_env_file()

Base.metadata.create_all(bind=engine)


def run_lightweight_migrations() -> None:
    # Keep older sqlite schema compatible without Alembic.
    with engine.begin() as conn:
        tour_columns = conn.execute(text("PRAGMA table_info(tours)")).fetchall()
        existing_tour_columns = {col[1] for col in tour_columns}
        if "category_id" not in existing_tour_columns:
            conn.execute(text("ALTER TABLE tours ADD COLUMN category_id INTEGER"))


run_lightweight_migrations()

app = FastAPI(
    title="NomadAI API",
    description="Маркетплейс туров: партнеры продают, пользователи покупают",
    version="1.0.0"
)

# --- Эндпоинты для Партнеров (Турагентств) ---

@app.post("/partners/", response_model=PartnerOut, tags=["Partners"])
def register_partner(data: PartnerCreate, db: Session = Depends(get_db)):
    return auth_service.register_partner(db=db, data=data)


@app.post("/partners/login", response_model=PartnerOut, tags=["Partners"])
def login_partner(data: PartnerLogin, db: Session = Depends(get_db)):
    return auth_service.login_partner(db=db, email=data.contact_email, password=data.password)

@app.get("/partners/", response_model=List[PartnerOut], tags=["Partners"])
def list_partners(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return partner_service.get_all_partners(db=db, skip=skip, limit=limit)


# --- Эндпоинты для Пользователей ---

@app.post("/users/register", response_model=UserOut, tags=["Users"])
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db=db, data=data)


@app.post("/users/login", response_model=UserOut, tags=["Users"])
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db=db, email=data.email, password=data.password)


# --- Marketplace (продажа и покупка туров) ---

@app.post("/categories/", response_model=CategoryOut, tags=["Marketplace"])
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return marketplace_service.create_category(db=db, data=data)


@app.post("/marketplace/tours", response_model=TourOut, tags=["Marketplace"])
def partner_publish_tour(data: PartnerTourCreate, db: Session = Depends(get_db)):
    return marketplace_service.partner_create_tour(db=db, data=data)


@app.post("/marketplace/promotions", response_model=PromotionalTourOut, tags=["Marketplace"])
def set_tour_promotion(data: PromotionalTourCreate, db: Session = Depends(get_db)):
    return marketplace_service.add_or_update_promo(db=db, data=data)


@app.get("/marketplace/tours", response_model=List[TourMarketplaceOut], tags=["Marketplace"])
def list_marketplace_tours(
    category_id: Optional[int] = None,
    destination: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return marketplace_service.list_marketplace_tours(
        db=db,
        category_id=category_id,
        destination=destination,
    )


@app.post("/marketplace/purchase", response_model=PaymentOut, tags=["Marketplace"])
def purchase_tour(data: PurchaseCreate, db: Session = Depends(get_db)):
    return marketplace_service.buy_tour(db=db, data=data)


@app.get("/users/{user_id}/payments", response_model=List[PaymentOut], tags=["Marketplace"])
def user_payment_history(user_id: int, db: Session = Depends(get_db)):
    return marketplace_service.list_user_payments(db=db, user_id=user_id)


# --- AI консультации ---

@app.post("/ai/consult", response_model=AIConsultResponse, tags=["AI"])
def ai_consult(data: AIConsultRequest):
    return ai_consult_service.consult_with_ai(payload=data)


# --- Эндпоинты для Туров ---

@app.post("/tours/", response_model=TourOut, tags=["Tours"])
def add_new_tour(data: TourCreate, db: Session = Depends(get_db)):
    """
    Размещение нового тура от имени агентства.
    Включает проверку дат и существования партнера.
    """
    return tour_service.add_tour_to_agency(db=db, tour_data=data)

@app.get("/tours/", response_model=List[TourOut], tags=["Tours"])
def list_all_tours(destination: str = None, db: Session = Depends(get_db)):
    return tour_service.get_available_tours(db=db, destination=destination)

@app.get("/partners/{partner_id}/tours", response_model=List[TourOut], tags=["Tours"])
def get_tours_by_agency(partner_id: int, db: Session = Depends(get_db)):
    return tour_service.get_tours_by_partner(db=db, partner_id=partner_id)


# --- Тестовый эндпоинт ---
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to NomadAI API. Go to /docs for Swagger UI."}


if __name__ == "__main__":
    # Запуск сервера
    # host 0.0.0.0 нужен, если захочешь потестить с телефона в той же Wi-Fi сети
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)