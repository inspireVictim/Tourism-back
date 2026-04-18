from sqlalchemy.orm import Session
from Repositories import tour_repo, partner_repo
from Schemas.tour import TourCreate
from fastapi import HTTPException
from Models.database import Partner

def add_tour_to_agency(db: Session, tour_data: TourCreate):
    # 1. Проверяем, существует ли агентство вообще
    agency = db.query(Partner).filter(Partner.id == tour_data.partner_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Агентство не найдено")

    # 2. Бизнес-логика: проверка дат
    if tour_data.start_date >= tour_data.end_date:
        raise HTTPException(
            status_code=400, 
            detail="Дата начала не может быть позже даты окончания"
        )

    # 3. Если всё ок — отдаем команду репозиторию на сохранение
    return tour_repo.create_tour(db, tour_data)


def get_available_tours(db: Session, destination: str = None):
    if destination:
        return tour_repo.get_tours_by_destination(db, destination)
    return tour_repo.get_all_tours(db)


def get_tours_by_partner(db: Session, partner_id: int):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Агентство не найдено")
    return tour_repo.get_tours_by_partner(db, partner_id)

