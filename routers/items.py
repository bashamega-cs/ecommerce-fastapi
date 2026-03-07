from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import database

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/", response_model=List[schemas.Item])
def get_items(limit: int = 10, skip: int = 0, db: Session = Depends(database.get_db)):
    return db.query(models.Item).offset(skip).limit(limit).all()

@router.post('/new', response_model=schemas.Item)
def add(item: schemas.ItemBase, db: Session = Depends(database.get_db)):
    item_data = models.Item(**item.dict())
    db.add(item_data)
    db.commit()
    db.refresh(item_data)
    return item_data

@router.put('/update/{id}', response_model=schemas.Item)
def update_post(id: int, updated_item: schemas.ItemBase, db: Session = Depends(database.get_db)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")
    
    item_query.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    return item_query.first()

@router.delete("/delete/{id}")
def delete_post(id: int, db: Session = Depends(database.get_db)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")

    item_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Item deleted successfully"}

# Adding the requested /shop route
@router.get("/shop", response_model=List[schemas.Item])
def shop(db: Session = Depends(database.get_db)):
    """
    Returns all items available in the shop.
    """
    return db.query(models.Item).all()
