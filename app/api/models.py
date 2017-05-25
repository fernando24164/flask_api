from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Signer
from flask import current_app
from datetime import datetime

association = db.Table('association', db.Model.metadata,
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('users.id')),
                       db.Column('station_id', db.Integer,
                                 db.ForeignKey('stations.id'))
                       )

forecast = db.Table('weather_forecast',
                    db.Column('station_id', db.Integer,
                              db.ForeignKey('stations.id')),
                    db.Column('forecast_id', db.Integer,
                              db.ForeignKey('forecasts.id'))
                    )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), unique=True, index=True)
    pwdhash = db.Column(db.String())

    def __init__(self, name, pwd):
        self.name = name
        self.pwdhash = generate_password_hash(pwd)

    def verify_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def generate_auth_token(self, expiration=600):
        sign_hash = Signer(current_app.config['SECRET_KEY'],
                           expires_in=expiration)
        return sign_hash.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        sign_hash = Signer(current_app.config['SECRET_KEY'])
        try:
            data = sign_hash.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %s>' % self.name

    def to_json(self):
        json_user = {
            'name': self.name
        }
        return json_user

    @staticmethod
    def insert_users(users=5):
        from sqlalchemy.exc import InternalError
        import forgery_py

        for user in range(users):
            data = User(name=forgery_py.name.full_name(), pwd='admin')

            db.session.add(data)
            try:
                db.session.commit()
            except InternalError:
                db.session.rollback()


class Forecast(db.Model):
    __tablename__ = 'forecasts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now(), index=True)
    temperature = db.Column(db.String)
    wind_speed = db.Column(db.String)
    humidity = db.Column(db.String)
    comments = db.Column(db.Text)

    def __repr__(self):
        return '<Forecast date: %s>' % self.date

    def to_json(self):
        json_forecast = {
            'date': self.date,
            'temperature': self.temperature,
            'wind_speed': self.wind_speed,
            'humidity': self.humidity,
            'comments': self.comments
        }
        return json_forecast

    @staticmethod
    def insert_forecasts(forecasts=25):
        from sqlalchemy.exc import InternalError
        import forgery_py

        for forecast in range(5):
            data = Forecast(date=forgery_py.date.datetime(past=True,
                                                          min_delta=0,
                                                          max_delta=5),
                            temperature=str(forgery_py.basic.number(
                                at_least=15, at_most=31))+'ºC',
                            wind_speed=str(forgery_py.basic.number(
                                at_least=5, at_most=25))+'Km/h',
                            humidity=str(forgery_py.basic.number(
                                at_least=35, at_most=70))+'%',
                            comments=forgery_py.lorem_ipsum.paragraph(
                                sentences_quantity=2))

            db.session.add(data)
            try:
                db.session.commit()
            except InternalError:
                db.session.rollback()


class Weather_Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, unique=True)
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    users = db.relationship("User",
                            secondary=association)
    forecasts = db.relationship("Forecast",
                                secondary=forecast)

    def __repr__(self):
        return '<Weather_Station %s>' % self.description

    def get_forecast_array(self):
        forecast_array = []
        for forecast in self.forecasts:
            forecast_array.append(forecast.to_json())
        return forecast_array

    def to_json(self):
        json_station = {
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'forecast': self.get_forecast_array()
        }
        return json_station

    @staticmethod
    def insert_stations(stations=5):
        from sqlalchemy.exc import InternalError
        import forgery_py

        for station in range(stations):
            data = Weather_Station(description=forgery_py.address.street_address(),
                                   latitude=str(forgery_py.geo.latitude_degrees()) +
                                   str(forgery_py.geo.latitude_direction()),
                                   longitude=str(forgery_py.geo.longitude_degrees()) +
                                   str(forgery_py.geo.longitude_direction()))
            users = User.query.all()
            forecasts = Forecast.query.all()
            for forecast in forecasts:
                if forecast.id % (station+1) == 0:
                    data.forecasts.append(forecast)
            for user in users:
                data.users.append(user)

            db.session.add(data)
            try:
                db.session.commit()
            except InternalError:
                db.session.rollback()
