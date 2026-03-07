from sqlalchemy import Column, Float, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    img = Column(String)
    price = Column(Float)
    count = Column(Integer)
