from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets
import os


@app.route('/')
def home():
    products = Addproduct.query.filter(Addproduct.stock > 0)
    return render_template('products/index.html', products=products)


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        db.session.commit()
        flash('The brand has been updated', 'success')
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(
            f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('brands'))
    flash(
        f'The brand {brand.name} cannot be deleted', 'warning')
    return redirect(url_for('brands'))


@app.route('/deletecategory/<int:id>', methods=['GET', 'POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(
            f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('categories'))
    flash(
        f'The category {category.name} cannot be deleted', 'warning')
    return redirect(url_for('categories'))


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path,
                                   "static/images/"+product.image_1))
        except Exception as e:
            print(e)

        try:
            os.unlink(os.path.join(current_app.root_path,
                                   "static/images/"+product.image_2))
        except Exception as e:
            print(e)

        try:
            os.unlink(os.path.join(current_app.root_path,
                                   "static/images/"+product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(
            f'The product {product.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(
        f'The product {product.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))


@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        db.session.commit()
        flash('The category has been updated', 'success')
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title='Update Category Page', updatecategory=updatecategory)


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


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.description = form.description.data
        product.brand_id = brand
        product.category_id = category
        # update image_1, image_2 and image_3
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       "static/images/"+product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'),
                                              name=secrets.token_hex(10)+".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'),
                                              name=secrets.token_hex(10)+".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       "static/images/"+product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'),
                                              name=secrets.token_hex(10)+".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'),
                                              name=secrets.token_hex(10)+".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                                       "static/images/"+product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'),
                                              name=secrets.token_hex(10)+".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'),
                                              name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'The product has been updated', 'success')
        return redirect('/admin')

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)
