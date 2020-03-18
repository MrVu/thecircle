# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField, FileField, TextAreaField, SelectField  # BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class ContactForm(Form):
    name = StringField('Tên')
    email = StringField('Email')
    subject = StringField('Tiêu đề')
    content = TextAreaField('Nội dung')


class InvestForm(Form):
    invest_money = SelectField('Chọn số tiền góp vốn: ',
                               choices=[('2000000', '2.000.000 VND'), ('3000000', '3.000.000 VND'),
                                        ('5000000', '5.000.000 VND'), ('8000000', '8.000.000 VND')])
