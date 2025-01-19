"""sale modules to create table"""
from app.extensions import db
from datetime import datetime
import pytz


class Sale(db.Model):
    """Sale model representing the 'sales' table in the database.

    Attributes:
        id (Integer): Primary key, unique identifier for each sale.
        product_name (String): The name of the product sold.
        product_quantity (Integer): The quantity of the product sold.
        customer_name (String): The name of the customer.
        customer_email (String): The email address of the customer.
        customer_phone (String): The phone number of the customer.
        user_name (String): The name of the user who processed the sale.
        date (DateTime): The date when the sale record was created.

    Methods: __repr__():
    Returns a string representation of the sale object.
    """
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(15))
    user_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(pytz.UTC))

    def __repr__(self):
        """Returns a string representation of the sale object.

        Returns:
            str: A string that includes the sale's ID and product name.
        """
        return ('<sale id %r product name %r>'
                % self.id % self.product_name)


def get_sales(search):
    """Searches for sales in the database using a search pattern.

    Parameters:
        search: The search string to look for in sale records.

    Returns:
        list: A list of sale objects matching the search criteria.
    """
    search_pattern = f"%{search}"
    results = Sale.query.filter(
        (Sale.id.like(search_pattern))
        | (Sale.product_name.like(search_pattern))
        | (Sale.customer_name.like(search_pattern))
        | (Sale.customer_email.like(search_pattern))
        | (Sale.user_name.like(search_pattern))
        | (Sale.date.like(search_pattern))
    ).all()
    return results
