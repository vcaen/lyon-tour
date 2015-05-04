from sqlalchemy import Enum
from models import Attraction, Section
from foursquare_manager import executeRequests


__author__ = 'vcaen'

import datetime
import json

class Tour:

    def __init__(self, deb, fin, list=None):
        self.DateDebut = datetime.datetime.strptime(deb, '%d%m%Y')
        self.DateFin = datetime.datetime.strptime(fin, '%d%m%Y')
        self.nbJour = (self.DateFin - self.DateDebut).days + 1
        self.Jours = []
        self.Filtre = list

        for i in range(0,self.nbJour,1):
            self.Jours.append(Jour(self.DateDebut + datetime.timedelta(days = i)))

        self.PI = executeRequests(self.nbJour, list)


class Itineraire:
    def __init__(self):
        self.Jours = []

class Jour:
    def __init__(self, date):
        self.date = date
        self.attractions = []

    def addAttraction(self, attraction):
        self.attractions.append(attraction)

class JSONObject:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4, separators=(',', ': '))








