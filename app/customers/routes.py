from flask import render_template
from flask import Flask, render_template, request
from flask_security import Security, SQLAlchemySessionUserDatastore, roles_accepted
from app.customers import bp


from app.models.customer import Customer, get_customer


@bp.route('/view_customer/', methods=['GET'])
@roles_accepted('admin', 'editor', 'supervisor')
def view_customer():
    customers = Customer.query.order_by(Customer.date.desc()).all()
    return render_template('customers/view_customer.html', customers=customers)

@bp.route('/search_customer/', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor', 'supervisor')
def search_customer():
    search = request.args.get('search', '')
    customers = get_customer(search)
    return render_template('customers/search_customer.html', customers=customers)
