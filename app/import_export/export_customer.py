from app.models.customer import Customer


def export_customer_json():
    """ Export all customer records to a JSON-compatible list
    of dictionaries.

    Returns:
        list: A list of dictionaries, each representing a customer record.
    """
    customers = Customer.query.all()
    customer_list = [{"id": customer.id,
                      "customer_name": customer.customer_name,
                      "customer_email": customer.customer_email,
                      "customer_phone": customer.customer_phone,
                      "frequentcy_pay": customer.frequentcy_pay,
                      "date": customer.date.isoformat()
                      } for customer in customers]

    return customer_list
