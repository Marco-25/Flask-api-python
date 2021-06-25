from sql_alchemy import database
from datetime import datetime


class NewsModel(database.Model):
    __tablename__ = 'news'

    new_id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    content = database.Column(database.String(100), nullable=False)
    type_new = database.Column(database.String(100), nullable=False)
    created_at = database.Column(database.Date, default=datetime.now())
    updated_at = database.Column(database.Date, default=datetime.now())
    receive_new_id = database.Column(
        database.Integer, database.ForeignKey('receivenews.receive_new_id'))

    def __init__(self, title, content, type_new, created_at, updated_at):
        self.title = title
        self.content = content
        self.type_new = type_new
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self):
        return {
            'id_noticia': self.new_id,
            'titulo': self.title,
            'conteudo': self.content,
            'tipo_noticia': self.type_new,
            'criado_em': self.created_at,
            'atualizado_em': self.updated_at
        }

    @classmethod
    def find_new(cls, type_new):
        new = cls.query.filter_by(type_new=type_new).all()
        if new:
            return new
        return None

    @classmethod
    def find_new(cls, title):
        new = cls.query.filter_by(title=title).all().first()
        if new:
            return new
        return None

    def save_new(self):
        database.session.add(self)
        database.session.commit()

    def update_new(self, title, content):
        self.title = title
        self.content = content
        self.updated_at = datetime.now()

    def delete_new(self):
        database.session.delete(self)
        database.session.commit()
