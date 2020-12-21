from flask import render_template, session, request, redirect, url_for, flash, current_app, make_response
from flask_login import login_required, current_user, login_user, logout_user
from shop import db, app, photos, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Customer, CustomerOrder
import secrets
import os
import pdfkit
import stripe

publishable_key = "pk_test_51I0C4HIkH6gk0430apoX6NH50LHEQZ5F1djym6q6z3Tkz8BsdolyHepme6ZWQSCNnCzz7EBLFeyWkYtcf1svh7s3005HvTSZsM"
stripe.api_key = "sk_test_51I0C4HIkH6gk0430YCxMf811TjxmJt1YJB285qveWyWUQOPxGALRHYgJkmU3t222t2aijhb9y0gMCPD0X7saLj8H00R6BQyUAn"


@app.route('/payment', methods=["POST"])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Shichen\'s shop',
        amount=amount,
        currency='cad',
    )
    order = CustomerOrder.query.filter_by(
        customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    order.status = "Paid"
    db.session.commit()
    flash('We received your payment. The order is completed, thank you!', 'success')
    return redirect(url_for('order_status', invoice=invoice))


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        customer = Customer(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
            country=form.country.data,
            state=form.state.data,
            contact=form.contact.data,
            city=form.city.data,
            address=form.address.data,
            zipcode=form.zipcode.data,
        )
        db.session.add(customer)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for("customer_login"))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['Get', 'POST'])
def customer_login():
    form = CustomerLoginForm()
    if request.method == "POST":
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in.', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        else:
            flash(f'incorrect email and password', 'danger')
            print('incorrect email and password')
            return redirect(url_for('customer_login'))

    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


def trim_product_info_in_cart():
    for _key, product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']
        del product['colors']
    return trim_product_info_in_cart


@app.route('/getorder')
@login_required
def create_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        trim_product_info_in_cart()
        try:
            order = CustomerOrder(
                invoice=invoice,
                customer_id=customer_id,
                purchased_items=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Please make the payment to finish this order', 'success')
            return redirect(url_for('order_status', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong while getting order', 'danger')
            return redirect(url_for('get_cart'))


@app.route('/orders/<invoice>')
@login_required
def order_status(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Customer.query.filter_by(id=customer_id).first()
        order = CustomerOrder.query.filter_by(
            invoice=invoice).first()
        for _key, product in order.purchased_items.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
        tax = float("%.2f" % (0.06 * float(subTotal)))
        grandTotal = str("%.2f" % float(subTotal + tax))
        return render_template(
            'customer/order.html',
            invoice=invoice,
            tax=tax,
            subTotal=subTotal,
            grandTotal=grandTotal,
            customer=customer,
            order=order
        )
    else:
        return redirect(url_for('customer_login'))


@app.route('/orders/<invoice>/pdf', methods=['POST'])
@login_required
def generate_invoice_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id

        customer = Customer.query.filter_by(id=customer_id).first()
        order = CustomerOrder.query.filter_by(
            invoice=invoice).first()

        for _key, product in order.purchased_items.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
        tax = float("%.2f" % (0.06 * float(subTotal)))
        grandTotal = str("%.2f" % (1.06 * float(subTotal)))

        rendered = render_template(
            'customer/pdf.html',
            invoice=invoice,
            tax=tax,
            grandTotal=grandTotal,
            customer=customer,
            order=order
        )
        pdf = pdfkit.from_string(rendered, False)
        response = make_response(pdf)
        response.headers['content-Type'] = 'application/pdf'
        response.headers['content-Disposition'] = 'attached; filename=' + \
            invoice+'.pdf'
        return response
    return request(url_for('order_status'))
