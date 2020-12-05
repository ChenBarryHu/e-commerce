
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
if True:
    from shop.products import routes


@app.route('/')
def home():
    return render_template('admin/index.html', title='Admin Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    from shop.admin.models import User
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(
            password=form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    from shop.admin.models import User
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {user.name}, you are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('wrong password, please try again', 'danger')
    return render_template('admin/login.html', form=form, title='Login Page')
