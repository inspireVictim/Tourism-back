from sqlalchemy.orm import Session
from Models.database import Tour
from Schemas.tour import TourCreate

def create_tour(db: Session, tour: TourCreate):
    db_tour = Tour(**tour.model_dump()) # Короткий способ передать все поля
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour

def get_tours_by_partner(db: Session, partner_id: int):
    return db.query(Tour).filter(Tour.partner_id == partner_id).all()