# Импорт необходимых для работы модулей
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Note, User
from . import db
import json
import requests
import geocoder
from geopy.geocoders import Nominatim


# Инитиализация blueprint
views = Blueprint('views', __name__)


# Подключение API погоды
def get_weather(weather=[]):
    # Получение координат
    coordinates = geocoder.ip('me').latlng
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(coordinates[0]) + "," + str(coordinates[1]))
    # Определение города по координатам
    address = location.raw['address']
    city = address.get('city', '')
    # Получение json-объекта с данными о городе и погодных условиях
    api = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=66e2fd0cd570079bfeabc5b1f959e0a9'
    data = requests.get(api).json()
    # Добавление названия города, погода и температуры города в лист weather
    weather.append(city)
    weather.append(data['weather'][0]['main'])
    weather.append(int(data['main']['temp'] - 273.1))
    return weather


# Создание основной страницы
@views.route('/')
def main_page():
    # Отображение основной страницы
    return render_template("main_page.html", user=current_user)


# Создание основной страницы для залогиненных пользователей
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Получение данных с формы
        note = request.form.get('note')
        # Проверка ограничений
        if len(note) < 1:
            flash('Пожалуйста, введите что-нибудь.', category='error')
        else:
            # Добавление заметки в базу данных
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    # Отображение основной страницы для залогиненных пользователей
    return render_template("home.html", user=current_user, weather=get_weather())


# Создание функции удаления заметок
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Получение json-объекта
    note = json.loads(request.data)
    # Получение id заметки по ключу noteId
    noteId = note['noteId']
    # Проверка на наличие заметки в базе
    note = Note.query.get(noteId)
    if note:
        # Проверка на наличие заметки у пользователя по id пользователя
        if note.user_id == current_user.id:
            # Удаление заметки с базы
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


# Создание страницы личного кабинета
@views.route('/cabinet')
@login_required
def cabinet():
    # Отображение страницы личного кабинета
    return render_template("cabinet.html", user=current_user)


# Создание страницы настроек
@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Получение id пользователя и данных с формы
        user_id = int(str(current_user)[-2])
        new_password = request.form.get('new_password')
        # Редактирование данных в базе
        db.session.query(User).filter(User.id == user_id).update({User.password: generate_password_hash(new_password)})
        db.session.commit()
        # Отображение основной страницы для залогиненных пользователей
        return render_template("home.html", user=current_user, weather=get_weather())
    # Отображение страницы настроек
    return render_template("settings.html", user=current_user)


# Создание функции редактирования заметок
@views.route('/edit', methods=['POST'])
def edit():
    # Получение json-объекта
    note = json.loads(request.data)
    # Получение id заметки по ключу noteId
    noteId = note['noteId']
    # Получение новой заметки по ключу new_note
    new_note = note['new_note']
    # Редактирование данных в базе
    db.session.query(Note).filter(Note.id == noteId).update({Note.data: new_note})
    db.session.commit()
    return jsonify({})
