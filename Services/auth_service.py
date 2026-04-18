from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Core.security import hash_password, verify_password
from Models.database import Partner, User
from Schemas.partner import PartnerCreate
from Schemas.user import UserCreate


def register_user(db: Session, data: UserCreate) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    db_user = User(
        full_name=data.full_name,
        email=data.email,
        age=data.age,
        password_hash=hash_password(data.password),
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return user


def register_partner(db: Session, data: PartnerCreate) -> Partner:
    existing = db.query(Partner).filter(Partner.contact_email == data.contact_email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Partner with this email already exists",
        )

    db_partner = Partner(
        name=data.name,
        description=data.description,
        website=str(data.website) if data.website else None,
        address=data.address,
        rating=data.rating,
        contact_email=data.contact_email,
        phone_number=data.phone_number,
        password_hash=hash_password(data.password),
        is_active=True,
    )
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner


def login_partner(db: Session, email: str, password: str) -> Partner:
    partner = db.query(Partner).filter(Partner.contact_email == email).first()
    if not partner or not verify_password(password, partner.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return partner
