from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from .db import models
from .db.database import engine
from .routers import customer, restaurant, order_item
from .dependencies import get_db
from .schemas import Token, Customer
from .security.pwd_hash import authenticate_user
from .security.jwt_auth import create_access_token, get_current_active_user, get_current_user
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(customer.router)
app.include_router(restaurant.router)
app.include_router(order_item.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def hello():
    return "Welcome to the food ordering system!"


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/test/me/", response_model=Customer)
async def read_users_me(current_user: Customer = Depends(get_current_active_user)):
    return current_user
