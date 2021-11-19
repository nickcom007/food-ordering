from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from ..dependencies import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import crud

'''
Contains all RESTful API for Restaurant and associated Menu Items
'''
router = APIRouter(
    prefix="/restaurant"
)


@router.post("/", response_model=schemas.Restaurant, tags=['restaurant'])
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):

    # uniform the name to lower case
    restaurant.name = restaurant.name.lower()

    return crud.create_restaurant(db, restaurant)


@router.get("/", response_model=List[schemas.Restaurant], tags=['restaurant'])
def get_all_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    return crud.get_all_restaurants(db, skip, limit)


@router.get("/{name}", response_model=List[schemas.Restaurant], tags=['restaurant'])
def get_restaurant(name: str, db: Session = Depends(get_db)):

    db_restaurant = crud.get_restaurant_by_name(db, name.lower())

    return db_restaurant


@router.post("/menu_item", response_model=schemas.MenuItem, tags=['menu_item'])
def create_menu_item(menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):

    return crud.create_menu_item(db, menu_item)


@router.get("/{restaurant_id}/menu_item", response_model=List[schemas.MenuItem], tags=['menu_item'])
def get_all_menu_items_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):

    if crud.get_restaurant(db, restaurant_id) is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db_menu_items = crud.get_menu_items_for_restaurant(db, restaurant_id)

    return db_menu_items
