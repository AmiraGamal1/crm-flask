from flask import render_template
from flask import render_template, url_for, request, redirect, Response
from flask_security import roles_accepted
from app.products import bp
from app.extensions import db
from flask import jsonify
import io, csv, json, os
from werkzeug.utils import secure_filename
from sqlalchemy import inspect



from app.models.product import Product, get_product
from app.import_export.export_product import export_product_json
from app.import_export.import_sale import allowed_file
from app.import_export.import_product import parse_products_csv_file, parse_products_json_file

@bp.route('/', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def index():
    """view product table"""
    products = Product.query.order_by(Product.product_name).all()
    return render_template('products/index.html', products=products)

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
            return redirect(url_for('products.index'))
        except:
            return 'There was an error adding your product'
    else:
        return render_template('products/add_product.html')

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
        return redirect(url_for('products.index'))
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
            return redirect(url_for('products.index'))
        except:
            return 'db update error'
        
    else:
        return render_template('products/update_product.html', product=product)
    
@bp.route('/download_products')
@roles_accepted('admin', 'editor')
def download_products():
    format = request.args.get('format')
    products_dict = export_product_json()

    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(products_dict[0].keys())
        for row in products_dict:
            writer.writerow(row.values())
        output.seek(0)
        response = Response(output, mimetype='test/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=products.csv'
    elif format == 'json':
        json_data = json.dumps(products_dict, indent=4)
        response = Response(json_data, mimetype='application/json')
        response.headers['Content-Disposition'] = 'attachment; filename=products.json'
    else:
        return "Invalid format", 400
    return response

@bp.route('/upload_product', methods=['POST', 'GET'])
@roles_accepted('admin', 'editor')
def upload_products():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        uploaded_file = request.files['file']
        if uploaded_file == '':
            return jsonify({"error": "No selected file"}), 400

        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            extention = filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join('uploads/', filename)
            uploaded_file.save(file_path)
            filename.rsplit('.', 1)[1].lower()
            if extention == 'json':
                msg = parse_products_json_file(file_path)
                return msg
            elif extention == 'csv':
                inspector = inspect(db.engine)
                msg = parse_products_csv_file(inspector, file_path)
                return msg
            else:
                pass
            return redirect(url_for('products.index'))
        else:
            return jsonify({"error": "File not allowed"}), 400
    return render_template('upload_product')
