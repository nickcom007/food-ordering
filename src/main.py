from fastapi import FastAPI
from .db import models
from .db.database import engine
from .routers import customer, restaurant, order_item

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(customer.router)
app.include_router(restaurant.router)
app.include_router(order_item.router)


@app.get("/")
def hello():
    return "Welcome to the food ordering system!"
