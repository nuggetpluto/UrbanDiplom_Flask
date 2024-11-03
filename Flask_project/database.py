from models import db, Product


def add_product(name, price, description, image):
    new_product = Product(name=name, price=price, description=description, image=image)
    db.session.add(new_product)
    db.session.commit()


def get_all_products():
    return Product.query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def update_product(product_id, name, price, description, image):
    product = get_product_by_id(product_id)
    if product:
        product.name = name
        product.price = price
        product.description = description
        product.image = image
        db.session.commit()


def delete_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
