from app.models.product import Product


def export_product_json():
    products = Product.query.all()
    product_list = [{"id": product.id, "product_name": product.product_name,
                      "price": product.price,
                      "product_quantity": product.product_quantity,
                      "date": product.date.isoformat()} for product in products]
    
    return product_list
