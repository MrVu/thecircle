# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField, FileField, TextAreaField, SelectField  # BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileRequired


# Define the login form (WTForms)

class CreatePostForm(FlaskForm):
    category = SelectField('Post Category', choices=[('Mỹ Phẩm', 'Mỹ Phẩm'), ('Thời Trang', 'Thời Trang')])
    title = StringField('Title')
    description_text = StringField('Short Description')
    interest = StringField('Interest')
    min_money = StringField('Minimum money to deal')
    level = SelectField('Mức giá',
                        choices=[('Nhà phân phối', 'Phân phối'), ('Đại lý 1', 'Đại lý 1'), ('Đại lý 2', 'Đại lý 2'),
                                 ('Bán lẻ', 'Bán lẻ')])
    detail = TextAreaField('Detail Description')


class CreateUserForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField(('Password'))
    phone_number = StringField('Phone Number')
    address = StringField('Address')

class UpdateDealForm(FlaskForm):
    status = SelectField('Tình trạng', choices=[('Chờ duyệt', 'Chờ duyệt'), ('Đã xác nhận', 'Đã xác nhận'), ('Hoàn thành', 'Hoàn thành')])


class AdminLoginForm(FlaskForm):
    email = StringField(('Username'), validators=[DataRequired()])
    password = PasswordField(('Password'), validators=[DataRequired()])
