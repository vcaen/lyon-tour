# coding=utf-8
from lyontour import db
from lyontour.model.foursquare_manager import executeRequests

__author__ = 'mrcherif'

from lyontour.model.models import WeatherDay, Section
import lyontour.model.tour_manager

import datetime
import urllib2
import json

#L'api est spécifique pour Lyon / Elle donne des infos à prtir du jour de la requête jusqu'à 7 jours
meteo_api_url = "http://www.infoclimat.fr/public-api/gfs/json?_ll=45.74846,4.84671&_auth=ARtXQA9xVnRVeAYxAnRReFU9U2ZbLQcgCnYGZVoyVSgHY1c3Vj0AZlA5BnsHKFJiV3oDa1tgUmwBZQdhCHoDfwFgVzoPZVYyVTMGYAI2UXpVeVMuW2UHIAp2BmBaNFUyB3pXMVY0AGZQIQZlBz9Sbld6A2JbYlJoAX0HfwhkA2QBYVczD29WNFU6BmMCNFFiVXlTLFthBzoKbQZhWmZVPgdhV2VWNABmUG4GZgc%2BUmJXegNlW2RSYwFqB2UIZwNpAWdXLA9zVk1VSQZ5AnJRJ1UzU3VbeQdqCjcGNQ%3D%3D&_c=cd00e152c42b3f31881e89f4f263728c"


class filter_manager:
    #attribut: liste des sections filtrées par la météo(string)
    filtred_section = []

    #constructeur: à partir d'une liste de jour et des préférences utilisateurs pour les sections
    def __init__(self, jour, preferences_user=None):
        sections = []
        if not(preferences_user is None):
                sections = self.filtre_meteo(jour, preferences_user)
        self.filtred_section = sections


    #return un dictionnaire avec les clés suivantes: date(string formatée: Y-M-D), temp(en Celcius), nuage(bool), pluie(bool) et nuage(string: cloudy, partly cloudy, sunny)
    #param objet de type date
    def getWeatherByDay(self, jour):
        #on formate la date en string Y-M-D compatible avec le contenu du json de l'API
        date_formatee = datetime.datetime.strptime(jour, '%Y-%m-%d %H:%M:%S').date()
        #on recherche d'abord dans la table weather_day si la requête pour le jour a déjà été faite et stockée
        day = WeatherDay.query.get(date_formatee)
        weather_day = {}
        weather_day["date"] = date_formatee
        if not(day is None):
            #on remplit le dictionnaire renvoyé
            weather_day["temp"] = day.temp
            weather_day["nuage"] = day.cloud
            weather_day["pluie"] = day.rain
            weather_day["neige"] = day.snow
            return weather_day
        else:
            #sinon on requête API
            f = urllib2.urlopen(meteo_api_url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            f.close()
            #on remplit le dictionnaire renvoyé
            weather_day["temp"] = (parsed_json[str(date_formatee) + ' 12:00:00']["temperature"]["sol"]) - 273.15
            weather_day["pluie"] = parsed_json[str(date_formatee) + ' 12:00:00']["pluie"] >=2
            if parsed_json[str(date_formatee) + ' 12:00:00']["nebulosite"]["totale"] < 10:
                weather_day["nuage"] = "sunny"
            elif parsed_json[str(date_formatee) + ' 12:00:00']["nebulosite"]["totale"] >= 10 and parsed_json[str(date_formatee) + ' 12:00:00']["nebulosite"]["totale"] < 50:
                weather_day["nuage"] = "partly cloudy"
            else:
                weather_day["nuage"] = "partly cloudy"
            weather_day["neige"] = parsed_json[str(date_formatee) + ' 12:00:00']["risque_neige"] == "oui"
            #on construit l'objet et on le rentre dans la DB
            print "Filling WeatherDay table .."
            day = WeatherDay(str(date_formatee), weather_day["temp"], weather_day["nuage"], weather_day["pluie"], weather_day["neige"])
            db.session.add(day)
            db.session.commit()
            print "WeatherDay table Filled "
            return weather_day

    #@return une liste des sections filtées par la météo pour chaque jour à partir des préférences utilisateurs
    #params liste d'objets de type Date, liste des préférences de sections utilisateur(string)
    def filtre_meteo(self, jour, preference):
        user = preference
        for i in preference:
            section = Section.query.filter_by(name=i).first()
            if not(section is None):
                    if (section.weather == "bad" and (self.getWeatherByDay(jour)["pluie"] is False or self.getWeatherByDay(jour)["neige"] is False)) or (section.weather == "good" and (self.getWeatherByDay(jour)["pluie"] is True or self.getWeatherByDay(jour)["neige"] is True or self.getWeatherByDay(jour)["nuage"] == "cloudy" or self.getWeatherByDay(jour)["nuage"] == "partly cloudy")):
                        preference.remove(i)
        if (not preference):
            return user
        else:
            return preference
