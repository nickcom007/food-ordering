from passlib.context import CryptContext
from .. import crud
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    '''
    Get the hased password
    '''
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Check whether the password is correct
    '''
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    '''
    Authenticate a user by matching password in db
    '''
    user = crud.get_customer(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
