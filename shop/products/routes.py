from flask import render_template, session, request, redirect, url_for, flash
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        brandname = request.form.get('brand')
        brand = Brand(name=brandname)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {brandname} was added to your database', 'success')
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        catname = request.form.get('category')
        cat = Category(name=catname)
        db.session.add(cat)
        db.session.commit()
        flash(f'The Category {catname} was added to your database', 'success')
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'),
                              name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'),
                              name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'),
                              name=secrets.token_hex(10)+".")
        product = Addproduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            colors=colors,
            description=description,
            brand_id=brand,
            category_id=category,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3
        )
        db.session.add(product)
        db.session.commit()
        flash(f'The product {name} has been added to yout database', 'success')
        return redirect(url_for('addproduct'))

    return render_template('products/addproduct.html', title="Add Product Page", form=form, brands=brands, categories=categories)
