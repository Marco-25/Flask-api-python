from sql_alchemy import database
from datetime import datetime


class ReceiveNewsModel(database.Model):
    __tablename__ = 'receivenews'

    receive_new_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    type_new = database.Column(database.String(100), nullable=False)
    active = database.Column(database.Boolean, default=True)
    created_at = database.Column(database.String(20))

    news = database.relationship('NewsModel')

    def __init__(self, name, email, type_new):
        self.name = name
        self.email = email
        self.type_new = type_new
        self.created_at = datetime.now().isoformat()

    def json(self):
        return {
            'receive_new_id': self.receive_new_id,
            'name': self.name,
            'created_at': self.created_at,
            'noticias': [new.json() for new in self.news]
        }

    @classmethod
    def find_receive_new_by_email(cls, email):
        receiver_new = cls.query.filter_by(email=email).first()
        if receiver_new:
            return receiver_new
        return None

    @classmethod
    def find_receive_new_by_id(cls, receive_new_id):
        receiver_new = cls.query.filter_by(
            receive_new_id=receive_new_id).first()
        if receiver_new:
            return receiver_new
        return None

    def save_receive_news(self):
        database.session.add(self)
        database.session.commit()

    def delete_receive_news(self):
        database.session.delete(self)
        database.session.commit()
