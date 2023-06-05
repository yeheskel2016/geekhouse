from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import app, db
from .models import Station, Reservation
from .forms import RegistrationForm, LoginForm, ReservationForm

@app.route('/')
def home():
    stations = Station.query.all()
    return render_template('home.html', stations=stations)

@app.route('/station/<int:station_id>')
@login_required
def station(station_id):
    station = Station.query.get(station_id)
    if station is None:
        return redirect(url_for('home'))
    return render_template('station.html', station=station)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_employee:
        return redirect(url_for('home'))
    reservations = Reservation.query.all()
    return render_template('admin.html', reservations=reservations)