from os import name
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas

'''
Customer
'''


def get_customer(db: Session, email: str):

    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):

    fake_hashed_password = customer.password + "funnyhashed"
    db_user = models.Customer(
        email=customer.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


'''
Cart
'''


def create_cart(db: Session, cart: schemas.CartCreate):

    db_cart = models.Cart(customer_email=cart.customer_email)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


def get_cart_by_email(db: Session, email: str):

    return db.query(models.Cart).filter(models.Cart.customer_email == email).first()


def update_cart_total_price(db: Session, id: int):

    # Get all order items within the cart
    all_order_items = db.query(models.OrderItem).filter(models.OrderItem.cart_id == id)\
        .all()

    # Calculate the total_price
    total_price = sum([order_item.price for order_item in all_order_items])

    # Get the cart object to update
    db_cart_to_update = db.query(models.Cart).get(id)
    db_cart_to_update.total_price = total_price

    db.commit()
    db.refresh(db_cart_to_update)

    return db_cart_to_update


'''
Restaurant
'''


def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):

    db_restaurant = models.Restaurant(address=restaurant.address,
                                      name=restaurant.name, phone=restaurant.phone)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def get_restaurant(db: Session, id: int):

    return db.query(models.Restaurant).filter(models.Restaurant.id == id).first()


def get_all_restaurants(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Restaurant).offset(skip).limit(limit).all()


def get_restaurant_by_name(db: Session, name: str):

    return db.query(models.Restaurant).filter(models.Restaurant.name == name.lower()).all()


'''
Menu Item
'''


def create_menu_item(db: Session, menu_item: schemas.MenuItemCreate):

    db_menu_item = models.MenuItem(name=menu_item.name, price=menu_item.price,
                                   restaurant_id=menu_item.restaurant_id)

    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)

    return db_menu_item


def get_menu_items_for_restaurant(db: Session, restaurant_id: int):

    return db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()


def get_menu_item(db: Session, id: int):

    return db.query(models.MenuItem).filter(models.MenuItem.id == id).first()


'''
Order Item
'''


def create_order_item(db: Session, order_item: schemas.OrderItemCreate):

    # get the menu item price first
    db_menu_item = get_menu_item(db, order_item.menu_item_id)
    item_price = db_menu_item.price

    # calculate the total price for a order item
    order_price = item_price * order_item.quantity

    db_order_item = models.OrderItem(quantity=order_item.quantity,
                                     price=order_price, menu_item_id=order_item.menu_item_id,
                                     cart_id=order_item.cart_id)

    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)

    return db_order_item


def delete_order_item(db: Session, id: int):

    cart_to_update = db.query(models.OrderItem).get(id)
    # if failed somehow
    if cart_to_update is None:
        return None

    cart_id = cart_to_update.cart_id
    # Remove the order item
    _ = db.query(models.OrderItem).filter(models.OrderItem.id == id)\
        .delete()

    # Update the total price for the cart
    cart_update_result = update_cart_total_price(db, cart_id)

    return cart_update_result

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):

#     db_item = models.Item(**item.dict(), owner_id=user_id)

#     db.add(db_item)

#     db.commit()

#     db.refresh(db_item)

#     return db_item
