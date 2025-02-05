from app.main import bp
from flask import render_template
from app.models.sale import Sale
from app.models.product import Product
from app.models.customer import Customer
from app.models.user import User
from flask_login import login_required
from flask_security import roles_accepted


@bp.route('/', methods=['GET'])
@login_required
@roles_accepted('admin', 'editor', 'supervisor')
def index():
    """ Display the main dashboard with various counts.

    Methods:
        GET: Retrieve and display counts for users, customers,
        products, and sales.

    Returns:
        Template: Render the main/index.html template with the counts
        data.
    """
    user_count = User.query.count()
    customer_count = Customer.query.count()
    product_count = Product.query.count()
    sale_count = Sale.query.count()
    data = {
        'sale_count': sale_count,
        'customer_count': customer_count,
        'product_count': product_count,
        'user_count': user_count
    }
    return render_template('main/index.html', data=data)
