from blacklist import BLACKLIST
from flask import Flask, jsonify
from flask_restful import Api
from resources.User import UserConfirm, UserLogin, UserLogout, Users, User, UserRegister
from resources.News import New, News, RegisterNew
from resources.ReceiveNews import ReceiveNew, Unsubscribe

from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost/python2"
# serve para evitar os avisos
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_database():
    database.create_all()


@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_invalid(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401


api.add_resource(UserRegister, '/register_user')

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:user_id>')

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(UserConfirm, '/confirmed/<int:user_id>')

# -------------------------------------------------------

api.add_resource(News, '/news')
api.add_resource(New, '/news/<int:new_id>', '/news/<string:type_new>')
api.add_resource(RegisterNew, '/register_new')

api.add_resource(Unsubscribe, '/unsubscribe/<int:receive_new_id>')
api.add_resource(
    ReceiveNew, '/receive_news/<int:receive_new_id>', '/receive_news')

# -------------------------------------------------------

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)
