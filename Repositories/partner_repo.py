from sqlalchemy.orm import Session
from Models.database import Partner  # Импорт модели из твоей папки Models
from Schemas.partner import PartnerCreate

def create_partner(db: Session, partner: PartnerCreate):
    # 1. Превращаем Pydantic-схему в SQLAlchemy-объект
    db_partner = Partner(
        name=partner.name,
        description=partner.description,
        website=str(partner.website) if partner.website else None,
        address=partner.address,
        contact_email=partner.contact_email,
        phone_number=partner.phone_number,
        is_active=True
    )
    # 2. Добавляем в сессию и сохраняем
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner) # Чтобы получить ID, сгенерированный базой
    return db_partner

def get_partners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Partner).offset(skip).limit(limit).all()