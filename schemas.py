from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    img: str
    price: float
    count: int

    class Config:
        orm_mode = True

class Item(ItemBase):
    id: int
