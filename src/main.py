from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import schema
from sqlalchemy.orm import Session, session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .dependencies import get_db
from .routers import customer

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(customer.router)


@app.post("/restaurant/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):

    # uniform the name to lower case
    restaurant.name = restaurant.name.lower()

    return crud.create_restaurant(db, restaurant)


@app.get("/restaurant/", response_model=List[schemas.Restaurant])
def get_all_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    return crud.get_all_restaurants(db, skip, limit)


@app.get("/restaurant/{name}", response_model=List[schemas.Restaurant])
def get_restaurant(name: str, db: Session = Depends(get_db)):

    db_restaurant = crud.get_restaurant_by_name(db, name.lower())

    return db_restaurant


@app.post("/restaurant/menu_item/", response_model=schemas.MenuItem)
def create_menu_item(menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):

    return crud.create_menu_item(db, menu_item)


@app.get("/restaurant/menu_item/{restaurant_id}", response_model=List[schemas.MenuItem])
def get_all_menu_items_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):

    if crud.get_restaurant(db, restaurant_id) is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db_menu_items = crud.get_menu_items_for_restaurant(db, restaurant_id)

    return db_menu_items


@app.post("/order_item/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):

    # Will return a OrderItem includes price
    db_order_item = crud.create_order_item(db, order_item)

    # Will also update the cart price
    db_cart_to_update = crud.update_cart_total_price(db, order_item.cart_id)

    return db_order_item


@app.delete("/order_item/{order_id}", response_model=schemas.Cart)
def delete_order_item(order_id: int, db: Session = Depends(get_db)):

    updated_cart = crud.delete_order_item(db, order_id)
    if updated_cart is None:
        raise HTTPException(status_code=404, detail="No order item found")

    # will return the updated cart with new total price
    return updated_cart

# @app.post("/customers/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
