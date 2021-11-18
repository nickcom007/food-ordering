from typing import List, Optional
from pydantic import BaseModel


class CartBase(BaseModel):

    total_price: float


class CartCreate(CartBase):

    pass


class Cart(CartBase):

    id: int

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):

    email: str


class CustomerCreate(CustomerBase):

    password: str


class Customer(CustomerBase):

    first_name: str
    last_name: str
    enabled: bool

    class Config:
        orm_mode = True
