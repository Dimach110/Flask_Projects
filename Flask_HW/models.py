import atexit
from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import PG_DSN

engine = create_engine(PG_DSN) # привязываем нашу базу данных
Base = declarative_base(bind=engine)



class UserModel(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

class AdvertisementModel(Base):

    __tablename__ = 'Advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, unique=False, nullable=False, index=True)
    date_of_creation = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    owner = Column(String, unique=False, nullable=False, index=True)

Base.metadata.drop_all()
Base.metadata.create_all() # проводим миграцию

Session = sessionmaker(bind=engine)
session = Session()


u1 = UserModel(
    email = 'e1@e.ru',
    password = '12345'
)

u2 = UserModel(
    email = 'e2@e.ru',
    password = '54321'
)
session.add_all([u1, u2])
session.commit()

atexit.register((lambda: engine.dispose)) # разорвать соединение при завершении работы приложения