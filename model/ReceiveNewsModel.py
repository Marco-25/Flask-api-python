from sql_alchemy import database
from datetime import datetime


class ReceiveNews(database.Model):
    __tablename__ = 'receivenews'

    receive_new_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    type_new = database.Column(database.String(100), nullable=False)
    active = database.Column(database.Boolean, default=True)
    created_at = database.Column(database.Date, datetime.now())
    news = database.relationship('NewsModel')

    def __init__(self, name, email, type_new, created_at, updated_at):
        pass

    def json(self):
        return {
            'receber_noticia_id': self.receive_new_id,
            'nome': self.name,
            'criado_em': self.created_at,
            'noticias': [new.json() for new in self.news]
        }
