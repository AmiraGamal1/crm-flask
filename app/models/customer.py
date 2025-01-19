"""Customer modules to create table"""
from app.extensions import db
from datetime import datetime
import pytz


class Customer(db.Model):
    """ Customer model representing the 'customers' table in the database.

    Attributes:
        id (Integer): Primary key, unique identifier for each customer.
        customer_name (String): The name of the customer.
        customer_email (String): The email address of the customer.
        customer_phone (String): The phone number of the customer.
        frequentcy_pay (Integer): The number of times the customer has made
        payments.
        date (DateTime): The date when the customer record was created.

    Methods:
    __repr__(): Returns a string representation of the customer object.
    """
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(15))
    frequentcy_pay = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(pytz.UTC))

    def __repr__(self):
        """ Returns a string representation of the customer object.

        Returns:

            str: A string that includes the customer's name and email.
        """
        return ('<Customer name %r Email %r>'
                % self.customer_name % self.customer_email)


def add_customer(sale):
    """ Adds a new customer or updates
    an existing customer's payment frequency.

    Parameters:
        sale: The sale object containing customer details.
    Returns:
        str: A message if failure
    """
    existing_customer = Customer.query.filter_by(
        customer_email=sale.customer_email).first()
    if existing_customer:
        existing_customer.frequentcy_pay += 1
    else:
        new_customer = Customer(customer_name=sale.customer_name,
                                customer_email=sale.customer_email,
                                customer_phone=sale.customer_phone,
                                frequentcy_pay=1)
        db.session.add(new_customer)
    try:
        db.session.commit()
    except:
        return 'There was an issue adding new customer'
    return 'Customer added/updated successfully'


def get_customer(search):
    """ Searches for customers in the database using a search pattern.

    Parameters:
        search: The search string to look for in customer records.

    Returns:
        list: A list of customer objects matching the search criteria.
    """
    search_pattern = f"%{search}"
    results = Customer.query.filter(
        (Customer.id.like(search_pattern))
        | (Customer.customer_name.like(search_pattern))
        | (Customer.customer_email.like(search_pattern))
        | (Customer.customer_phone.like(search_pattern))
        | (Customer.date.like(search_pattern))
    ).all()
    return results
