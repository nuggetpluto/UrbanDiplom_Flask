from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from database import get_all_products
from models import Product, db

product_bp = Blueprint('product', __name__)


@product_bp.route('/')
@login_required
def home():
    products = get_all_products()  # Получаем список продуктов
    return render_template('index.html', products=products, title="Магазин")


@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image = request.form.get('image')

        new_product = Product(name=name, description=description, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()

        flash('Продукт успешно добавлен!')
        return redirect(url_for('product.home'))

    return render_template('add_product.html')


from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user


@product_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = {}  # Пример, нужно получить актуальные данные корзины
    if request.method == 'POST':
        # Получаем данные из формы
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')
        cart = request.form.get('cart')  # Получаем данные о корзине

        # Здесь можно добавить обработку данных заказа (например, сохранение в базе данных)

        # Очищаем корзину после оформления заказа (если это нужно)
        # Это зависит от того, как вы храните корзину (в сессии, в локальном хранилище и т.д.)

        # Перенаправляем на страницу подтверждения заказа
        return redirect(url_for('product.order_confirmation'))

    # Для GET запроса отображаем форму оформления заказа
    return render_template('checkout.html', cart=cart)


@product_bp.route('/order_confirmation', methods=['GET'])
@login_required
def order_confirmation():
    return render_template('order_confirmation.html')


@product_bp.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product, title=product.name)
