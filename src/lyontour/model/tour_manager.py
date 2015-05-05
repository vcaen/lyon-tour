from sqlalchemy import Enum
from models import Attraction, Section
from foursquare_manager import executeRequests
from filter_manager import filter_manager

__author__ = 'vcaen'

import datetime
import json

class Tour:

    def __init__(self, deb, fin, list=None):
        self.DateDebut = datetime.datetime.strptime(deb, '%Y-%m-%d')
        self.DateFin = datetime.datetime.strptime(fin, '%Y-%m-%d')
        self.nbJour = (self.DateFin - self.DateDebut).days + 1
        self.Jours = []
        self.Filtre = list

        for i in range(0,self.nbJour,1):
            self.Jours.append(Jour(self.DateDebut + datetime.timedelta(days = i)))

        self.PI = executeRequests(self.nbJour, list)

    def getJours(self):
        return self.Jours


class Itineraire:
    def __init__(self):
        self.Jours = []

class Jour:
    def __init__(self, date):
        self.date = date
        self.attractions = []
        f_manager = filter_manager()
        weather = f_manager.getWeatherByDay(date)
        if weather["pluie"] is True:
            self.weather_status = "rainy"
        else:
            self.weather_status = weather["nuage"]

    def getWeatherStatus(self):
        return self.weather_status

    def addAttraction(self, attraction):
        self.attractions.append(attraction)

    def getDate(self):
        return self.date

    def getAttractions(self):
        return self.attractions

class JSONObject:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4, separators=(',', ': '))








