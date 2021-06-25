from flask_restful import Resource, reqparse
from model.NewsModel import NewsModel
from flask import make_response, render_template

from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.utils import get_jwt

from blacklist import BLACKLIST

import traceback


class News(Resource):
    # @jwt_required()
    def get(self):
        return {'noticias': [new.json() for new in NewsModel.query.all()]}


class New(Resource):

    body = reqparse.RequestParser()
    body.add_argument('title', type=str)
    body.add_argument('content', type=str)
    body.add_argument('type_new', type=str)

    @jwt_required()
    def get(self, type_new):
        new = NewsModel.find_new(type_new)
        if new:
            # return new.json()
            return [new.json() for new in NewsModel.query.all() if new.type_new == type_new]
        return {'message': 'new not found.'}, 404

    @jwt_required()
    def put(self, new_id):

        data = self.body.parse_args()

        new = NewsModel.find_user(new_id)
        if user:
            try:
                new.update_new(data['title'], data['content'])
                new.save_new()
                return {'message': 'new updated!', 'new': user.json()}, 200
            except:
                return {'message': 'An internal error ocurred to updateding new.'}, 500
        return {'message': 'new not found!'}, 404

    @jwt_required()
    def delete(self, new_id):
        new = NewsModel.find_user(new_id)
        if new:
            try:
                new.delete_new()
                return {'message': 'new deleted.'}, 200
            except:
                return {'message': 'An internal error ocurred to deleted new.'}, 500
        return {'message': 'new not found'}, 404


class RegisterNew(Resource):
    @jwt_required()
    def post(self):
        body = reqparse.RequestParser()
        body.add_argument('title', type=str)
        body.add_argument('content', type=str)
        body.add_argument('type_new', type=str)

        body = reqparse.RequestParser()
        body.add_argument('title', type=str, required=True,
                          help="the field 'title' cannot be left blank.")
        body.add_argument('content', type=str, required=True,
                          help="the field 'content' cannot be left blank.")
        body.add_argument('type_new', type=str, required=True,
                          help="the field 'type_new' cannot be left blank.")

        data = body.parse_args()

        if NewsModel.find_by_title(data['title']) or data.get('title') is '':
            return {'message': f"The title ''{data['title']}'' already exists."}, 400

        new_object = NewsModel(**data)
        try:
            new_object.save_new()
        except:
            new_object.delete_new()
            traceback.print_exc()
            return {'message': 'An internal error ocurred to trying to save new.'}, 500

        return {'message': 'User created successfully.', 'new': user_object.json()}, 201


class Unsubscribe(Resource):
    pass
#     @classmethod
#     def get(cls, user_id):
#         # buscar da lista de receive news
#         user = UserModel.find_user(user_id)

#         if not user:
#             return {'message': f"User id ''{user_id}'' not found."}, 404

#         user.active = True
#         user.save_user()
#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template('user_confirm.html', email=user.email, user=user.login), headers)
