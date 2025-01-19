from app.models.product import Product


def export_product_json():
    """ Export all product records to a JSON-compatible list
    of dictionaries.

    Returns:
        list: A list of dictionaries, each representing a product record.
    """
    products = Product.query.all()
    product_list = [{"id": product.id,
                     "product_name": product.product_name,
                     "price": product.price,
                     "product_quantity": product.product_quantity,
                     "date": product.date.isoformat()
                     } for product in products]

    return product_list
