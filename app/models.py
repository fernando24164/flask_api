from . import db


association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('station_id', db.Integer, db.ForeignKey('stations.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), unique=True, index=True)

    def __repr__(self):
        return '<User %s>' % self.name

    @staticmethod
    def insert_users(users=5):
        from sqlalchemy.exc import InternalError
        import forgery_py

        for user in range(users):
            data = User(name=forgery_py.name.first_name())

            db.session.add(data)
            try:
                db.session.commit()
            except InternalError:
                db.session.rollback()


class Weather_Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), unique=True)
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    users = db.relationship("User",
                            secondary=association_table)

    def __repr__(self):
        return '<Weather_Station %s>' % self.description

    @staticmethod
    def insert_stations(stations=5):
        from sqlalchemy.exc import InternalError
        import forgery_py

        for station in range(stations):
            data = Weather_Station(description=forgery_py.address.street_name(),
                                   latitude=str(forgery_py.geo.latitude_degrees()) +
                                   str(forgery_py.geo.latitude_direction()),
                                   longitude=str(forgery_py.geo.longitude_degrees()) +
                                   str(forgery_py.geo.longitude_direction()))
            users = User.query.all()
            for user in users:
                data.users.append(user)

            db.session.add(data)
            try:
                db.session.commit()
            except InternalError:
                db.session.rollback()
