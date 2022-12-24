import pydantic
from errors import ApiException

# создаём класс с нужной схемой (согласно которой проводится проверка)
class CreateUserSchema(pydantic.BaseModel):
    email: str
    password: str

class CreateAdverSchema(pydantic.BaseModel):
    heading: str
    description: str
    user_id: int

# создаём функцию проверки ввода данных согласной заданной схеме
def validateData(data: dict, schema_class):
    try:
        return schema_class(**data).dict()
    except pydantic.ValidationError as err:
        raise ApiException(400, err.errors())


