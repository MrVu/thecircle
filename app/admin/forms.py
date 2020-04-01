# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField, FileField, TextAreaField, SelectField  # BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileRequired


# Define the login form (WTForms)

class ChangeOrderStatusForm(FlaskForm):
    status = SelectField()


class CreateUserForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField(('Password'))
    phone_number = StringField('Phone Number')
    address = StringField('Address')


class AdminLoginForm(FlaskForm):
    email = StringField(('Username'), validators=[DataRequired()])
    password = PasswordField(('Password'), validators=[DataRequired()])
