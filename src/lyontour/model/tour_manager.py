from sqlalchemy import Enum
from models import Attraction, Section
from foursquare_manager import executeRequests


__author__ = 'vcaen'

import datetime
import json
from lyontour.model.models import Section

class Tour:

    def __init__(self, deb, fin, list=None):
        self.DateDebut = datetime.datetime.strptime(deb, '%d%m%Y')
        self.DateFin = datetime.datetime.strptime(fin, '%d%m%Y')
        self.nbJour = (self.DateFin - self.DateDebut).days + 1
        self.Jours = []
        self.Filtre = list

        for i in range(0,self.nbJour,1):
            self.Jours.append(Jour(self.DateDebut + datetime.timedelta(days = i)))
            self.Jours[i].attractions = executeRequests(14, list)
            self.Jours[i].doIt()


class Itineraire:
    def __init__(self):
        self.Jours = []

class Jour:
    def __init__(self, date):
        self.date = date
        self.attractions = []
        self.etapes=[]

    def addAttraction(self, attraction):
        self.attractions.append(attraction)

    def doIt(self):
        midi = False
        soir = False

        night = []
        eat = []
        day = []
        evnight = []
        dayev = []
        for a in self.attractions:
            s = a.section.dayTime
            if s == "night":
                night.append(a)
            elif s == "day":
                day.append(a)
            elif s == "eat":
                eat.append(a)
            elif s == "evening/night":
                evnight.append(a)

        currentH = datetime.datetime.strptime('8:00','%H:%M')
        nbHday = len(day)+len(dayev)+len(eat)+ len(evnight)+len(night)

        for i in range(0,nbHday,1):
            if (currentH.hour >=8 and currentH.hour <12) and len(day)!=0 :
                self.etapes.append(Etape(currentH, day.pop()))
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)
            elif (currentH.hour >=12 and currentH.hour <14) and len(eat)!=0 and midi ==False :
                self.etapes.append(Etape(currentH, eat.pop()))
                midi = True
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)
            elif (currentH.hour >=19 and currentH.hour <21) and len(eat)!=0 and soir == False :
                self.etapes.append(Etape(currentH, eat.pop()))
                soir = True
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)
            elif (currentH.hour >=13 and currentH.hour <20) and len(day)!=0 :
                self.etapes.append(Etape(currentH, day.pop()))
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)
            elif (currentH.hour >=13 and currentH.hour <20) and len(dayev)!=0:
                self.etapes.append(Etape(currentH, dayev.pop()))
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)
            elif (currentH.hour >=20 and currentH.hour <23) and len(evnight)!=0:
                self.etapes.append(Etape(currentH, evnight.pop()))
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)
            else:
                currentH = currentH + datetime.timedelta(minutes = 14*60/nbHday)


class Etape:
    def __init__(self, Heure, Attraction):
        self.heure = Heure
        self.attaction = Attraction


class JSONObject:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4, separators=(',', ': '))








