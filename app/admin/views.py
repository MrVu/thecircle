from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, current_app
from flask_login import login_user, logout_user, current_user
from .forms import CreatePostForm, AdminLoginForm, CreateUserForm, UpdateDealForm
from app.main.models import Post, User, requires_access_level, ACCESS, Deal
from werkzeug.utils import secure_filename
from app import db

admin = Blueprint('admin', __name__)

"""
@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin/', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.get_posts'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.admin_login'))
        login_user(user)
        return redirect(url_for('admin.get_posts'))
    return render_template('admin/admin_login.html', form=form)
"""


@admin.route('/admin/users')
@requires_access_level(ACCESS['admin'])
def get_users():
    table_header = ['Tên', 'Email', 'Địa chỉ', 'Điện thoại']
    create_link = [url_for('admin.create_user'), "Tạo người dùng"]
    users = User.query.all()
    return render_template('admin/get_posts.html', users=users, table_header=table_header, create_link = create_link)


@admin.route('/admin/users/<int:id>')
@requires_access_level(ACCESS['admin'])
def admin_get_user_profile(id):
    table_header = ['Sản phẩm', 'Tiền đầu tư', 'Tình trạng']
    user = User.query.get(id)
    return render_template('admin/user_profile.html', user=user, table_header=table_header)


@admin.route('/admin/deals')
@requires_access_level(ACCESS['admin'])
def get_deals():
    table_header = ['Tiêu đề', 'Khách hàng', 'Số tiền', 'Tình trạng']
    deals = Deal.query.all()
    return render_template('admin/get_posts.html', deals=deals, table_header=table_header)


@admin.route('/admin/deals/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def get_deal_detail(id):
    deal = Deal.query.get(id)
    table_header = ['Tiêu đề', 'Số tiền', 'Tình trạng']
    form = UpdateDealForm()
    if form.validate_on_submit():
        deal.status = form.status.data
        db.session.commit()
        return redirect(url_for('admin.get_deal_detail', id= deal.id))
    return render_template('/admin/deal_detail.html', deal=deal, table_header= table_header, form=form)


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin/', methods=['GET', 'POST'])
@admin.route('/admin/posts')
@requires_access_level(ACCESS['admin'])
def get_posts():
    table_header = ['Tiêu đề', 'Mô tả', 'Tổng tiền', 'Số khách hàng']
    create_link = [url_for('admin.create_post'), "Tạo kho mới"]
    posts = Post.query.all()
    return render_template('admin/get_posts.html', posts=posts, table_header=table_header, create_link= create_link)


"""
@admin.route('/admin/logout')
@requires_access_level(ACCESS['admin'])
def admin_logout():
    logout_user()
    return redirect(url_for('main.index'))
"""


@admin.route('/admin/users/remove/<int:id>')
@requires_access_level(ACCESS['admin'])
def remove_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.get_posts'))


@admin.route('/admin/deals/remove/<int:id>')
@requires_access_level(ACCESS['admin'])
def remove_deal(id):
    deal = Deal.query.get(id)
    db.session.delete(deal)
    db.session.commit()
    return redirect(url_for('admin.get_posts'))


@admin.route('/admin/posts/remove/<int:id>')
@requires_access_level(ACCESS['admin'])
def remove_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin.get_posts'))


@admin.route('/admin/posts/edit/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def edit_post(id):
    post = Post.query.get(id)
    form = CreatePostForm()

    if form.validate_on_submit():
        post.level = form.level.data
        post.interest = form.interest.data
        post.min_money = form.min_money.data
        post.category = form.category.data
        post.title = form.title.data
        post.description_text = form.description_text.data
        post.detail = form.detail.data
        post.set_service_fee(form.interest.data)
        db.session.commit()
        return redirect(url_for('admin.get_posts'))
    form.min_money.data = post.min_money
    form.interest.data = post.interest
    form.level.data = post.level
    form.category.data = post.category
    form.title.data = post.title
    form.description_text.data = post.description_text
    form.detail.data = post.detail
    return render_template('admin/create_post.html', form=form)


@admin.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
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
        return redirect(url_for('admin.get_posts'))
    form.name.data = user.name
    form.phone_number.data = user.phone_number
    form.email.data = user.email
    form.address.data = user.address
    return render_template('admin/create_user.html', form=form)


@admin.route('/admin/posts/create', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        category = form.category.data
        min_money = form.min_money.data
        interest = form.interest.data
        level = form.level.data
        title = form.title.data
        description_text = form.description_text.data
        detail = form.detail.data
        post = Post(title=title, description_text=description_text,
                    detail=detail, category=category, level=level, min_money=min_money, interest=interest)
        post.set_service_fee(interest)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.get_posts'))
    return render_template('admin/create_post.html', form=form)


@admin.route('/admin/users/create', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        email = form.email.data
        pw = form.password.data
        user = User(name=name, phone_number=phone_number, address=address, email=email)
        user.set_password(pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.get_posts'))
    return render_template('admin/create_user.html', form=form)
