# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField, FileField, TextAreaField, SelectField  # BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class ContactForm(FlaskForm):
    name = StringField('Tên')
    email = StringField('Email')
    subject = StringField('Tiêu đề')
    content = TextAreaField('Nội dung')


class OrderForm(FlaskForm):
    category = SelectField('Lĩnh vực ')
    name = StringField('Tên vị trí cần tuyển dụng')
    detail = TextAreaField('Thông tin chi tiết')
    budget = StringField('Ngân sách dự kiến')
