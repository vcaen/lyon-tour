
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
        if (temp < distMin and r.section.name in filtre):
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
        if len(self.Filtre)>0:
            nombreRequest = int(10*self.nbJour/len(self.Filtre))+1
        else:
            nombreRequest = 1
        self.attractions = executeRequests(nombreRequest, self.Filtre)
        for i in range(0,self.nbJour,1):
            self.Jours.append(Jour((self.DateDebut + datetime.timedelta(days = i)), self.Filtre))
        self.doItineraire()

    def doItineraire(self):
        night = []
        day = []
        evnight = []
        eat = executeRequests(26, [str('food')])

        for a in self.attractions:
            s = a.section.dayTime
            if s == "night":
                night.append(a)
            elif s == "day":
                day.append(a)
            elif s == "evening/night":
                evnight.append(a)

        for jour in self.Jours:
            midi = False
            soir = False

            currentH = 8

            while currentH<23:
                if currentH == 8 :
                    if len(day) != 0:
                        currentA = day[0]
                        for att in day:
                            if att.section.name in jour.filtres :
                                currentA = att
                                break
                    day.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    currentH = currentH +  currentA.section.duration
                elif currentH >=13 and midi == False:
                    if currentH > 13:
                        currentH = 13
                    currentA = calculDistance(currentA, eat, ['food'])
                    eat.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    midi = True
                    currentH = currentH + currentA.section.duration
                elif currentH >=21 and soir == False:
                    if currentH > 21:
                        currentH = 21
                    currentA = calculDistance(currentA, eat, ['food'])
                    eat.remove(currentA)
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
                    eat.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    midi = True
                    currentH = currentH + 2
                elif (currentH >=19 and currentH <21) and len(eat)!=0 and soir == False :
                    currentA = calculDistance(currentA, eat, ['food'])
                    eat.remove(currentA)
                    jour.etapes.append(Etape(currentH, currentA))
                    soir = True
                    currentH = currentH +  currentA.section.duration
                elif (currentH >=13 and currentH <20) and len(day)!=0 :
                    currentA = calculDistance(currentA, day, jour.filtres)
                    day.remove(currentA)
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
        liste_jour = []
        for jour in self.Jours:
            liste_jour.append(jour.getDate())
        return liste_jour


class Itineraire:
    def __init__(self):
        self.Jours = []

class Jour:
    def __init__(self, date, filtres):
        self.date = date
        self.etapes=[]
        f_manager = filter_manager([date])
        weather = f_manager.getWeatherByDay(str(self.date))
        self.weather_temp = weather["temp"]
        if weather["pluie"] is True:
            self.weather_status = "rainy"
        else:
            self.weather_status = weather["nuage"]

        self.filtres = f_manager.filtre_meteo(str(self.date), filtres)


class Etape:
    def __init__(self, Heure, Attraction):
        self.heure = Heure
        self.attraction = Attraction
