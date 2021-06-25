from flask_restful import Resource, reqparse
from model.UserModel import UserModel
from flask import make_response, render_template

from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.utils import get_jwt
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST

import traceback
import bcrypt


class Users(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}


class User(Resource):

    body = reqparse.RequestParser()
    body.add_argument('name', type=str)
    body.add_argument('password', type=str)
    body.add_argument('active', type=bool)

    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404

    @jwt_required()
    def put(self, user_id):

        data = self.body.parse_args()

        user = UserModel.find_user(user_id)
        if user:
            try:
                user.update_user(data['name'], data['password'])
                user.save_user()
                return {'message': 'user updated!', 'user': user.json()}, 200
            except:
                return {'message': 'An internal error ocurred to updateding user.'}, 500
        return {'message': 'user not found!'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {'message': 'user deleted.'}, 200
            except:
                return {'message': 'An internal error ocurred to deleted user.'}, 500
        return {'message': 'user not found'}, 404


class UserRegister(Resource):
    def post(self):
        body = reqparse.RequestParser()
        body.add_argument('name', type=str, required=True,
                          help="the field 'name' cannot be left blank.")
        body.add_argument('login', type=str, required=True,
                          help="the field 'login' cannot be left blank.")
        body.add_argument('password', type=str, required=True,
                          help="the field 'password' cannot be left blank.")
        body.add_argument('email', type=str, required=True,
                          help="the field 'email' cannot be left blank.")
        body.add_argument('active', type=bool)

        data = body.parse_args()

        if UserModel.find_by_login(data['login']) or data.get('login') is '':
            return {'message': f"The login ''{data['login']}'' already exists."}, 400

        if data.get('email') is None or data.get('email') is '':
            return {'message': f"The email cannot be left null."}, 400

        if UserModel.find_by_email(data.get('email')):
            return {'message': f"The email ''{data['email']}'' already exists."}, 400

        user_object = UserModel(**data)
        user_object.active = False
        try:
            user_object.save_user()
            user_object.send_confirmation_email()
        except:
            user_object.delete_user()
            traceback.print_exc()
            return {'message': 'An internal error ocurred to trying to save user.'}, 500

        return {'message': 'User created successfully.', 'user': user_object.json()}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        body = reqparse.RequestParser()
        body.add_argument('login', type=str, required=True,
                          help="the field 'login' cannot be left blank.")
        body.add_argument('password', type=str, required=True,
                          help="the field 'password' cannot be left blank.")

        data = body.parse_args()
        user = UserModel.find_by_login(data['login'])

        data_hashed = bcrypt.hashpw(
            data['password'].encode('utf8'), user.password)
        print(data_hashed)
        print(user.password)

        if user and safe_str_cmp(user.password, data_hashed):
            if user.active:
                token_access = create_access_token(identity=user.user_id)
                return {'token': token_access}
            return {'message': 'User not confirmed'}, 400
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200


class UserConfirm(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': f"User id ''{user_id}'' not found."}, 404

        user.active = True
        user.save_user()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, user=user.login), headers)
