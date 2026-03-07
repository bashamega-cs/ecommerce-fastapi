from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from database import Base

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class LoginBase(BaseModel):
    email:str
    password:str
  
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed = Column(String, unique=True, index=False)

    cart = relationship("Cart", back_populates="user")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    img = Column(String)
    price = Column(Float)
    count = Column(Integer)
    carts = relationship("Cart", back_populates="item")

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="cart")
    item = relationship("Item", back_populates="carts")