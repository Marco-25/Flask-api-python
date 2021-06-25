from sql_alchemy import database
from flask import request, url_for
from requests import post
from env import MAILGUN_DOMAIN, MAILGUN_API_KEY, FROM_TITLE, FROM_EMAIL
import bcrypt

from datetime import datetime


class UserModel(database.Model):
    __tablename__ = 'users'

    user_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    login = database.Column(database.String(50), unique=True, nullable=False)
    password = database.Column(database.String(100),  nullable=False)
    email = database.Column(database.String(100), unique=True,  nullable=False)
    active = database.Column(database.Boolean,  default=False)
    created_at = database.Column(database.Date, default=datetime.now())
    updated_at = database.Column(database.Date, default=datetime.now())

    def __init__(self, name, login, password, email, active):
        self.name = name
        self.login = login
        self.password = bcrypt.hashpw(
            password.encode('utf8'), bcrypt.gensalt(8))
        self.email = email
        self.active = active

    def json(self):
        return {
            'id_usuario': self.user_id,
            'nome': self.name,
            'login': self.login,
            'email': self.email,
            'criado_em': self.created_at,
            'atualizado_em': self.updated_at
        }

    def send_confirmation_email(self):
        link = request.url_root[:-1] + \
            url_for('userconfirm', user_id=self.user_id)
        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                  "to": self.email,
                  "subject": "Confirmação de cadastro de usuario",
                  "text": f"Confirme seu cadastro clicando no link: {link}",
                  "html": f"<html><p><a href={link}> Click no link para confirmar seu cadastro de usuario. </a></p></html>"}
        )

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def update_user(self, name, password):
        self.name = name
        self.password = bcrypt.hashpw(
            password.encode('utf8'), bcrypt.gensalt())

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None
