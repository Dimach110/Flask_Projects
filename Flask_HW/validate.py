from pydantic import BaseModel, EmailStr, ValidationError, validator
from errors import ApiException
from typing import Any, Dict, Optional, Type

# создаём класс с нужной схемой (согласно которой проводится проверка)
class Login(BaseModel):
    email: EmailStr
    password: str

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class PatchUser(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

class CreateAdver(BaseModel):
    heading: str
    description: str

class PatchAdver(BaseModel):
    heading: Optional[str]
    description: Optional[str]

class Login(BaseModel):
    email: EmailStr
    password: str


# создаём функцию проверки ввода данных согласной заданной схеме
def validateData(data: dict, schema_class):
    try:
        return schema_class(**data).dict()
    except ValidationError as err:
        raise ApiException(400, err.errors())


