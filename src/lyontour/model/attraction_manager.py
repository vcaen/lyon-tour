from lyontour.model.models import Attraction, Type

__author__ = 'vcaen'


class AttractionManager:

    def __init__(self):
        pass

    @staticmethod
    def get_attraction(self, number):
        list_attractions = Attraction.query.limit(number).all()
        if len(list) < number:
            # Todo request more attractions
            pass


    @staticmethod
    def get_attraction_by_type(self, number, type):
        list_attractions = Attraction.query.filter_by(type=Type.query.filter_by(name=type))




