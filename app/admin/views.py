from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, current_app
from flask_login import login_user, logout_user, current_user
from .forms import AdminLoginForm, CreateUserForm, ChangeOrderStatusForm
from app.main.models import User, requires_access_level, ACCESS, Order, OrderStatus
from werkzeug.utils import secure_filename
from app import db

status_count = 0

admin = Blueprint('admin', __name__)
@admin.before_request
def orders_status_count():
    global status_count
    status = OrderStatus.query.get(1)
    g.status_count = Order.query.filter_by(belong_to_status=status).count()


@admin.route('/admin/users')
@requires_access_level(ACCESS['mod'])
def get_users():
    table_header = ['Tên', 'Email', 'Địa chỉ', 'Điện thoại']
    create_link = [url_for('admin.create_user'), "Tạo người dùng"]
    users = User.query.all()
    return render_template('admin/get_posts.html', users=users, table_header=table_header, create_link=create_link)


@admin.route('/admin/users/<int:id>')
@requires_access_level(ACCESS['mod'])
def admin_get_user_profile(id):
    table_header = ['Sản phẩm', 'Tiền đầu tư', 'Tình trạng']
    user = User.query.get(id)
    return render_template('admin/user_profile.html', user=user, table_header=table_header)


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin/', methods=['GET', 'POST'])
@admin.route('/admin/orders', methods=['GET', 'POST'])
@requires_access_level(ACCESS['mod'])
def get_orders():
    table_header = ['Tiêu đề', 'Khách hàng', 'Ngân sách', 'Tình trạng']
    orders = Order.query.all()
    #create_link = [url_for('admin.create_post'), "Tạo kho mới"]
    return render_template('admin/get_posts.html', table_header=table_header, orders=orders)


@admin.route('/admin/orders/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['mod'])
def admin_get_order_detail(id):
    form = ChangeOrderStatusForm()
    choices = []
    orders_status = OrderStatus.query.all()
    order = Order.query.get(id)
    for order_status in orders_status:
        choices.append((order_status.name, order_status.name))
    form.status.choices = choices
    if form.validate_on_submit():
        order_status = OrderStatus.query.filter_by(
            name=form.status.data).first()
        order.belong_to_status = order_status
        db.session.commit()
        return redirect(url_for('admin.admin_get_order_detail', id=order.id))

    return render_template('admin/order_detail.html', order=order, form=form)


@admin.route('/admin/users/remove/<int:id>')
@requires_access_level(ACCESS['mod'])
def remove_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.get_users'))


@admin.route('/admin/orders/remove/<int:id>')
@requires_access_level(ACCESS['mod'])
def remove_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('admin.get_orders'))


@admin.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['mod'])
def edit_user(id):
    form = CreateUserForm()
    user = User.query.get(id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.phone_number = form.phone_number.data
        user.address = form.address.data
        user.email = form.email.data
        pw = form.password.data
        if pw:
            user.set_password(pw)
        db.session.commit()
        return redirect(url_for('admin.get_users'))
    form.name.data = user.name
    form.phone_number.data = user.phone_number
    form.email.data = user.email
    form.address.data = user.address
    return render_template('admin/create_user.html', form=form)


@admin.route('/admin/users/create', methods=['GET', 'POST'])
@requires_access_level(ACCESS['mod'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        email = form.email.data
        pw = form.password.data
        user = User(name=name, phone_number=phone_number,
                    address=address, email=email)
        user.set_password(pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.get_users'))
    return render_template('admin/create_user.html', form=form)
