from flask import render_template, session, request, redirect, url_for, flash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shop.admin.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'sdfsdfsdwrt435342sdf'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# The following code is for getting rid of circular import
# Will modify later
if True:
    from shop.products import routes
    from shop.admin import routes
