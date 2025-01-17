from flask import render_template, request, redirect, url_for, Response, get_flashed_messages
from flask_security import roles_accepted
from app.sales import bp
from app.extensions import db
import csv
import io
import json
import os
from werkzeug.utils import secure_filename
from sqlalchemy import inspect
from flask import jsonify

from app.models.sale import Sale, get_sales
from app.import_export.export_sale import export_sale_json
from app.import_export.import_sale import allowed_file, parse_sales_json_file, parse_sales_csv_file
from app.models.product import Product
from app.models.customer import add_customer


@bp.route('/', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def index():
    """view Sale table"""
    sales = Sale.query.order_by(Sale.date.desc()).all()
    return render_template('sales/index.html', sales=sales)

@bp.route('/search_sale/', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor', 'supervisor')
def search_sale():
    search = request.args.get('search', '')
    sales = get_sales(search)
    return render_template('sales/search_sale.html', sales=sales)


@bp.route('/add_sale/', methods=['POST', 'GET'])
@roles_accepted('admin', 'editor')
def add_sale():
    """add new sale"""
    if request.method == 'POST':
        error = ""
        product = request.form['product']
        quantity = request.form['quantity']
        customer = request.form['customer']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        user = request.form['user']
        prod = Product.query.filter_by(product_name=product).first()
        if prod:
            if prod.product_quantity < int(quantity):
                error = 'Not enough quantity'
            else:
                prod.product_quantity -= int(quantity)
                try:
                    db.session.commit()
                except:
                    return 'There was an issue updating product quantity'
        else:
            error = 'Product not found'
        if error:
            return render_template('add_sale.html', product=product,
                                   quantity=quantity, customer=customer,
                                   customer_email=customer_email,
                                   customer_phone=customer_phone,
                                   user=user, error=error)
        new_sale = Sale(product_name=product, product_quantity=quantity,
                        customer_name=customer, customer_email=customer_email,
                        customer_phone=customer_phone, user_name=user)
        try:
            db.session.add(new_sale)
            db.session.commit()
            add_customer(new_sale)
            return redirect(url_for('sales.index'))
        except:
            return 'There was an issue adding your sale information'
    else:
        return render_template('sales/add_sale.html')


@bp.route('/info_sale/<int:id>', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def info_sale(id):
    """view single sale information"""
    sale = Sale.query.get_or_404(id)
    return render_template('sales/info_sale.html', sale=sale)


@bp.route('/delete_sale/<int:id>')
@roles_accepted('admin', 'editor')
def delete_sale(id):
    """delete single sale"""
    sale_to_delete = Sale.query.get_or_404(id)

    try:
        db.session.delete(sale_to_delete)
        db.session.commit()
        return redirect(url_for('sales.index'))
    except:
        return 'delete error'

@bp.route('/update_sale/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def update_sale(id):
    sale = Sale.query.get_or_404(id)
    if request.method == 'POST':
        product = request.form['product']
        quantity = request.form['quantity']
        sale.customer_name = request.form['customer']
        sale.user_name = request.form['user']
        prod = Product.query.filter_by(product_name=product).first()
        if prod:
            if prod.product_quantity < int(quantity):
                error = 'Not enough quantity'
            else:
                prod.product_quantity += sale.product_quantity
                prod.product_quantity -= int(quantity)
                sale.product_name = product
                sale.product_quantity = quantity
                try:
                    db.session.commit()
                    return redirect(url_for('sales.index'))
                except:
                    return 'db update error'
        else:
            error = 'Product not found'
        return render_template('sales/update_sale.html', sale=sale, error=error)
    else:
        return render_template('sales/update_sale.html', sale=sale)

@bp.route('/download_sales')
@roles_accepted('admin')
def download_sales():
    format = request.args.get('format')
    sales_dict = export_sale_json()

    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(sales_dict[0].keys())
        for row in sales_dict:
            writer.writerow(row.values())
        output.seek(0)
        response = Response(output, mimetype='test/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=sales.csv'
    elif format == 'json':
        json_data = json.dumps(sales_dict, indent=4)
        response = Response(json_data, mimetype='application/json')
        response.headers['Content-Disposition'] = 'attachment; filename=sales.json'
    else:
        return "Invalid format", 400
    return response

@bp.route('/upload_sales', methods=['POST', 'GET'])
@roles_accepted('admin', 'editor')
def upload_sales():
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
                msg = parse_sales_json_file(file_path)
                return msg
            elif extention == 'csv':
                inspector = inspect(db.engine)
                return parse_sales_csv_file(inspector, file_path)
            else:
                pass
            return redirect(url_for('sales.index'))
        else:
            return jsonify({"error": "File not allowed"}), 400
    return render_template('upload_sales')

