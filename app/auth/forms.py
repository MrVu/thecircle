# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField, FileField, TextAreaField, SelectField  # BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileRequired

class LoginForm(Form):
    email = StringField(('Username'), validators=[DataRequired()])
    password = PasswordField(('Password'), validators=[DataRequired()])
