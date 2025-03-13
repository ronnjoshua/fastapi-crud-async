from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)