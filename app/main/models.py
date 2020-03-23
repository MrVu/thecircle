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
    'mod':2,
    'admin': 3
}


# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Post(Base):
    __tablename__ = 'blog_post'
    category = db.Column(db.String(128), nullable=True)
    title = db.Column(db.String(128), nullable=False)
    description_text = db.Column(db.String(128), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    deals= db.relationship('Deal', backref='belong_to_post', lazy='dynamic')
    interest = db.Column(db.String(128))
    min_money = db.Column(db.String(128))
    level = db.Column(db.String(128))
    service_fee = db.Column(db.Integer)

    def __init__(self, category, title, description_text, detail, interest, min_money, level):
        self.category= category
        self.title = title
        self.description_text = description_text
        self.detail = detail
        self.interest = interest
        self.min_money= min_money
        self.level = level

    def set_service_fee(self, int_interest):
        int_interest = int(int_interest.strip('%'))
        if int_interest < 100:
            self.service_fee = 50000
        elif 100 < int_interest < 300:
            self.service_fee = 100000
        else:
            self.service_fee = 150000

class User(Base, UserMixin):
    __tablename__ = 'user'
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    phone_number = db.Column(db.String(50))
    address = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    deals = db.relationship('Deal', backref='belong_to_user', lazy='dynamic')
    access = db.Column(db.Integer())

    def __init__(self, name, email, phone_number, address, access=ACCESS['user']):
        self.name = name
        self.email = email
        self.phone_number= phone_number
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


class Deal(Base):
    __tablename__ = 'deal'
    status = db.Column(db.String(120))
    invest_money = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = current_user
            if not current_user.is_authenticated:
                return redirect(url_for('auth.user_login'))
            elif not user.allowed(access_level):
                return redirect(url_for('auth.user_profile', id= current_user.id, message="You do not have access to that page. Sorry!"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
