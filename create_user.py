from app import db
from app.main.models import User
name = input('User name: ')
email = input('User email: ')
phone_number = input('Phone number: ')
address = input('Address: ')
password = input('Password: ')
user = User(name= name, email= email, phone_number= phone_number, address=address)
user.set_password(password)
access_level = input('Access level: ')
access_level = int(access_level)
if access_level == 2:
    user.set_mod()
elif access_level == 3:
    user.set_admin()
else:
    print('Normal user')
db.session.add(user)
db.session.commit()
