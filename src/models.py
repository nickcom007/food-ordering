from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class Customer(Base):

    __tablename__ = "customer"

    email = Column(String(32), primary_key=True, index=True)
    first_name = Column(String(24))
    last_name = Column(String(24))
    hashed_password = Column(String(32))
    enabled = Column(Boolean, default=True)
    cart_id = Column(Integer, ForeignKey("cart.id"))

    cart = relationship("Cart", back_populates="customer")


class Item(Base):

    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float(32))

    customer = relationship("Customer", back_populates="cart")


class OrderItem(Base):

    __tablename__ = "orderitem"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    price = Column(Float(32))
    menu_item_id = Column(ForeignKey("menuitem.id"))
    cart_id = Column(ForeignKey("cart.id"))


class MenuItem(Base):

    __tablename__ = "menuitem"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24))
    price = Column(Float(32))
    description = Column(String(64))
    restaurant_id = Column(ForeignKey("restaurant.id"))


class Restaurant(Base):

    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(64))
    name = Column(String(32))
    phone = Column(String(12))
    image_url = Column(String(512))
