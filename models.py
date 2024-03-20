from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(14), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    posts = db.relationship('Posts', back_populates='user')


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_following(self, user):
        return Follow.query.filter_by(follower_id=self.id, followed_id=user.id).count() > 0



class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', back_populates='posts')


class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    follower = db.relationship('Users', foreign_keys=[follower_id], backref=db.backref('following', lazy='dynamic'))
    followed = db.relationship('Users', foreign_keys=[followed_id], backref=db.backref('followers', lazy='dynamic'))


