# Импорт необходимых для работы модулей
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


# Инитиализация blueprint
auth = Blueprint('auth', __name__)


# Вход пользователя
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получение данных из формы
        email = request.form.get('email')
        password = request.form.get('password')
        # Проверка на наличие пользователя в базе данных
        user = User.query.filter_by(email=email).first()
        if user:
            # Проверка пароля
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                # Отображение основной страницы для залогиненных пользователей с файла views.py
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль. Попробуйте ещё раз.', category='error')
        else:
            flash('Пользователь не найден.', category='error')
    # Отображение страницы входа
    return render_template("login.html", user=current_user)



# Выход пользователя
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.main_page'))


# Регитсрация пользователя
@auth.route('/sign-up', methods=['GET', 'POST'])    
def sign_up():
    if request.method == 'POST':
        # Получение данных из формы
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # Проверка на уникальность
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Пользователь с таким именем уже существует.', category='error')
        # Проверка ограничений
        elif len(email) < 4:
            flash('Логин должен иметь более 3 символов.', category='error')
        elif len(first_name) < 2:
            flash('Имя должно иметь более 1 символа.', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают.', category='error')
        elif len(password1) < 7:
            flash('Пароль должен иметь как минимум 7 символов.', category='error')
        else:
            # Добавление нового пользователя в базу данных
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            # Отображение основной страницы для залогиненных пользователей с файла views.py
            return redirect(url_for('views.home'))
    # Отображение страницы регистрации
    return render_template("sign_up.html", user=current_user)
