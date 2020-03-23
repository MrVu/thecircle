# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
development_database = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
production_database = 'sqlite:///' + os.path.join(BASE_DIR, 'thecircle.db')
DATABASE_CONFIG = {'development': development_database , 'production': production_database}
SQLALCHEMY_DATABASE_URI = DATABASE_CONFIG.get(os.environ.get('DATABASE'))
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app/static/img/')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ.get('SECRET_KEY')

# Secret key for signing cookies
SECRET_KEY = os.environ.get('SECRET_KEY')
ADMINS =['vuhoang17891@gmail.com']
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = 1
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
