from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import db, app, photos
from shop.admin.routes import mgmt_bp
from .models import Brand, Category, Product
from .forms import ProductForm
import secrets
import os

__productperpage = 8


def brands():
    brands = Brand.query.join(
        Product, (Brand.id == Product.brand_id)).all()
    return brands


def categories():
    categories = Category.query.join(
        Product, (Category.id == Product.category_id)).all()
    return categories

# for User end:


@app.route('/')
def home():
    page_num = request.args.get('page', 1, type=int)
    products = Product.query.filter(
        Product.stock > 0).paginate(page=page_num, per_page=__productperpage)
    print(brands)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories())


@app.route('/product/<int:id>')
def product_detail_page(id):
    product = Product.query.get_or_404(id)
    return render_template('products/detailpage.html', product=product, brands=brands(), categories=categories())


@app.route('/brand/<int:id>')
def products_by_brand(id):
    page_num = request.args.get('page', 1, type=int)
    product_for_brand = Product.query.filter_by(
        brand_id=id).paginate(page=page_num, per_page=__productperpage)
    return render_template('products/index.html', product_for_brand=product_for_brand, brands=brands(), categories=categories(), brand_id=id)


@app.route('/category/<int:id>')
def products_by_category(id):
    page_num = request.args.get('page', 1, type=int)
    # category = Category.query.filter_by(id=id).first_or_404()
    product_for_category = Product.query.filter_by(
        category_id=id).paginate(page=page_num, per_page=__productperpage)
    return render_template('products/index.html', product_for_category=product_for_category, brands=brands(), categories=categories(), category_id=id)


# for management end:


@mgmt_bp.route('/addbrand', methods=['GET', 'POST'])
def add_brand():
    if 'admin_email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('management.login'))
    if request.method == "POST":
        brandname = request.form.get('brand')
        brand = Brand(name=brandname)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {brandname} was added to your database', 'success')
        return redirect(url_for('management.add_brand'))
    return render_template('admin/addbrand.html', brands='brands')


@mgmt_bp.route('/addcategory', methods=['GET', 'POST'])
def add_category():
    if 'admin_email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('management.login'))
    if request.method == "POST":
        catname = request.form.get('category')
        cat = Category(name=catname)
        db.session.add(cat)
        db.session.commit()
        flash(f'The Category {catname} was added to your database', 'success')
        return redirect(url_for('management.add_category'))
    return render_template('admin/addbrand.html')


@mgmt_bp.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    if 'admin_email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = ProductForm(request.form)

    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand_id = request.form.get('brand_id')
        category_id = request.form.get('category_id')
        image_1 = photos.save(request.files.get('image_1'),
                              name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'),
                              name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'),
                              name=secrets.token_hex(10)+".")
        product = Product(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            colors=colors,
            description=description,
            brand_id=brand_id,
            category_id=category_id,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3
        )
        db.session.add(product)
        db.session.commit()
        flash(f'The product {name} has been added to yout database', 'success')
        return redirect(url_for('management.add_product'))

    return render_template('admin/addproduct.html', title="Add Product Page", form=form, brands=brands, categories=categories)


@mgmt_bp.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def update_brand(id):
    if 'admin_email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('management.login'))
    update_brand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        update_brand.name = brand
        db.session.commit()
        flash('The brand has been updated', 'success')
        return redirect(url_for('management.brands'))
    return render_template('admin/updatebrand.html', title='Update Brand Page', update_brand=update_brand)


@mgmt_bp.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def update_category(id):
    if 'admin_email' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    update_category = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        update_category.name = category
        db.session.commit()
        flash('The category has been updated', 'success')
        return redirect(url_for('management.categories'))
    return render_template('admin/updatebrand.html', title='Update Category Page', update_category=update_category)


@mgmt_bp.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    brand_id = request.form.get('brand_id')
    category_id = request.form.get('category_id')
    form = ProductForm(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.description = form.description.data
        product.brand_id = brand_id
        product.category_id = category_id
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
        return redirect(url_for('management.admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    return render_template('admin/updateproduct.html', form=form, brands=brands, categories=categories, product=product)


@mgmt_bp.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(
            f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('management.brands'))
    flash(
        f'The brand {brand.name} cannot be deleted', 'warning')
    return redirect(url_for('management.brands'))


@mgmt_bp.route('/deletecategory/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(
            f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('management.categories'))
    flash(
        f'The category {category.name} cannot be deleted', 'warning')
    return redirect(url_for('management.categories'))


@mgmt_bp.route('/deleteproduct/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
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
        return redirect(url_for('management.admin'))
    flash(
        f'The product {product.name} cannot be deleted', 'warning')
    return redirect(url_for('management.admin'))
