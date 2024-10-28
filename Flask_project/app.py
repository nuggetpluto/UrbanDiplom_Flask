from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from passlib.hash import sha256_crypt
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'killeu1501'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Продукты
products = [
    {
        "name": "Ключик",
        "description": "Это многофункциональный инструмент, который поможет вам в любых ремонтных работах.",
        "price": "100 руб",
        "image": "static/images/product1.jpg",
        "characteristics": {
            "material": "Высококачественная сталь",
            "weight": "200 г",
            "length": "15 см",
            "features": "Противоскользящая рукоятка, компактный дизайн"
        }
    },
    {
        "name": "Бегемот",
        "description": "Бегемоты — крупные травоядные млекопитающие, обитающие в водоемах и болотистых зонах Африки. Они являются одними из самых массивных сухопутных животных, взрослые особи могут достигать веса до нескольких тонн.",
        "price": "200 руб",
        "image": "static/images/product2.jpg",
        "characteristics": {
            "size_and_weight": "достигают веса до нескольких тонн",
            "head": "массивная голова с широким ртом и острыми клыками для кусания травы и водных растений",
            "skin": "тело покрыто толстой кожей, предотвращающей обезвоживание и защищающей от ультрафиолетовых лучей",
            "buoyancy": "имеют невероятную плавучесть для передвижения в воде с легкостью"
        }
    },
    {
        "name": "Макбук",
        "description": "Макбук — это стильный и мощный ноутбук от Apple, идеально подходящий для работы и развлечений.",
        "price": "1000 руб",
        "image": "static/images/product4.jpg",  # Убедитесь, что изображение доступно по этому пути
        "characteristics": {
            "processor": "Apple M1",
            "ram": "8 ГБ",
            "storage": "256 ГБ SSD"
        }
    },
    # Другие товары...
]


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверяем, существует ли уже пользователь с таким же именем пользователя
        existing_user_by_username = User.query.filter_by(username=username).first()
        if existing_user_by_username:
            flash('Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.')
            return redirect(url_for('register'))

        # Проверяем, существует ли уже пользователь с таким же email
        existing_user_by_email = User.query.filter_by(email=email).first()
        if existing_user_by_email:
            flash('Пользователь с таким email уже существует. Пожалуйста, используйте другой email.')
            return redirect(url_for('register'))

        hashed_password = sha256_crypt.hash(password)

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Регистрация успешна!')  # Добавлено сообщение о успешной регистрации
        return redirect(url_for('home'))  # Перенаправление на главную страницу

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
            flash('Ваш профиль был успешно обновлён.')  # Новое сообщение о обновлении профиля
        else:
            message = 'Профиль не был изменен.'

        flash(message)
        return redirect(url_for('profile'))

    return render_template('profile.html', name=current_user.username, email=current_user.email, message=message)


@app.route('/')
@login_required
def home():
    return render_template('index.html', products=products, title="Магазин")


@app.route('/product/<name>')
@login_required
def product(name):
    for prod in products:
        if prod['name'].lower() == name.lower():
            return render_template('product.html', product=prod, title=prod['name'])
    return render_template('product.html', title='Товар не найден')


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title="О нас")


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', products=products, title="Корзина")


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


@app.route('/admin/users')
@login_required
def view_users():
    if current_user.is_authenticated and current_user.username == 'admin':  # простой пример проверки на администратора
        users = User.query.all()
        return render_template('view_users.html', users=users)
    else:
        flash('Access denied.')
        return redirect(url_for('home'))


@app.route('/confirm/<token>')
def confirm_email(token):
    user = User.query.filter_by(reset_token=token).first()
    if user:
        user.email_confirmed = True
        user.reset_token = None
        db.session.commit()
        flash('Email confirmed successfully')
        return redirect(url_for('login'))
    else:
        flash('Invalid or expired token')
        return redirect(url_for('home'))


@app.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = sha256_crypt.hash(email)
            user.reset_token = token
            db.session.commit()
            flash('Password reset request processed')  # Замените на любой текст, который хотите
            return redirect(url_for('login'))
    return render_template('reset_request.html')


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user:
        flash('Invalid or expired token')
        return redirect(url_for('home'))

    if request.method == 'POST':
        password = request.form.get('password')
        user.password = sha256_crypt.hash(password)
        user.reset_token = None
        db.session.commit()
        flash('Password reset successfully')
        return redirect(url_for('login'))

    return render_template('reset_token.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
