from datetime import timedelta, datetime,timezone
from fastapi import APIRouter,Depends,HTTPException,status_codes
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from api.models import User
from api.database import db_dependency,bcrypt_context
from sqlalchemy.orm import Session

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")


class UserCreateRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
        to_encode = {"sub": username, "id": user_id}
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

@router.post("/",status_code=status_codes.HTTP_201_CREATED)
async def create_user(user: UserCreateRequest, db: Session = Depends(db_dependency)):