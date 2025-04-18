from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status_codes
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from .database import SessionLocal

load_dotenv()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
