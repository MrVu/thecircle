from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, current_app
from flask_mail import Message
from .models import Post, requires_access_level, ACCESS, Deal
from .forms import ContactForm, InvestForm
from app import mail, db
from flask_login import current_user

main = Blueprint('main', __name__)

def send_email(subject, sender, recipients, text_body, user_name, user_email):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body + '\n' + 'From: ' + user_name + "\n" + 'Email: ' + user_email
    mail.send(msg)


@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    static_url = url_for('static', filename="")
    return render_template('main/business_index.html', posts=posts, static_url=static_url)


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['user'])
def post_detail(id):
    post = Post.query.get(id)
    form = InvestForm()
    if form.validate_on_submit():
        deal = Deal(belong_to_post=post, belong_to_user=current_user._get_current_object(), status='Chờ duyệt',
                    invest_money=int(form.invest_money.data))
        db.session.add(deal)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/post_detail.html', post=post, form=form)


@main.route('/about-us')
def about_us():
    return render_template('main/about_us.html')


@main.route('/contact-us', methods=['GET', 'POST'])
@requires_access_level(ACCESS['user'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(subject=form.subject.data, sender=current_app.config['ADMINS'][0],
                   recipients=['vuhoang17891@gmail.com'], text_body=form.content.data, user_name=form.name.data,
                   user_email=form.email.data)
        return redirect(url_for('main.index'))
    return render_template('main/contact_us.html', form=form)
