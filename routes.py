from flask import render_template, flash, redirect, url_for, request
from app import app, db, login_manager, User, Station, Reservation
from forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Eduardo'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

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