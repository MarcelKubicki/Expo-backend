from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import logging
import uuid
import jwt

passwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return passwd_context.verify(password, password_hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

