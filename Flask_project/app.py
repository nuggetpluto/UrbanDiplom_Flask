from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from passlib.hash import sha256_crypt
from flask_migrate import Migrate
from models import User, Product, db
from database import add_product, get_all_products, update_product, delete_product

app = Flask(__name__)
app.config['SECRET_KEY'] = 'killeu1501'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user_by_username = User.query.filter_by(username=username).first()
        if existing_user_by_username:
            flash('Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.')
            return redirect(url_for('register'))

        existing_user_by_email = User.query.filter_by(email=email).first()
        if existing_user_by_email:
            flash('Пользователь с таким email уже существует. Пожалуйста, используйте другой email.')
            return redirect(url_for('register'))

        hashed_password = sha256_crypt.hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Регистрация успешна!')
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and sha256_crypt.verify(password, user.password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    message = None
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        changes = []
        if current_user.username != new_username:
            current_user.username = new_username
            changes.append(f'ваше новое имя пользователя: {new_username}')
        if current_user.email != new_email:
            current_user.email = new_email
            changes.append(f'ваша новая электронная почта: {new_email}')
        if new_password:
            current_user.password = sha256_crypt.hash(new_password)
            changes.append('ваш новый пароль был обновлен')

        db.session.commit()

        if changes:
            message = 'Профиль успешно изменен: ' + ', '.join(changes)
            flash('Ваш профиль был успешно обновлён.')
        else:
            message = 'Профиль не был изменен.'

        flash(message)
        return redirect(url_for('profile'))

    return render_template('profile.html', name=current_user.username, email=current_user.email, message=message)


@app.route('/')
@login_required
def home():
    products = get_all_products()  # Получаем список продуктов
    return render_template('index.html', products=products, title="Магазин")


@app.route('/product/<name>')
@login_required
def product(name):
    products = get_all_products()
    for prod in products:
        if prod.name.lower() == name.lower():
            return render_template('product.html', product=prod, title=prod.name)
    return render_template('product.html', title='Товар не найден')


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title="О нас")


@app.route('/cart')
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


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html', title="Контакты")


@app.route('/support')
@login_required
def support():
    return render_template('support.html', title="Поддержка")


@app.route('/api/data', methods=['POST'])
@login_required
def get_data():
    data = request.json
    response = {"message": "Data received", "data": data}
    return jsonify(response)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image = request.form.get('image')

        # Создание и добавление нового продукта в базу данных
        new_product = Product(name=name, description=description, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()

        flash('Продукт успешно добавлен!')
        return redirect(url_for('home'))  # Перенаправление на главную страницу

    return render_template('add_product.html')  # Показать форму при GET-запросе


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
