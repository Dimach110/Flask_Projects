from flask.views import MethodView
from models import UserModel, AdvertisementModel, Session
from flask import jsonify, request
from errors import ApiException
from sqlalchemy.exc import IntegrityError

class userView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            # print(type(user), "->", user)
            if user is None:
                raise ApiException(404, 'User not found')
            return jsonify({
                "id_user": user.id,
                "email": user.email
            })

    def post(self):
        user_data = request.json
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "email is already busy")
            return jsonify({'id_user': new_user.id, 'email': new_user.email})


    def patch(self):
        pass

    def delete(self):
        pass

class adverView(MethodView):
    # def get(self, user_id: int):
    #     with Session() as session:
    #         user = session.query(UserModel).get(user_id)
    #         # print(type(user), "->", user)
    #         if user is None:
    #             raise ApiException(404, 'User not found')
    #         return jsonify({
    #             "id_user": user.id,
    #             "email": user.email
    #         })
    #
    # def post(self):
    #     user_data = request.json
    #     with Session as session:
    #         new_user = UserModel(**user_data)
    #         session.add(new_user)
    #         session.commit()
    #         return jsonify({'id_user': new_user.id, 'email': new_user.email})


    def patch(self):
        pass

    def delete(self):
        pass

