from sql_alchemy import database
from datetime import datetime


class NewsModel(database.Model):
    __tablename__ = 'news'

    new_id = database.Column(database.Integer, primary_key=True)
    type_new = database.Column(database.String(100), nullable=False)
    title = database.Column(database.String(100), nullable=False)
    content = database.Column(database.Text(), nullable=False)
    created_at = database.Column(database.String(20))
    updated_at = database.Column(database.String(20))

    receive_new_id = database.Column(
        database.Integer, database.ForeignKey('receivenews.receive_new_id'))

    def __init__(self, title, content, type_new, receive_new_id):
        self.title = title
        self.content = content
        self.type_new = type_new
        self.receive_new_id = receive_new_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def json(self):
        return {
            'new_id': self.new_id,
            'title': self.title,
            'content': self.content,
            'type_new': self.type_new,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def find_new_by_type(cls, type_new):
        new = cls.query.filter_by(type_new=type_new).all()
        if new:
            return new
        return None

    @classmethod
    def find_new_by_type_specific(cls, type_new):
        new = cls.query.filter_by(type_new=type_new).first()
        if new:
            return new
        return None

    @classmethod
    def find_new_by_id(cls, new_id):
        new = cls.query.filter_by(new_id=new_id).first()
        if new:
            return new
        return None

    @classmethod
    def find_new_by_title(cls, title):
        new = cls.query.filter_by(title=title).first()
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
