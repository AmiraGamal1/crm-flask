"""Product modules to create table"""
from app.extensions import db
from datetime import datetime
import pytz


class Product(db.Model):
    """Product model representing the 'products' table in the database.

    Attributes:
        id (Integer): Primary key, unique identifier for each product.
        product_name (String): The name of the product.
        price (Integer): The price of the product.
        product_quantity (Integer): The quantity of the product available.
        date (DateTime): The date when the product record was created.

    Methods: __repr__():
        Returns a string representation of the product object.
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(pytz.UTC))

    def __repr__(self):
        """Returns a string representation of the product object.

        Returns:
            str: A string that includes the product's name and price.
        """
        return ('<Product name %r Price %r>'
                % self.product_name % self.price)


def get_product(search):
    """Searches for products in the database using a search pattern.

    Parameters:
        search: The search string to look for in product records.

    Returns:
        list: A list of product objects matching the search criteria.
    """
    search_pattern = f"%{search}"
    results = Product.query.filter(
        (Product.id.like(search_pattern))
        | (Product.product_name.like(search_pattern))
        | (Product.price.like(search_pattern))
    ).all()
    return results
