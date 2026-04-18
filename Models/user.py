from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    FullName = Column(String)
    email = Column(String, unique=True)
    age = Column(Integer)
    hash = Column(String)