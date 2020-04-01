from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, current_app
from flask_login import login_user, logout_user, current_user
from app.main.models import User, requires_access_level, ACCESS, Order, OrderStatus
from werkzeug.utils import secure_filename
from app import db
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/users/<int:id>')
@requires_access_level(ACCESS['user'])
def user_profile(id):
    table_header = ['Tên dịch vụ', 'Lĩnh vực', 'Ngân sách', 'Tình trạng']
    user = User.query.get(id)
    return render_template('auth/user_profile.html', user=user, table_header=table_header)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.user_profile', id=current_user.id))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        email = form.email.data
        existed_user = User.query.filter_by(email=email).first()
        if existed_user:
            flash('Email đã được sử dụng')
            return redirect(url_for('auth.register'))
        pw = form.password.data
        user = User(name=name, phone_number=phone_number,
                    address=address, email=email)
        user.set_password(pw)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('auth.user_profile', id=user.id))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.get_posts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.user_login'))
        login_user(user)
        if user.access >= ACCESS['admin']:
            return redirect(url_for('admin.get_posts'))
        else:
            return redirect(url_for('auth.user_profile', id=user.id))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@requires_access_level(ACCESS['user'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))
