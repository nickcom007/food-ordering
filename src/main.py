from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import schema
from sqlalchemy.orm import Session, session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .dependencies import get_db
from .routers import customer, restaurant, order_item

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(customer.router)
app.include_router(restaurant.router)
app.include_router(order_item.router)


@app.get("/")
def hello():
    return "Welcome to the food ordering system!"
