# import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# Define the WSGI application object
app = Flask(__name__)

#custom filter on jinja2
@app.template_filter()
def thousand_seperator(val):
    val = int(val)
    return format(val , ',d').replace(",",".")
# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.main.views import main as main
from app.admin.views import admin as admin
from app.auth.views import auth as auth

# Register blueprint(s)
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(auth)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
