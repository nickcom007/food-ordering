from os import name
from typing import List, Optional
from pydantic import BaseModel


'''
Validation and schema for Cart
'''


class CartBase(BaseModel):

    customer_email: str


class CartCreate(CartBase):

    pass


class Cart(CartBase):

    id: int
    total_price: float

    class Config:
        orm_mode = True


'''
Validation and schema for Customer
'''


class CustomerBase(BaseModel):

    email: str


class CustomerCreate(CustomerBase):

    password: str


class Customer(CustomerBase):

    first_name: Optional[str]
    last_name: Optional[str]
    enabled: bool

    class Config:
        orm_mode = True


'''
Validation and schema for Restaurant
'''


class RestaurantBase(BaseModel):

    name: str
    address: str
    phone: str


class RestaurantCreate(RestaurantBase):

    pass


class Restaurant(RestaurantBase):

    id: int
    image_url: Optional[str]

    class Config:
        orm_mode = True


'''
Menu Item
'''


class MenuItemBase(BaseModel):

    name: str
    price: float


class MenuItemCreate(MenuItemBase):

    restaurant_id: int


class MenuItem(MenuItemCreate):

    id: int
    description: Optional[str]

    class Config:
        orm_mode = True


'''
Order Item
'''


class OrderItemBase(BaseModel):

    menu_item_id: int
    cart_id: int


class OrderItemCreate(OrderItemBase):

    quantity: int


class OrderItem(OrderItemCreate):

    id: int
    price: float

    class Config:
        orm_mode = True
