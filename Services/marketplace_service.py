from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.database import Category, Partner, Payment, PromotionalTour, Tour, User
from Schemas.marketplace import (
    CategoryCreate,
    PartnerTourCreate,
    PromotionalTourCreate,
    PurchaseCreate,
    TourMarketplaceOut,
)


def create_category(db: Session, data: CategoryCreate) -> Category:
    existing = db.query(Category).filter(Category.name == data.name).first()
    if existing:
        return existing

    category = Category(name=data.name, description=data.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def partner_create_tour(db: Session, data: PartnerTourCreate) -> Tour:
    partner = db.query(Partner).filter(Partner.id == data.partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Партнер не найден")

    category = db.query(Category).filter(Category.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    if data.start_date >= data.end_date:
        raise HTTPException(status_code=400, detail="Некорректные даты тура")

    tour = Tour(
        partner_id=data.partner_id,
        category_id=data.category_id,
        title=data.title,
        description=data.description,
        price=data.price,
        destination=data.destination,
        start_date=data.start_date,
        end_date=data.end_date,
        slots_available=data.slots_available,
    )
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return tour


def add_or_update_promo(db: Session, data: PromotionalTourCreate) -> PromotionalTour:
    tour = db.query(Tour).filter(Tour.id == data.tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Тур не найден")
    if tour.partner_id != data.partner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Партнер может менять только свои туры",
        )

    promo_price = round(tour.price * (1 - data.discount_percent / 100), 2)
    promo = db.query(PromotionalTour).filter(PromotionalTour.tour_id == tour.id).first()
    if promo:
        promo.discount_percent = data.discount_percent
        promo.promo_price = promo_price
        promo.expires_at = data.expires_at
        promo.is_active = True
    else:
        promo = PromotionalTour(
            tour_id=tour.id,
            discount_percent=data.discount_percent,
            promo_price=promo_price,
            expires_at=data.expires_at,
            is_active=True,
        )
        db.add(promo)

    db.commit()
    db.refresh(promo)
    return promo


def list_marketplace_tours(
    db: Session,
    category_id: Optional[int] = None,
    destination: Optional[str] = None,
):
    query = db.query(Tour).join(Partner).outerjoin(Category).outerjoin(PromotionalTour)
    if category_id:
        query = query.filter(Tour.category_id == category_id)
    if destination:
        query = query.filter(Tour.destination == destination)

    tours = query.all()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    result = []
    for tour in tours:
        promo = tour.promo
        is_promo_active = (
            promo
            and promo.is_active
            and (promo.expires_at is None or promo.expires_at >= now)
        )
        result.append(
            TourMarketplaceOut(
                id=tour.id,
                title=tour.title,
                description=tour.description,
                destination=tour.destination,
                price=tour.price,
                category=tour.category.name if tour.category else None,
                partner_name=tour.partner.name,
                slots_available=tour.slots_available,
                promo_price=promo.promo_price if is_promo_active else None,
                discount_percent=promo.discount_percent if is_promo_active else None,
            )
        )
    return result


def buy_tour(db: Session, data: PurchaseCreate) -> Payment:
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    tour = db.query(Tour).filter(Tour.id == data.tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Тур не найден")
    if tour.slots_available < data.seats:
        raise HTTPException(status_code=400, detail="Недостаточно мест")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    promo = db.query(PromotionalTour).filter(PromotionalTour.tour_id == tour.id).first()
    current_price = tour.price
    if promo and promo.is_active and (promo.expires_at is None or promo.expires_at >= now):
        current_price = promo.promo_price

    payment = Payment(
        user_id=user.id,
        tour_id=tour.id,
        seats=data.seats,
        amount=round(current_price * data.seats, 2),
        status="paid",
        created_at=now,
    )
    tour.slots_available -= data.seats

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def list_user_payments(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db.query(Payment).filter(Payment.user_id == user_id).order_by(Payment.id.desc()).all()
