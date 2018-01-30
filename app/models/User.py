# _*_ coding: utf-8 _*_
# filename: User.py
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passwd = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username
