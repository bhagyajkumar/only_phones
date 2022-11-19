from .ext import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    