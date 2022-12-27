from flask.views import MethodView
from models import UserModel, AdvertisementModel, Session, Token
from flask import jsonify, request
from errors import ApiException
from sqlalchemy.exc import IntegrityError
from auth import hash_pass, check_password
from validate import CreateUser, validateData, CreateAdver, PatchUser, Login, PatchAdver
from auth import check_auth
from crud import get_item
from datetime import datetime


# добавил функцию для вывода всего списка пользователей
def allUserView():
    with Session() as session:
        list_user = session.query(UserModel).all()
        user_list = []
        for user in list_user:
            dict_user = {"id_user": user.id, "email": user.email}
            user_list.append(dict_user)
    return jsonify(user_list)

def login():
    login_data = validateData(request.json, Login)
    with Session() as session:
        user = session.query(UserModel).filter(UserModel.email == login_data["email"]).first()
        if user is None or not check_password(user.password, login_data["password"]):
            raise ApiException(401, "Invalid user or password")
        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({"token": token.id})

class userView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise ApiException(404, 'User not found')
            return jsonify({
                "id_user": user.id,
                "email": user.email
            })

    def post(self):
        user_data = validateData(request.json, CreateUser)
        user_data['password'] = hash_pass(user_data['password'])
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "email is already busy")
            return jsonify({'id_user': new_user.id, 'email': new_user.email})


    def patch(self, user_id: int):
        user_data = validateData(request.json, PatchUser)
        if 'password' in user_data:
            user_data['password'] = hash_pass(user_data['password'])
        with Session() as session:
            token = check_auth(session)
            user = session.query(UserModel).get(user_id)

            # проверка на наличие пользователя
            if user is None:
                raise ApiException(404, 'user not found')

            if token.user_id != user.id:
                raise ApiException(403, "user has no access")
            for key, value in user_data.items():
                setattr(user, key, value) # команда динамического обновления атрибутов существующего объекта SQLAlchemy
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "email is already busy")
            return jsonify({'id_user': user.id, 'email': user.email})


    def delete(self, user_id):
        with Session() as session:
            token = check_auth(session)
            user = session.query(UserModel).get(user_id)

            if user is None:
                raise ApiException(404, 'user not found')

            if token.user_id != user.id:
                raise ApiException(403, "user has no access")

            else:
                session.delete(user)
                session.commit()
                return jsonify({'id_user': user_id, 'status': 'deleted'})


# добавил функцию для вывода всего списка пользователей
def allAdverView():
    with Session() as session:
        list_adver = session.query(AdvertisementModel).all()
        adver_list = []
        for adver in list_adver:
            dict_adver = {"adver_id": adver.id,
                          "heading": adver.heading,
                          "description": adver.description,
                          "date_of_creation": adver.date_of_creation,
                          "user": adver.user.email}
            adver_list.append(dict_adver)
    return jsonify(adver_list)

class adverView(MethodView):
    def get(self, adver_id: int):
        with Session() as session:
            adver = session.query(AdvertisementModel).get(adver_id)
            if adver is None:
                raise ApiException(404, 'User not found')
            return jsonify({
                "id_adver": adver.id,
                "heading": adver.heading,
                "description": adver.description,
                "date_of_creation": adver.date_of_creation,
                "user": adver.user.email
            })

    def post(self):
        adver_data = validateData(request.json, CreateAdver)
        with Session() as session:
            # Проверка авторизации
            token = check_auth(session)

            user = session.query(UserModel).get(token.user_id)
            new_adver = AdvertisementModel(**adver_data, user_id=user.id)
            session.add(new_adver)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "heading is already busy")
            return jsonify({'adver_id': new_adver.id,
                            'heading': new_adver.heading,
                            'description': new_adver.description
                            })

    def patch(self, adver_id: int):
        adver_data = validateData(request.json, PatchAdver)
        with Session() as session:
            adver = session.query(AdvertisementModel).get(adver_id)
            # проверка на наличие объявления
            if adver is None:
                raise ApiException(404, 'Advertisement not found')

            # проверка аутентификации
            token = check_auth(session)
            if adver.user_id != token.user_id:
                raise ApiException(403, "user has no access") # Уведомляет об ошибке и останавливает функцию

            for key, value in adver_data.items():
                setattr(adver, key, value) # команда динамического обновления атрибутов существующего объекта SQLAlchemy
            session.add(adver)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "heading is already busy")
            return jsonify({'adver_id': adver.id,
                            'heading': adver.heading,
                            'description': adver.description
                            })

    def delete(self, adver_id):
        with Session() as session:
            adver = session.query(AdvertisementModel).get(adver_id)
            # проверка на наличие объявления
            if adver is None:
                raise ApiException(404, 'Advertisement not found')

            # проверка аутентификации
            token = check_auth(session)
            if adver.user_id != token.user_id:
                raise ApiException(403, "user has no access")



            session.delete(adver)
            session.commit()
            return jsonify({'adver_id': adver_id, 'status': 'deleted'})
