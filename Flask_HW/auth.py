from flask import request
from app import bcrypt
from config import TOKEN_TTL
from errors import ApiException
from models import Token
import time
import uuid


# хешируем пароли
def hash_pass(password: str):
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()

# Проверка соответсвия паролей (введённого и хешированного для определённого пользователя)
def check_password(password_hash: str, password: str) -> bool:
    return bcrypt.check_password_hash(password_hash.encode(), password.encode())
#
# Проверка на наличие токена, на его соответствие BD и на его годность (просрочен или нет)
def check_auth(session):

    try:
        token = uuid.UUID(request.headers.get("token"))
    except (ValueError, TypeError):
        raise ApiException(403, "add token to headers")

    token = session.query(Token).get(token)

    if token is None:
        raise ApiException(403, "incorrect token")

    if time.time() - token.creation_time.timestamp() > TOKEN_TTL:
        raise ApiException(403, "the token expired")

    return token

