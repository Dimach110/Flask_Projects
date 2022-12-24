from flask.views import MethodView
from models import UserModel, AdvertisementModel, Session
from flask import jsonify, request
from errors import ApiException
from sqlalchemy.exc import IntegrityError
from auth import hash_pass
from validate import CreateUserSchema, validateData, CreateAdverSchema
from datetime import datetime

class allUserView(MethodView):
    # добавил функцию для вывода всего списка пользователей
    def get(self):
        with Session() as session:
            list_user = session.query(UserModel).all()
            user_list = []
            for user in list_user:
                dict_user = {"id_user": user.id, "email": user.email}
                user_list.append(dict_user)
        return jsonify(user_list)

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
        user_data = validateData(request.json, CreateUserSchema)
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
        user_data = request.json
        if 'password' in user_data:
            user_data['password'] = hash_pass(user_data['password'])
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            for key, value in user_data.items():
                setattr(user, key, value) # команда динамического обновления атрибутов существующего объекта SQLAlchemy
            session.add(user)
            session.commit()
            return jsonify({'id_user': user.id, 'email': user.email})


    def delete(self, user_id):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise ApiException(404, 'User not found')
            else:
                session.delete(user)
                session.commit()
                return jsonify({'id_user': user_id, 'status': 'deleted'})

class allAdverView(MethodView):
    # добавил функцию для вывода всего списка пользователей
    def get(self):
        with Session() as session:
            list_adver = session.query(AdvertisementModel).all()
            adver_list = []
            for adver in list_adver:
                dict_adver = {"id_adver": adver.id,
                              "heading": adver.heading,
                              "description": adver.description,
                              "date_of_creation": adver.date_of_creation,
                              "user": adver.user}
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
        adver_data = validateData(request.json, CreateAdverSchema)
        with Session() as session:
            new_adver = AdvertisementModel(**adver_data)
            session.add(new_adver)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "heading is already busy")
            return jsonify({'id_advers': new_adver.id,
                            'heading': new_adver.heading,
                            'description': new_adver.description
                            })
#
#
#     def patch(self, user_id: int):
#         user_data = request.json
#         if 'password' in user_data:
#             user_data['password'] = hash_pass(user_data['password'])
#         with Session() as session:
#             user = session.query(UserModel).get(user_id)
#             for key, value in user_data.items():
#                 setattr(user, key, value) # команда динамического обновления атрибутов существующего объекта SQLAlchemy
#             session.add(user)
#             session.commit()
#             return jsonify({'id_user': user.id, 'email': user.email})
#
#
#     def delete(self, user_id):
#         with Session() as session:
#             user = session.query(UserModel).get(user_id)
#             if user is None:
#                 raise ApiException(404, 'User not found')
#             else:
#                 session.delete(user)
#                 session.commit()
#                 return jsonify({'id_user': user_id, 'status': 'deleted'})
