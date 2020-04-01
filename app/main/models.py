# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from functools import wraps
from flask import url_for, request, redirect, session

ACCESS = {
    'guest': 0,
    'user': 1,
    'mod': 2,
    'admin': 3
}


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Category(Base):
    __tablename__ = 'category'
    name = db.Column(db.String(128), nullable=True)
    order = db.relationship(
        'Order', backref='belong_to_category', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Order(Base):
    __tablename__ = 'order'
    name = db.Column(db.String(50))
    detail = db.Column(db.Text, nullable=False)
    budget = db.Column(db.String(50))
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class OrderStatus(Base):
    __tablename__ = "order_status"
    order = db.relationship(
        'Order', backref='belong_to_status', lazy='dynamic')
    name = db.Column(db.String(50))


class User(Base, UserMixin):
    __tablename__ = 'user'
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    phone_number = db.Column(db.String(50))
    address = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    order = db.relationship(
        'Order', backref='belong_to_user', lazy='dynamic')
    access = db.Column(db.Integer())

    def __init__(self, name, email, phone_number, address, access=ACCESS['user']):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']

    def set_admin(self):
        self.access = ACCESS['admin']

    def set_mod(self):
        self.access = ACCESS['mod']

    def allowed(self, access_level):
        return self.access >= access_level

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = current_user
            if not current_user.is_authenticated:
                return redirect(url_for('auth.user_login'))
            elif not user.allowed(access_level):
                return redirect(url_for('auth.user_profile', id=current_user.id, message="You do not have access to that page. Sorry!"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
