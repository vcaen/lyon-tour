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

    def __init__(self, liste_jours=None, preferences_user=None):
        self.filtred_attractions = self.getAttractionFiltred(liste_jours, preferences_user)

    def getWeatherByDay(self, jour):
        date_jour = datetime.datetime.strptime(jour, '%Y%m%d').date()
        date_formatee = date_jour.year + "-" + date_jour.month + "-" + date_jour.day
        # to_day = datetime.datetime.now().date()
        # if date_jour < to_day:
        #     return "erreur, date passée \n"
        #else:
            #rain = WeatherDay.query.filter_by(date=jour).first().rain
        day = WeatherDay.query.get(jour)
        weather_day = {}
        weather_day["date"] = date_jour
        if not(day is None):
            weather_day["temp"] = day.temp
            weather_day["nuage"] = day.cloud
            weather_day["pluie"] = day.rain <= 2
            weather_day["neige"] = day.snow
            return weather_day
        else:
            f = urllib2.urlopen(meteo_api_url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            f.close()
            weather_day["temp"] = parsed_json[date_formatee + ' 12:00:00']["temperature"]["sol"] - 273,15
            weather_day["pluie"] = parsed_json[date_formatee + ' 12:00:00']["pluie"]
            if parsed_json[jour + ' 12:00:00']["nebulosite"]["totale"] < 10:
                weather_day["nuage"] = "sunny"
            elif parsed_json[date_formatee + ' 12:00:00']["nebulosite"]["totale"] >= 10 and parsed_json[date_formatee + ' 12:00:00']["nebulosite"]["totale"] < 50:
                weather_day["nuage"] = "partly cloudy"
            else:
                weather_day["nuage"] = "partly cloudy"
            weather_day["neige"] = parsed_json[date_formatee + ' 12:00:00']["snow"] == "oui"
            weather_day["pluie"] = day.rain >= 2
            weather_day["snow"] = day.snow
            day = WeatherDay(date_jour, weather_day["temp"], weather_day["nuage"], weather_day["pluie"], weather_day["snow"])
            db.session.add(day)
            db.session.commit()
            return weather_day


    # on ne s'en sert plus !
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

    # on ne s'en sert plus !
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
                    if (section.weather == "bad" and (self.getWeatherByDay(jour)["pluie"] is False or self.getWeatherByDay(jour)["neige"] is False)) or (section.weather == "good" and (self.getWeatherByDay(jour)["pluie"] is True or self.getWeatherByDay(jour)["neige"] is True or self.getWeatherByDay(jour)["nuage"] == "cloudy" or self.getWeatherByDay(jour)["nuage"] == "partly cloudy")):
                        preference.remove(i)
        return preference

