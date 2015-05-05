from sqlalchemy import Enum
from models import Attraction, Section
from foursquare_manager import executeRequests1
from foursquare_manager import executeRequests
from filter_manager import filter_manager

__author__ = 'vcaen'

import datetime
import json
from lyontour.model.models import Section

def calculDistance(a,list, filtre = None):
    resto = list[0]
    distMin = 100000
    for r in list:
        temp = pow(float(a.latitude) - float(r.latitude),2)+pow(float(a.longitude) - float(r.longitude),2)
        if temp < distMin and r.section.name in filtre:
            distMin=temp
            resto = r
    return resto

class Tour:

    def __init__(self, deb, fin, list=None):
        self.DateDebut = datetime.datetime.strptime(deb, '%d%m%Y')
        self.DateFin = datetime.datetime.strptime(fin, '%d%m%Y')
        self.nbJour = (self.DateFin - self.DateDebut).days + 1
        self.Jours = []
        self.Filtre = str(list).split(',')
        self.attractions = executeRequests1(int(10*self.nbJour/len(self.Filtre)), self.Filtre)
        for i in range(0,self.nbJour,1):
            self.Jours.append(Jour((self.DateDebut + datetime.timedelta(days = i)), self.Filtre))
        self.doItineraire()

    def doItineraire(self):
        night = []
        eat = []
        day = []
        evnight = []
        dayev = []
        eat = executeRequests1(26, [str('food')])

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

        for jour in self.Jours:
            midi = False
            soir = False

            currentH = 8

            while currentH<23:
                if currentH == 8 :
                    print(len(day))
                    for att in day:
                        if att.section.name in jour.filtres :
                            currentA = att
                            day.remove(att)
                            break
                    jour.etapes.append(Etape(currentH, currentA))
                    currentH = currentH +  currentA.section.duration
                elif currentH >=13 and midi == False:
                    if currentH > 13:
                        currentH = 13
                    currentA = calculDistance(currentA, eat, ['food'])
                    jour.etapes.append(Etape(currentH, currentA))
                    midi = True
                    currentH = currentH + currentA.section.duration
                elif currentH >=21 and soir == False:
                    if currentH > 21:
                        currentH = 21
                    currentA = calculDistance(currentA, eat, ['food'])
                    jour.etapes.append(Etape(currentH, currentA))
                    soir = True
                    currentH = currentH +  currentA.section.duration
                elif (currentH >8 and currentH <12) and len(day)!=0 :
                    currentA = calculDistance(currentA, day, jour.filtres)
                    day.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    currentH = currentH +  currentA.section.duration
                elif (currentH >=11 and currentH <14) and midi ==False :
                    if currentH < 12:
                        currentH = 12
                    currentA = calculDistance(currentA, eat, ['food'])
                    jour.etapes.append(Etape(currentH, currentA))
                    midi = True
                    currentH = currentH + datetime.timedelta(hours = 2)
                elif (currentH >=19 and currentH <21) and len(eat)!=0 and soir == False :
                    currentA = calculDistance(currentA, eat, ['food'])
                    jour.etapes.append(Etape(currentH, currentA))
                    soir = True
                    currentH = currentH +  currentA.section.duration
                elif (currentH >=13 and currentH <20) and len(day)!=0 :
                    currentA = calculDistance(currentA, day, jour.filtres)
                    day.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    currentH = currentH +  currentA.section.duration
                elif (currentH >=13 and currentH <20) and len(dayev)!=0:
                    currentA = calculDistance(currentA, dayev, jour.filtres)
                    dayev.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    currentH = currentH +  currentA.section.duration
                elif (currentH >=20 and currentH <23) and len(evnight)!=0:
                    currentA = calculDistance(currentA, evnight, jour.filtres)
                    evnight.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    currentH = currentH +  currentA.section.duration
                elif currentH < 8 :
                    break
                else:
                    currentH = currentH + 1

    def getJours(self):
        return self.Jours


class Itineraire:
    def __init__(self):
        self.Jours = []

class Jour:
    def __init__(self, date, filtres):
        self.date = date
        self.etapes=[]
        self.filtres = filtres

        # f_manager = filter_manager()
        # weather = f_manager.getWeatherByDay(date)
        # if weather["pluie"] is True:
        #     self.weather_status = "rainy"
        # else:
        #     self.weather_status = weather["nuage"]

    def getWeatherStatus(self):
        return self.weather_status

    def addAttraction(self, attraction):
        self.attractions.append(attraction)

    def getDate(self):
        return self.date

    def getAttractions(self):
        return self.attractions

class Etape:
    def __init__(self, Heure, Attraction):
        self.heure = Heure
        self.attraction = Attraction

    def getDate(self):
        return self.date
