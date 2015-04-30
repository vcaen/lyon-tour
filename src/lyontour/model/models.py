
from lyontour import db


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), primary_key=True)
    weather = db.Column(db.String(45), nullable=True)
    dayTime = db.Column(db.String(45), nullable=True)  # day, evening, night
    duration = db.Column(db.DateTime, nullable=True)
    attraction_id =  db.Column(db.Integer, db.ForeignKey('attraction.id'))


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foursquare_id = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(2055), nullable=True)
    photo = db.Column(db.String(511), nullable=True)
    section = db.relationship('Section', backref='attraction', lazy='joined' )
    address = db.Column(db.String(1023), nullable=True)
    latitude = db.Column(db.String(255), nullable=True)
    longitude = db.Column(db.String(255), nullable=True)
    postcode = db.Column(db.Integer, nullable=True)
    ville = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(25), nullable=True)
    hours = db.Column(db.String(30), nullable=True)

    def __init__(self, nom , untype, desc, adress):
        self.name = nom
        self.description = desc
        self.section_id = untype
        self.address = adress




class WeatherDay(db.Model):
    date = db.Column(db.Date, primary_key=True)
    rain = db.Column(db.Float, nullable=True)
    snow = db.Column(db.Boolean, nullable=True)



