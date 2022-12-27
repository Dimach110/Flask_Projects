import atexit
import uuid
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import UUIDType, EmailType
from config import PG_DSN
from typing import Type
from cachetools import cached


engine = create_engine(PG_DSN) # привязываем нашу базу данных
Base = declarative_base(bind=engine)



class UserModel(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

class AdvertisementModel(Base):

    __tablename__ = 'Advertisements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, unique=False, nullable=False, index=True)
    date_of_creation = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    user = relationship(UserModel, backref='Advertisements')

class Token(Base):

    __tablename__ = 'Token'
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('Users.id', ondelete="CASCADE"))
    creation_time = Column(DateTime, server_default=func.now())
    user = relationship(UserModel, lazy='joined')
# lazy='joined' объединяет две таблицы с помощью LEFT JOIN (ленивый оператор)


Base.metadata.drop_all()
Base.metadata.create_all() # проводим миграцию

Session = sessionmaker(bind=engine)
session = Session()

# # Создаём тестовых пользователей
# u1 = UserModel(email = 'e1@e.ru', password = '12345')
# u2 = UserModel(email = 'e2@e.ru', password = '54321')
# session.add_all([u1, u2])
# session.commit()

# разорвать соединение при завершении работы приложения
atexit.register((lambda: engine.dispose))

# предполагаю что для хранения сессии в кеше
@cached({})
def get_engine():
    return create_engine(PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine())


# def init_db():
#     Base.metadata.create_all(bind=get_engine())
#
#
# def close_db():
#     get_engine().dispose()


# не разобрался пока зачем
ORM_MODEL_CLS = Type[UserModel] | Type[Token] | Type[AdvertisementModel]
ORM_MODEL = UserModel | Token | AdvertisementModel