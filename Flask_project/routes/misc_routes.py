from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from database import get_all_products

misc_bp = Blueprint('misc', __name__)


@misc_bp.route('/about')
@login_required
def about():
    return render_template('about.html', title="О нас")


@misc_bp.route('/cart')
@login_required
def cart():
    # Получаем все продукты
    products = get_all_products() or []

    # Преобразуем объекты Product в словари
    products_serializable = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image': product.image
        }
        for product in products
    ]

    return render_template('cart.html', title="Корзина", products=products_serializable)


@misc_bp.route('/contact')
@login_required
def contact():
    return render_template('contact.html', title="Контакты")


@misc_bp.route('/support')
@login_required
def support():
    return render_template('support.html', title="Поддержка")



