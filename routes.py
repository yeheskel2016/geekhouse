from flask import render_template, redirect, url_for
from flask_login import login_required
from app import app, db, Station, Reservation, User
from forms import ReservationForm


@app.route('/')
def home():
    stations = Station.query.all()
    return render_template('home.html', stations=stations)


@app.route('/station/<int:station_id>', methods=['GET', 'POST'])
@login_required
def station(station_id):
    station = Station.query.get(station_id)
    if station is None:
        return redirect(url_for('home'))

    form = ReservationForm()
    if form.validate_on_submit():
        new_reservation = Reservation(start_time=form.start_time.data,
                                      end_time=form.end_time.data,
                                      user_id=current_user.id,
                                      station_id=station.id)
        db.session.add(new_reservation)
        db.session.commit()
        flash('Your reservation has been made!')
        return redirect(url_for('station', station_id=station_id))

    return render_template('station.html', station=station, reservation_form=form)


@app.route('/admin')
@login_required
def admin():
    # Only allow access if the current user is an employee
    if not current_user.is_employee:
        return redirect(url_for('home'))

    reservations = Reservation.query.all()
    return render_template('admin.html', reservations=reservations)
