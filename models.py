from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
from . import db

class Station(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price_per_hour = db.Column(db.Integer)
    is_vip = db.Column(db.Boolean, default=False)
    is_open = db.Column(db.Boolean, default=True)
    actual_start = db.Column(db.DateTime, default=None)
    actual_end = db.Column(db.DateTime, default=None)
    ETA = db.Column(db.DateTime, default=None)
    reservations = db.relationship('Reservation', back_populates='station')

    def check_availability(self, start_time, end_time):
        for reservation in self.reservations:
            if (start_time < reservation.end_time and
                    end_time > reservation.start_time):
                return False
        return True

    def next_available_time(self):
        if not self.reservations:
            return datetime.now()

        last_reservation = self.reservations[-1]
        return last_reservation.end_time

    def is_available_for_the_day(self, date):
        available_slots = self.get_available_slots(date)
        return len(available_slots) > 0

    def close_station(self):
        self.is_open = False
        db.session.commit()

    def open_station(self):
        self.is_open = True
        db.session.commit()

    def get_available_slots(self, date):
        # Return an empty list if the station is closed
        if not self.is_open:
            return []

        # Define opening and closing hours. This could also be attributes of the Station class
        opening_hour = datetime.time(18, 0)
        closing_hour = datetime.time(4, 0)

        # Convert these times to datetime objects on the specified date
        timezone = pytz.timezone("Israel")  # Replace with your actual timezone
        now = datetime.datetime.now(timezone)
        opening_time = timezone.localize(datetime.datetime.combine(date, opening_hour))
        closing_time = timezone.localize(datetime.datetime.combine(date, closing_hour))

        if closing_time < opening_time:
            closing_time += datetime.timedelta(days=1)

        # Check that the date is today or tomorrow
        if date.date() not in {now.date(), (now + datetime.timedelta(days=1)).date()}:
            raise ValueError("You can only make reservations for today or tomorrow.")

        # Start with a list of all time slots
        slot_duration = datetime.timedelta(hours=1)
        available_slots = [
            (opening_time + i * slot_duration, opening_time + (i + 1) * slot_duration)
            for i in range((closing_time - opening_time) // slot_duration)
        ]

        # Remove slots that overlap with existing reservations
        for reservation in self.reservations:
            if reservation.start_time.date() == date:
                available_slots = [
                    slot for slot in available_slots
                    if slot[0] >= reservation.end_time or slot[1] <= reservation.start_time
                ]

        # Check the ETA of the station and remove all slots before the ETA.
        if self.actual_start is not None and self.ETA is not None:
            available_slots = [slot for slot in available_slots if slot[0] >= self.ETA]

        return available_slots
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    is_employee = db.Column(db.Boolean, default=False)

    reservations = db.relationship('Reservation', back_populates='user')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))
    station = db.relationship('Station', back_populates='reservations')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='reservations')

    @staticmethod
    def make_reservation(user, station, start_time, end_time):
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        if not station.check_availability(start_time, end_time):
            raise ValueError("Station is not available during the requested time slot")
        reservation = Reservation(start_time=start_time, end_time=end_time, station=station, user=user)
        db.session.add(reservation)
        db.session.commit()
        return reservation

    def calculate_cost(self):
        if self.actual_start and self.actual_end:
            duration = (self.actual_end - self.actual_start).seconds / 3600
        else:
            duration = (self.end_time - self.start_time).seconds / 3600
        return duration * self.station.price_per_hour
