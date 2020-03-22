from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, current_app
from flask_login import login_user, logout_user, current_user
from app.main.models import Post, User
from werkzeug.utils import secure_filename
from app import db
from app.main.models import requires_access_level, ACCESS
from .forms import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/users/<int:id>')
@requires_access_level(ACCESS['user'])
def user_profile(id):
    table_header = ['Mặt hàng', 'Tiền đầu tư','Phí kho hàng', 'Tình trạng']
    user = User.query.get(id)
    return render_template('auth/user_profile.html', user=user, table_header=table_header)


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
