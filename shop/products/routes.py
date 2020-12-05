from flask import render_template, session, request, redirect, url_for, flash
from shop import db, app
from .models import Brand, Category


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
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
    if request.method == "POST":
        catname = request.form.get('category')
        cat = Category(name=catname)
        db.session.add(cat)
        db.session.commit()
        flash(f'The Category {catname} was added to your database', 'success')
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')
