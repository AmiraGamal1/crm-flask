
from flask import render_template, Response, jsonify
from flask import render_template, request
from flask_security import roles_accepted
from app.customers import bp
import io
import csv
import json
from app.import_export.export_customer import export_customer_json
from app.models.customer import Customer, get_customer


@bp.route('/', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def index():
    """ Display the list of customers.

    Methods:
        GET: Retrieve and display all customer records, ordered by date
          in descending order.

    Returns:
        Template: Render the customers/index.html template with customer data.
    """
    customers = Customer.query.order_by(Customer.date.desc()).all()
    return render_template('customers/index.html', customers=customers)


@bp.route('/search_customer/', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor', 'supervisor')
def search_customer():
    """ Search for customers based on a search string.

    Methods:
        GET/POST: Retrieve and display customer records that match the
        search criteria.

    Returns:
        Template: Render the customers/search_customer.html
        template with search results.
    """
    search = request.args.get('search', '')
    customers = get_customer(search)
    return render_template('customers/search_customer.html',
                           customers=customers)


@bp.route('/download_customers')
@roles_accepted('admin')
def download_customers():
    """ Download customer data in the specified format (CSV or JSON).

    Methods:
        GET: Retrieve customer data and export it in the specified format.

    Returns:
        Response: A response containing the customer data file for download.
    """
    format = request.args.get('format')
    customers_dict = export_customer_json()

    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(customers_dict[0].keys())
        for row in customers_dict:
            writer.writerow(row.values())
        output.seek(0)
        response = Response(output, mimetype='test/csv')
        response.headers['Content-Disposition'] = 'attachment; \
            filename=customers.csv'
    elif format == 'json':
        json_data = json.dumps(customers_dict, indent=4)
        response = Response(json_data, mimetype='application/json')
        response.headers['Content-Disposition'] = 'attachment; \
            filename=customers.json'
    else:
        return jsonify("Invalid format"), 400
    return response
