from sqlalchemy import Column, Float, Integer, String
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
    id = Column[int](Integer, primary_key=True, index=True)
    name = Column[str](String, index=True)
    email = Column[str](String, unique=True, index=True)
    hashed = Column[str](String, unique=True, index=False)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    img = Column(String)
    price = Column(Float)
    count = Column(Integer)
