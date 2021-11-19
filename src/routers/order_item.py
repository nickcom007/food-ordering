from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from ..dependencies import get_db
from sqlalchemy.orm import Session
from .. import crud


'''
Contains all RESTful API for Restaurant and associated Menu Items
'''
router = APIRouter(
    prefix="/order_item",
    tags=['order_item']
)


@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):

    # Will return a OrderItem includes price
    db_order_item = crud.create_order_item(db, order_item)

    # Will also update the cart price
    db_cart_to_update = crud.update_cart_total_price(db, order_item.cart_id)

    return db_order_item


@router.delete("/{order_id}", response_model=schemas.Cart)
def delete_order_item(order_id: int, db: Session = Depends(get_db)):

    updated_cart = crud.delete_order_item(db, order_id)
    if updated_cart is None:
        raise HTTPException(status_code=404, detail="No order item found")

    # will return the updated cart with new total price
    return updated_cart
