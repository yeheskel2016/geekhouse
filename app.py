from . import app, db
from models import Station, User, Reservation

def close_all_stations():
    for station in Station.query.all():
        station.close_station()
    db.session.commit()

def open_all_stations():
    for station in Station.query.all():
        station.open_station()
    db.session.commit()

#Data relevant for geekhouse
def create_initial_data():
    # Check if the database is already populated
    if db.session.query(User).count() > 0:
        return
    # Create some users
    edo = User(name="Edo", phone_number='+972526362822', email="Edo@yeheskel.co.il", is_employee=True)
    edo.set_password("416057")
    shiel = User(name="Shiel", email="Shielhad@gmail.com")
    shiel.set_password("416057")

    db.session.add_all([edo, shiel])

    # Create some stations
    station = Station(name="Snooker Table", price_per_hour=45)
    station1 = Station(name="Station 1", price_per_hour=60)
    station2 = Station(name="Station 2", price_per_hour=60)
    station3 = Station(name="Station 3", price_per_hour=60)
    station4 = Station(name="Station 4", price_per_hour=60)
    station5 = Station(name="Station 5", price_per_hour=60)
    station6 = Station(name="Station 6", price_per_hour=60)
    station7 = Station(name="Station 7", price_per_hour=60)
    station8 = Station(name="Station VIP", price_per_hour=80, is_vip=True)
    station9 = Station(name="Station PRIVATE", price_per_hour=80, is_vip=True)

    db.session.add_all([station, station1, station2, station3, station4, station5, station6, station7, station8, station9])
    db.session.commit()

def occupy_station(station_id, start_time, ETA):
    session = db.Session()
    station = session.query(Station).get(station_id)
    station.actual_start = start_time
    station.ETA = ETA
    session.commit()

def free_station(station_id, end_time):
    session = db.Session()
    station = session.query(Station).get(station_id)
    station.actual_end = end_time
    station.ETA = None
    session.commit()

def update_ETA(station_id, new_ETA):
    session = db.Session()
    station = session.query(Station).get(station_id)
    station.ETA = new_ETA
    session.commit()


if __name__ == "__main__":
    create_initial_data()
    app.run(debug=True)

