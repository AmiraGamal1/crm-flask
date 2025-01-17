import json
from flask import jsonify
from app.models.sale import Sale
from app.extensions import db
from app.models.product import Product
import pandas as pd
from app.import_export.import_sale import validate_sales_csv_file



def validate_products_json_file(data):
    for item in data:
        if 'product_name'  not in item or \
            'product_quantity' not in item or 'price' not in item:
            return False, jsonify("missing columns")
        if  not isinstance(item['product_name' ], str) or \
             not isinstance(item['product_quantity'], int) or \
                not isinstance(item['price'], int):
            return False, jsonify("data type error")
    return True, None

def parse_products_json_file(file_path):
    try:
        with open(file_path) as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno} (char {e.pos})"})
    stat, mesg = validate_products_json_file(data)
    if not stat:
        return mesg    
    for item in data:
        prod = Product.query.filter_by(product_name=item['product_name']).first()
        if prod:
            prod.product_quantity += item['product_quantity']
            prod.price = item['price']
            try:
                db.session.commit()
            except: 
                return jsonify({"error":'There was an issue updating product quantity'})
        else:
            product = Product(product_name=item['product_name'], product_quantity=item['product_quantity'], price=item['price'])
            try:
                db.session.add(product)
                db.session.commit()
            except:
                return jsonify({"error": "database error"})
    return jsonify({"message": "Products added successfully"})

def validate_products_csv_file(inspector ,table, csvData):
    columns = inspector.get_columns(table)
    db_columns = {col['name']: str(col['type'])  for col in columns if col['name'] != 'id' and col['name'] != 'date'}
    missing_columns = [col for col in db_columns if col not in csvData.columns]
    if missing_columns:
        return False, jsonify({"missing columns": missing_columns})
    try:
        csvData['product_quantity'].apply(int)
    except ValueError:
        return False, jsonify({"incorrect data type": f"data type of product_quantity is Integer put fount {type(csvData['product_quantity'].iloc[0]).__name__}"})
    try:
        csvData['price'].apply(int)
    except ValueError:
        return False, jsonify({"incorrect data type": f"data type of price is Integer put fount {type(csvData['price'].iloc[0]).__name__}"})
    return True, None

def parse_products_csv_file(inspector, file_path):
    csvData = pd.read_csv(file_path)
    stat, mesg = validate_sales_csv_file(inspector,'product', csvData)
    if not stat:
        return mesg
    for i, row in csvData.iterrows():
        prod = Product.query.filter_by(product_name=row['product_name']).first()
        if prod:
            prod.product_quantity += row['product_quantity']
            prod.price = row['price']
            try:
                db.session.commit()
            except:
                return jsonify({"error":'There was an issue updating product quantity'})
        else:
            product = Product(product_name=row['product_name'], product_quantity=row['product_quantity'], price=row['price'])
            try:
                db.session.add(product)
                db.session.commit()
            except:
                return jsonify({"error": "database error"})
    return jsonify({"message": "Products added successfully"})
