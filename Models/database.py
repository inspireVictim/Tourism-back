from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    website = Column(String, nullable=True)
    address = Column(String, nullable=False)
    rating = Column(Float, default=0.0, nullable=False)
    contact_email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    tours = relationship("Tour", back_populates="partner", cascade="all, delete-orphan")


class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    destination = Column(String, index=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    slots_available = Column(Integer, nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    partner = relationship("Partner", back_populates="tours")
    category = relationship("Category", back_populates="tours")
    payments = relationship("Payment", back_populates="tour", cascade="all, delete-orphan")
    promo = relationship("PromotionalTour", back_populates="tour", uselist=False, cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    tours = relationship("Tour", back_populates="category")


class PromotionalTour(Base):
    __tablename__ = "promotional_tours"

    id = Column(Integer, primary_key=True, index=True)
    tour_id = Column(Integer, ForeignKey("tours.id"), unique=True, nullable=False)
    discount_percent = Column(Float, nullable=False)
    promo_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)

    tour = relationship("Tour", back_populates="promo")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)
    seats = Column(Integer, nullable=False, default=1)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="paid")
    created_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="payments")
    tour = relationship("Tour", back_populates="payments")
