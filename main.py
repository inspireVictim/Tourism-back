import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Импорт настроек базы данных
from db.database import engine, get_db, Base

# Импорт схем (Pydantic)
from Schemas.partner import PartnerOut, PartnerCreate
from Schemas.tour import TourOut, TourCreate

# Импорт сервисов (Бизнес-логика)
from Services import partner_service, tour_service

# Импорт моделей для инициализации таблиц
from Models import database as models

# Автоматическое создание таблиц в SQLite при старте приложения
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Yess!Go Travel API",
    description="API для агрегатора туров от агентств-партнеров",
    version="1.0.0"
)

# --- Эндпоинты для Партнеров (Турагентств) ---

@app.post("/partners/", response_model=PartnerOut, tags=["Partners"])
def register_partner(data: PartnerCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового турагентства в системе.
    """
    return partner_service.create_partner(db=db, partner_data=data)

@app.get("/partners/", response_model=List[PartnerOut], tags=["Partners"])
def list_partners(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Получение списка всех зарегистрированных агентств.
    """
    return partner_service.get_all_partners(db=db, skip=skip, limit=limit)


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
    """
    Получение списка всех доступных туров (с возможностью фильтрации по направлению).
    """
    return tour_service.get_available_tours(db=db, destination=destination)

@app.get("/partners/{partner_id}/tours", response_model=List[TourOut], tags=["Tours"])
def get_tours_by_agency(partner_id: int, db: Session = Depends(get_db)):
    """
    Просмотр всех туров конкретного агентства.
    """
    return tour_service.get_tours_by_partner(db=db, partner_id=partner_id)


# --- Тестовый эндпоинт ---
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Yess!Go API. Go to /docs for Swagger UI."}


if __name__ == "__main__":
    # Запуск сервера
    # host 0.0.0.0 нужен, если захочешь потестить с телефона в той же Wi-Fi сети
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)