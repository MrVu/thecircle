from app import db
from app.main.models import User, Category, OrderStatus
print('Chọn 1 trong những lựa chọn sau: ')
print('1.Thêm Category')
print('2.Thêm User')
print('3.Thêm tình trạng đơn hàng')
choice = input('Lựa chọn: ')
if int(choice) == 2:
    name = input('User name: ')
    email = input('User email: ')
    phone_number = input('Phone number: ')
    address = input('Address: ')
    password = input('Password: ')
    user = User(name=name, email=email,
                phone_number=phone_number, address=address)
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
elif int(choice) == 1:
    category_list = ['Thời trang', 'Mỹ phẩm', 'Thiết kế', 'Khác']
    for category in category_list:
        new_category = Category(name=category)
        db.session.add(new_category)
        db.session.commit()
    print('Đã thêm category mẫu')
elif int(choice) == 3:
    order_status_list = ['Chờ xác nhận', 'Đã xác nhận',
                         'Đang tiến hành', 'Đã hoàn thành', 'Hủy']
    for order_status in order_status_list:
        new_status = OrderStatus(name=order_status)
        db.session.add(new_status)
        db.session.commit()
    print('Đã thêm status mẫu')
