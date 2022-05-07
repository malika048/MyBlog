# Импорт необходимых для работы модулей
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_login import LoginManager


# Инитиализация SQLAlchemy
db = SQLAlchemy()
# Загрузка переменных окружения
load_dotenv()


# Создание веб-приложения Flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = f'{os.getenv("SECRET_KEY")}' # Получение секретного ключа из .env
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getenv("DB_NAME")}' # Получение названия базы данных из .env
    db.init_app(app)
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/') # Подключение blueprint
    app.register_blueprint(auth, url_prefix='/') # Подключение blueprint
    from .models import User, Note
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


# Создание базы данных
def create_database(app):
    if not os.path.exists(f'website/{os.getenv("DB_NAME")}'):
        db.create_all(app=app)
        print('Created Database!')
