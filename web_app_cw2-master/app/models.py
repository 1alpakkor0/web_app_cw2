from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
## from flask_login import LoginManager, current_user
from app import db
## from flask_sqlalchemy import SQLAlchemy

## db = SQLAlchemy()

# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.context_processor
# def inject_user():
#     return dict(current_user=current_user)

class User(db.Model, UserMixin): ## This is the user model which is used for creating the user table in the database
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    favorites = db.relationship('Product', secondary='favorites', backref='favorited_by', lazy='dynamic')


class Product(db.Model, UserMixin): ## This is the product model which is used for creating the product table in the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)










favorites = db.Table('favorites', db.Column('user_id', db.Integer, db.ForeignKey('user.id')), db.Column('product_id', db.Integer, db.ForeignKey('product.id'))) ## This is the favorites table which is used for creating the many-to-many relationship between the user and product tables


class Category(db.Model, UserMixin): ## This is the category model which is used for creating the category table in the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    products = db.relationship('Product', backref='category', lazy=True) ## This is the relationship between the category and product tables



class CartItem(db.Model, UserMixin): ## This is the cart item model which is used for creating the cart item table in the database relation between the user and product tables
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product') ## This is the relationship between the cart item and product tables
