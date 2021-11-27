from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from ..dependencies import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import crud

'''
Contains all RESTful APIs for Customer and associated Cart operation
'''


router = APIRouter(
    prefix="/customers"
)


@router.post("/signup", response_model=schemas.Customer, tags=['customers'])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_user = crud.get_customer(db, email=customer.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    customer_creation = crud.create_customer(db=db, customer=customer)
    # create a cart for new customer
    cart_creation = schemas.CartCreate(customer_email=customer.email)
    crud.create_cart(db, cart_creation)

    return customer_creation


@router.get("/", response_model=List[schemas.Customer], tags=['customers'])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers


@router.get("/{email}", response_model=schemas.Customer, tags=['customers'])
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_customer(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_user


@router.post("/cart", response_model=schemas.Cart, tags=['cart'])
def create_cart_for_customer(cart: schemas.CartCreate, db: Session = Depends(get_db)):

    if crud.get_customer(db, email=cart.customer_email) is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    if crud.get_cart_by_email(db, email=cart.customer_email):
        raise HTTPException(status_code=403, detail="Cart already existed")

    return crud.create_cart(db, cart)


@router.get("/cart/{customer_email}", response_model=schemas.Cart, tags=['cart'])
def get_cart_for_customer(customer_email: str, db: Session = Depends(get_db)):

    db_carts = crud.get_cart_by_email(db, customer_email)
    if db_carts is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return db_carts
