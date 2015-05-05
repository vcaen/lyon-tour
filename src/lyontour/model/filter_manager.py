# coding=utf-8
from lyontour import db
from lyontour.model.foursquare_manager import executeRequests

__author__ = 'mrcherif'

from lyontour.model.models import WeatherDay, Section

import datetime
import urllib2
import json

#L'api est spécifique pour Lyon / Elle donne des infos à prtir du jour de la requête jusqu'à 7 jours
meteo_api_url = "http://www.infoclimat.fr/public-api/gfs/json?_ll=45.74846,4.84671&_auth=ARtXQA9xVnRVeAYxAnRReFU9U2ZbLQcgCnYGZVoyVSgHY1c3Vj0AZlA5BnsHKFJiV3oDa1tgUmwBZQdhCHoDfwFgVzoPZVYyVTMGYAI2UXpVeVMuW2UHIAp2BmBaNFUyB3pXMVY0AGZQIQZlBz9Sbld6A2JbYlJoAX0HfwhkA2QBYVczD29WNFU6BmMCNFFiVXlTLFthBzoKbQZhWmZVPgdhV2VWNABmUG4GZgc%2BUmJXegNlW2RSYwFqB2UIZwNpAWdXLA9zVk1VSQZ5AnJRJ1UzU3VbeQdqCjcGNQ%3D%3D&_c=cd00e152c42b3f31881e89f4f263728c"


class filter_manager:

    def __init__(self):
        pass

    def getWeatherByDay(self, jour):
        res = [] #Tableau Rain(bool) / Snow(Oui, non)
        date_jour = datetime.datetime.strptime(jour, '%Y-%m-%d').date()
        # to_day = datetime.datetime.now().date()
        # if date_jour < to_day:
        #     return "erreur, date passée \n"
        #else:
            #rain = WeatherDay.query.filter_by(date=jour).first().rain
        day = WeatherDay.query.get(jour)
        if not(day is None):
            pluie = day.rain
            snow = day.snow
            res.append(pluie<=2.5)
            res.append(snow)
            return res
        else:
            f = urllib2.urlopen(meteo_api_url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            f.close()
            rain = parsed_json[jour + ' 12:00:00']["pluie"]
            snow = parsed_json[jour + ' 12:00:00']["snow"]
            pluie = day.rain
            snow = day.snow
            res.append(pluie<=2.5)
            res.append(snow)
            day = WeatherDay(date_jour, rain, snow)
            db.session.add(day)
            db.session.commit()
            return res

    def getRainByDay(self, jour):
        date_jour = datetime.datetime.strptime(jour, '%Y-%m-%d').date()
        # to_day = datetime.datetime.now().date()
        # if date_jour < to_day:
        #     return "erreur, date passée \n"
        # else:
            #snow = WeatherDay.query.filter_by(date=jour).first().snow
        day = WeatherDay.query.get(jour)
        if not(day is None):
            pluie = day.rain
            return pluie<=2.5
        else:
            f = urllib2.urlopen(meteo_api_url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            f.close()
            pluie = parsed_json[jour + ' 12:00:00']["rain"]
            return pluie

    def getSnowByDay(self, jour):
        date_jour = datetime.datetime.strptime(jour, '%Y-%m-%d').date()
        # to_day = datetime.datetime.now().date()
        # if date_jour < to_day:
        #     return "erreur, date passée \n"
        # else:
            #snow = WeatherDay.query.filter_by(date=jour).first().snow
        day = WeatherDay.query.get(jour)
        if not(day is None):
            neige = day.snow
            return neige
        else:
            f = urllib2.urlopen(meteo_api_url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            f.close()
            snow = parsed_json[jour + ' 12:00:00']["risque_neige"]
            return snow

    def filtre_meteo(self, jour, preference):
        for i in preference:
            section = Section.query.filter_by(name=i).first()
            if not(section is None):
                    if (section.weather == "bad" and (self.getWeatherByDay(jour)[0] is False or self.getWeatherByDay(jour)[1] == "non")) or (section.weather == "good" and (self.getWeatherByDay(jour)[0] is True or self.getWeatherByDay(jour)[1] == "oui")):
                        preference.remove(i)
        return preference

    def getAttractionFiltred(self, liste_jours, preferences_user):
        attractions = []
        preferences_filtrees = []
        for i, elt in liste_jours:
            preferences_filtrees = self.filtre_meteo(elt.getDate(), preferences_user)
            attractions = executeRequests(10, preferences_filtrees)
            for a in attractions:
                if (a in liste_jours[i-1].getAttractions):
                    attractions.remove[a]
            i.addAttraction(attractions)
        return attractions
