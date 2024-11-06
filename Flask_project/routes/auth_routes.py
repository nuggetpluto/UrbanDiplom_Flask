from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from passlib.hash import sha256_crypt
from models import User, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user_by_username = User.query.filter_by(username=username).first()
        if existing_user_by_username:
            flash('Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.')
            return redirect(url_for('auth.register'))

        existing_user_by_email = User.query.filter_by(email=email).first()
        if existing_user_by_email:
            flash('Пользователь с таким email уже существует. Пожалуйста, используйте другой email.')
            return redirect(url_for('auth.register'))

        hashed_password = sha256_crypt.hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Регистрация успешна!')
        return redirect(url_for('product.home'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and sha256_crypt.verify(password, user.password):
            login_user(user)
            return redirect(url_for('product.home'))
        else:
            flash('Такого пользователя нет!Пройдите регистрацию.')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.')
    return redirect(url_for('product.home'))

