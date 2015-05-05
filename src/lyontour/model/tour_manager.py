from sqlalchemy import Enum
from models import Attraction, Section
from foursquare_manager import executeRequests1


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
            self.Jours[i].attractions = executeRequests1(2)
            self.Jours[i].doIt()


class Itineraire:
    def __init__(self):
        self.Jours = []

class Jour:
    def __init__(self, date):
        self.date = date
        self.attractions = []
        self.etapes=[]
        #self.Weather

    def addAttraction(self, attraction):
        self.attractions.append(attraction)

    def getTime(self, attr):
        result = 0
        for a in attr:
            result = result + a.section.duration
        return result

    def calculDistance(self,a,list):
        resto = list[0]
        distMin = 0
        for resto in list:
            if (float(a.latitude) - float(resto.latitude))<distMin:
                resto = a
        return resto

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
             elif s == "evening/night":
                 evnight.append(a)
             elif s == "day/evening":
                 dayev.append(a)


        currentH = datetime.datetime.strptime('8:00','%H:%M')
        nbHday = self.getTime(night) + self.getTime(day) + self.getTime(dayev) + self.getTime(eat) + self.getTime(evnight)
        nbAttrac = len(self.attractions)


        for i in range(0,nbAttrac,1):
             print(currentH.hour)
             if (currentH.hour >=8 and currentH.hour <12) and len(day)!=0 :
                 currentA = day.pop()
                 self.etapes.append(Etape(currentH, currentA))
                 currentH = currentH + datetime.timedelta(hours = currentA.section.duration)
                 if (currentH.hour >=11 and currentH.hour <14) and midi ==False :
                     listSection = []
                     listSection.append('food')
                     eat = executeRequests1(10, listSection)
                     print(len(eat))
                     print(self.calculDistance(currentA, eat).name)
                     self.etapes.append(Etape(currentH, eat.pop()))
                     midi = True
                     currentH = currentH + datetime.timedelta(hours = currentA.section.duration)
             elif (currentH.hour >=19 and currentH.hour <21) and len(eat)!=0 and soir == False :
                 self.etapes.append(Etape(currentH, eat.pop()))
                 soir = True
                 currentH = currentH + datetime.timedelta(hours = currentA.section.duration)
             elif (currentH.hour >=13 and currentH.hour <20) and len(day)!=0 :
                 self.etapes.append(Etape(currentH, day.pop()))
                 currentH = currentH + datetime.timedelta(hours = currentA.section.duration)
             elif (currentH.hour >=13 and currentH.hour <20) and len(dayev)!=0:
                 self.etapes.append(Etape(currentH, dayev.pop()))
                 currentH = currentH + datetime.timedelta(hours = currentA.section.duration)
             elif (currentH.hour >=20 and currentH.hour <23) and len(evnight)!=0:
                 self.etapes.append(Etape(currentH, evnight.pop()))
                 currentH = currentH + datetime.timedelta(hours = currentA.section.duration)
             elif currentH.hour < 8 :
                 break;
             else:
                 currentH = currentH + datetime.timedelta(hours = 1)




class Etape:
    def __init__(self, Heure, Attraction):
        self.heure = Heure
        self.attraction = Attraction

    def getDate(self):
        return self.date
