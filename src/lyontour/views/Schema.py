from marshmallow import Schema, fields, ValidationError
from marshmallow_sqlalchemy import ModelSchema

from lyontour.model.models import *
from lyontour import db

session = db.session


class AttractionSchema(Schema):

    id = fields.Int()
    foursquare_id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    photo = fields.Str()
    address = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()
    postcode = fields.Int()
    ville = fields.Str()
    phone = fields.Str()
    hours = fields.Str()
    rating = fields.Int()
    section_id =  fields.Int()

class EtapeSchema(Schema):
    heure = fields.Int()
    attraction = fields.Nested(AttractionSchema)

class JourSchema(Schema):
    date = fields.DateTime("%d%m%Y")
    etapes = fields.List(fields.Nested(EtapeSchema))
    weather_status = fields.Str()
    weather_temp = fields.Str()

class SectionSchema(ModelSchema):
    class Meta:
        model = Section
        sqla_session = session

class TourSchema(Schema):
    count = fields.Method('get_PI_count')
    DateDebut = fields.Str()
    DateFin = fields.Str()
    PI = fields.List(fields.Nested(AttractionSchema))
    Jours = fields.List(fields.Nested(JourSchema))


    def get_PI_count(self, obj):
        return len(obj.PI)

    # class Meta:
    #     fields = ('DateDebut', 'DateFin', 'PI')

class FilterSchema(Schema):
    filtred_section = fields.List(fields.Str())

attraction_schema = AttractionSchema()
section_schema = SectionSchema()
tour_schema = TourSchema()
filter_schema = FilterSchema()


