from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from passlib.hash import sha256_crypt
from models import db

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET', 'POST'])
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
        return redirect(url_for('profile.profile'))

    return render_template('profile.html', name=current_user.username, email=current_user.email, message=message)
