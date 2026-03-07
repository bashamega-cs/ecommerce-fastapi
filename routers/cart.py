from fastapi import APIRouter, Depends, HTTPException, status
from routers.users import info
from database import get_db
from models import Item, Cart

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.get("/list")
def list_cart(db=Depends(get_db), current_user: dict = Depends(info)):
    cart_entries = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    products = []
    total = 0.0

    for entry in cart_entries:
        item = db.query(Item).filter(Item.id == entry.item_id).first()
        if item:
            product_info = {
                "id": item.id,
                "title": item.title,
                "img": item.img,
                "price": item.price,
                "quantity": entry.quantity
            }
            products.append(product_info)
            total += item.price * entry.quantity

    return {
        "products": products,
        "total": total
    }

@router.post("/add/{product}")
def add_to_cart(product: int, db=Depends(get_db), current_user: dict = Depends(info)):
    # Ensure product refers to the Item id, not User id
    item = db.query(Item).filter(Item.id == product).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")

    # Get the user id from the authenticated user
    user_id = current_user.id

    cart_entry = db.query(Cart).filter(Cart.user_id == user_id, Cart.item_id == product).first()
    if cart_entry:
        cart_entry.quantity += 1
    else:
        cart_entry = Cart(user_id=user_id, item_id=product, quantity=1)
        db.add(cart_entry)
    db.commit()
    db.refresh(cart_entry)
    return {
        "detail": "Item added to cart",
        "cart": {
            "cart_id": cart_entry.id,
            "user_id": cart_entry.user_id,
            "item_id": cart_entry.item_id,
            "quantity": cart_entry.quantity
        }
    }

@router.delete("/remove/all")
def remove_all(db=Depends(get_db), current_user:dict = Depends(info)):
    user_id = current_user.id
    cart_entries = db.query(Cart).filter(Cart.user_id == user_id)
    deleted_count = cart_entries.delete(synchronize_session=False)
    db.commit()
    return {
        "detail": f"Removed {deleted_count} items from your cart"
    }

@router.delete("/remove/{id}")
def remove_from_cart(id: int, db=Depends(get_db), current_user: dict = Depends(info)):
    user_id = current_user.id
    cart_entry = db.query(Cart).filter(Cart.user_id == user_id, Cart.item_id == id).first()
    if not cart_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")
    db.delete(cart_entry)
    db.commit()
    return {
        "detail": f"Item {id} removed from your cart"
    }

@router.delete("/decrease/{id}")
def decrease_quantity(id: int, db=Depends(get_db), current_user: dict = Depends(info)):
    user_id = current_user.id
    cart_entry = db.query(Cart).filter(Cart.user_id == user_id, Cart.item_id == id).first()
    if not cart_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")
    if cart_entry.quantity > 1:
        cart_entry.quantity -= 1
        db.commit()
        db.refresh(cart_entry)
        return {
            "detail": f"Decreased quantity of item {id} in your cart",
            "cart": {
                "cart_id": cart_entry.id,
                "user_id": cart_entry.user_id,
                "item_id": cart_entry.item_id,
                "quantity": cart_entry.quantity
            }
        }
    else:
        db.delete(cart_entry)
        db.commit()
        return {
            "detail": f"Item {id} removed from your cart"
        }