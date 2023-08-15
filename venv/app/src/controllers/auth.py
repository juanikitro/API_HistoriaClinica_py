from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv
import os

from ..models.Credentials import Credentials

load_dotenv()


def authenticate_user(username: str, password: str):
    # Hard-coded username and password
    if username == "D3f4ultUs3r" and password == "D3f4ultP4ssw0rd":
        return True
    return False


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=int(os.getenv("TOKEN_EXPIRES"))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def auth(credentials: Credentials):
    user = authenticate_user(credentials.user, credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": credentials.user})
    return {"access_token": access_token, "token_type": "bearer"}


def verify_jwt(token: str):
    try:
        token = jwt.decode(
            token.split(" ")[1],
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )
        return

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )
