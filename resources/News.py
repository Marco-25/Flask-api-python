from flask_restful import Resource, reqparse
from model.NewsModel import NewsModel
from flask import make_response, render_template

from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt

from blacklist import BLACKLIST

import traceback


class News(Resource):
    @jwt_required()
    def get(self):
        try:
            return {'noticias': [new.json() for new in NewsModel.query.all()]}
        except:
            return {'message': 'An internal error ocurred.'}, 500


class New(Resource):

    body = reqparse.RequestParser()
    body.add_argument('title', type=str)
    body.add_argument('content', type=str)
    body.add_argument('type_new', type=str)

    @jwt_required()
    def get(self, type_new):
        new = NewsModel.find_new_by_type(type_new)
        if new:
            return [new.json() for new in NewsModel.query.all() if new.type_new == type_new]
        return {'message': 'new not found.'}, 404

    @jwt_required()
    def put(self, new_id):

        data = self.body.parse_args()

        new = NewsModel.find_new_by_id(new_id)
        if new:
            try:
                new.update_new(data['title'], data['content'])
                new.save_new()
                return {'message': 'new updated!', 'new': new.json()}, 200
            except:
                return {'message': 'An internal error ocurred to updateding new.'}, 500
        return {'message': 'new not found!'}, 404

    @jwt_required()
    def delete(self, new_id):
        new = NewsModel.find_new_by_id(new_id)
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
        body.add_argument('title', type=str, required=True,
                          help="the field 'title' cannot be left blank.")
        body.add_argument('content', type=str, required=True,
                          help="the field 'content' cannot be left blank.")
        body.add_argument('type_new', type=str, required=True,
                          help="the field 'type_new' cannot be left blank.")
        body.add_argument('receive_new_id', type=str, default=0)

        data = body.parse_args()

        if NewsModel.find_new_by_title(data['title']) or data.get('title') is '':
            return {'message': f"The title ''{data['title']}'' already exists or is it empty."}, 400

        if data.get('type_new') is '':
            return {'message': f"The ''type_new''  cannot be empty."}, 400

        new_object = NewsModel(**data)
        try:
            new_object.save_new()
        except:
            new_object.delete_new()
            traceback.print_exc()
            return {'message': 'An internal error ocurred to trying to save new.'}, 500

        return {'message': 'New created successfully.', 'new': new_object.json()}, 201
