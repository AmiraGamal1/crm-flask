from app.models.customer import Customer


def export_customer_json():
    customers = Customer.query.all()
    customer_list = [{"id": customer.id, "customer_name": customer.customer_name,
                      "customer_email":customer.customer_email,
                      "customer_phone": customer.customer_phone,
                      "frequentcy_pay": customer.frequentcy_pay,
                      "date": customer.date.isoformat()} for customer in customers]

    return customer_list
