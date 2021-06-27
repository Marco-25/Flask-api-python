from flask_restful import Resource, reqparse
from model.ReceiveNewsModel import ReceiveNewsModel
from model.NewsModel import NewsModel
from model.UserModel import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from flask import make_response, render_template
from sqlalchemy.orm import defer
import traceback


class ReceiveNew(Resource):
    def get(self, receive_new_id):
        receive_new = ReceiveNewsModel.find_receive_new_by_id(receive_new_id)
        if receive_new:
            return [new.json() for new in receive_new.query.all() if new.receive_new_id == receive_new_id]
        return {"message": "not found"}, 404

    def post(self):
        body = reqparse.RequestParser()
        body.add_argument('name', type=str, required=True,
                          help="the field 'name' cannot be left blank.")
        body.add_argument('email', type=str, required=True,
                          help="the field 'email' cannot be left blank.")
        body.add_argument('type_new', type=str, required=True,
                          help="the field 'type_new' cannot be left blank.")

        data = body.parse_args()

        if ReceiveNewsModel.find_receive_new_by_email(data.get('email')) \
                or UserModel.find_user_by_email(data.get('email')):
            return {'message': f"E-mail ''{data['email']}'' already exists"}, 400

        if not NewsModel.find_new_by_type_specific(data.get('type_new')):
            return {'message': f"This type_new ''{data['type_new']}'' not exists",
                    "type_new accepted": [new.type_new for new in NewsModel.query.all()]}, 400

        new_object = ReceiveNewsModel(**data)
        try:
            new_object.save_receive_news()
            return {'message': 'New created successfully.', 'user': new_object.json()}, 201
        except:
            new_object.delete_receive_news()
            traceback.print_exc()
            return {'message': 'An internal error ocurred to trying to save new.'}, 500


class Unsubscribe(Resource):
    @classmethod
    def get(cls, receive_new_id):
        receiver_new = ReceiveNewsModel.find_receive_new_by_id(
            receive_new_id)

        if not receiver_new:
            return {'message': f"receiver_new_id ''{receive_new_id}'' not found."}, 404

        if receiver_new.active is False:
            return {"message": "link expired or you are not on our list"}

        receiver_new.active = False
        receiver_new.save_receive_news()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('unsubscribe_receive_new.html', name=receiver_new.name), headers)
