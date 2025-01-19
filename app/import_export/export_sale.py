from app.models.sale import Sale


def export_sale_json():
    """ Export all sale records to a JSON-compatible list of dictionaries.

    Returns:
        list: A list of dictionaries, each representing a sale record.
    """
    sales = Sale.query.all()
    sale_list = [{"id": sale.id,
                  "product_name": sale.product_name,
                  "product_quantity": sale.product_quantity,
                  "customer_name": sale.customer_name,
                  "customer_email": sale.customer_email,
                  "customer_phone": sale.customer_phone,
                  "user_name": sale.user_name,
                  "date": sale.date.isoformat()
                  } for sale in sales]

    return sale_list
