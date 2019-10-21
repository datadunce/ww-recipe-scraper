from datetime import datetime
import os
from app import db, login
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), index=True, unique=True)
    title = db.Column(db.String(64))
    users = relationship(User, secondary='user_recipe_link')
    # ingredients = db.Column(db.
    # instructions = db.Column(db.String(128))


class User_Recipe_Link(db.Model):
    __tablename__ = 'user_recipe_link'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<URL {}>'.format(self.url)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
