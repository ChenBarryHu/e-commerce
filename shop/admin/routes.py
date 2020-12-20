from flask import render_template, session, request, redirect, url_for, flash, Blueprint
from .forms import RegistrationForm, LoginForm
from .models import Admin
from shop import app, bcrypt, db
from shop.products.models import Addproduct, Brand, Category

import os

mgmt_bp = Blueprint('management', __name__, url_prefix='/management')


@mgmt_bp.route('/')
def admin():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('management.login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)


@mgmt_bp.route('/brands')
def brands():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('management.login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brands.html', title='Brands Page', brands=brands)


@mgmt_bp.route('/categories')
def categories():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('management.login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brands.html', title='categories Page', categories=categories)


@mgmt_bp.route('/register', methods=['GET', 'POST'])
def register():
    from shop.admin.models import Admin
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(
            password=form.password.data)
        admin = Admin(name=form.name.data, username=form.username.data, email=form.email.data,
                      password=hash_password)
        db.session.add(admin)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering', 'success')
        return redirect(url_for('management.admin'))
    return render_template('admin/register.html', form=form, title="Registration Page")


@mgmt_bp.route('/login', methods=['GET', 'POST'])
def login():
    from shop.admin.models import Admin
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {admin.name}, you are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('management.admin'))
        else:
            flash('wrong password, please try again', 'danger')
    return render_template('admin/login.html', form=form, title='Login Page')


@mgmt_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email')
    return redirect(request.args.get('next') or url_for('management.admin'))
