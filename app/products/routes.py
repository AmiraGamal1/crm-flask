from flask import render_template
from flask import Flask, render_template, url_for, request, redirect
from flask_security import Security, SQLAlchemySessionUserDatastore, roles_accepted
from app.products import bp
from app.extensions import db


from app.models.product import Product, get_product


@bp.route('/view_product/', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def view_product():
    """view product table"""
    products = Product.query.order_by(Product.product_name).all()
    return render_template('products/view_product.html', products=products)

@bp.route('/search_product/', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor', 'supervisor')
def search_product():
    search = request.args.get('search', '')
    products = get_product(search)
    return render_template('products/search_product.html', products=products)

@bp.route('/add_product/', methods=['POST', 'GET'])
@roles_accepted('admin', 'editor')
def add_product():
    """add product"""
    if request.method == 'POST':
        product_name = request.form['product']
        price = request.form['price']
        product_quantity = request.form['quantity']
        existing_product = Product.query.filter_by(product_name=product_name).first()
        if existing_product:
            return "This product is already in the store, try update it!"
        new_product = Product(product_name=product_name, price=price,
                              product_quantity=product_quantity)
        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('products/view_product')
        except:
            return 'There was an error adding your product'
    else:
        return render_template('add_product.html')

@bp.route('/info_product/<int:id>', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def info_product(id):
    """info single product information"""
    product = Product.query.get_or_404(id)
    return render_template('products/info_product.html', product=product)

@bp.route('/delete_product/<int:id>')
@roles_accepted('admin', 'editor')
def delete_product(id):
    """delete single sale"""
    product_to_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('products/view_product')
    except:
        return 'delete error'
    
@bp.route('/update_product/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def update_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.product_name = request.form['product']
        product.price = request.form['price']
        product.product_quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('products/view_product')
        except:
            return 'db update error'
        
    else:
        return render_template('products/update_product.html', product=product)
