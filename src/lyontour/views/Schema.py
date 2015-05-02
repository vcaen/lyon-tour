from marshmallow import Schema, fields, ValidationError
from marshmallow_sqlalchemy import ModelSchema

from lyontour.model.models import *
from lyontour import db

session = db.session


class AttractionSchema(ModelSchema):
    class Meta:
        model = Attraction
        sqla_session = session

class SectionSchema(ModelSchema):
    class Meta:
        model = Section
        sqla_session = session

class TourSchema(ModelSchema):
    DateDebut = fields.Str()
    DateFin = fields.Str()
    PI = fields.List(fields.Nested(AttractionSchema))

    class Meta:
        fields = ('DateDebut', 'DateFin', 'PI')

attraction_schema = AttractionSchema()
section_schema = SectionSchema()
tour_schema = TourSchema()


