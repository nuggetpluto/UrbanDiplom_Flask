from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.product_routes import product_bp
from routes.misc_routes import misc_bp

app = Flask(__name__)
app.config.from_object(Config)

# Регистрация blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(product_bp)
app.register_blueprint(misc_bp)

# Инициализация расширений
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
