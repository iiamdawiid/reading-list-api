from flask_sqlalchemy import SQLAlchemy
# going to be used for primary keys in database
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(64), primary_key = True)
    username = db.Column(db.String(16), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    books = db.relationship('Book', backref='user')

    def __init__(self, username, password):
        self.id = uuid4()
        self.username = username
        self.password = generate_password_hash(password)

    def compare_password(self, password):
        return check_password_hash(self.password, password)
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.item():
            if key == 'password':
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'date_created': self.date_created,
            'books': [book.to_response() for book in self.books]
        }



class Book(db.Model):
    id = db.Column(db.String(64), primary_key = True)
    book_name = db.Column(db.String(100), nullable = False)
    genre = db.Column(db.String(50), nullable = True)
    desc = db.Column(db.String(250), nullable = True)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow, onupdate = datetime.utcnow)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'))

    def __init__(self, book_name, genre, desc):
        self.id = uuid4()
        self.book_name = book_name
        self.genre = genre
        self.desc = desc

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.item():
            if key == 'password':
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'genre': self.genre,
            'desc': self.desc,
            'date_added': self.date_added,
            'updated_at': self.updated_at,
            'user_id': self.user_id
        }