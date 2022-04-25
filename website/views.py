from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import requests
import geocoder
from geopy.geocoders import Nominatim


views = Blueprint('views', __name__)


def get_weather(weather=[]):
    coordinates = geocoder.ip('me').latlng
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(coordinates[0]) + "," + str(coordinates[1]))
    address = location.raw['address']
    city = address.get('city', '')
    api = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=66e2fd0cd570079bfeabc5b1f959e0a9'
    data = requests.get(api).json()
    weather.append(city)
    weather.append(data['weather'][0]['main'])
    weather.append(int(data['main']['temp'] - 273.1))
    return weather


@views.route('/')
def main_page():
    return render_template("main_page.html", user=current_user)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Пожалуйста, введите что-нибудь.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user, weather=get_weather())


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
