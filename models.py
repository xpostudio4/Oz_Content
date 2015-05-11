"""All database models are located here"""
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)


    def __init__(self, username, email, social_id):
        self.username = username
        self.email = email
        self.social_id = social_id

    def __repr__(self):
        return '<User %r>' % self.username


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    text = db.Column(db.Text)
    url = db.Column(db.String(264))
    picture_url = db.Column(db.String(264))

    def __init__(self, name, text, url, picture_url):
        self.name = name
        self.text = text
        self.url = url
        self.picture_url = picture_url

    def __repr__(self):
        return '<Animal %r>' % self.name


