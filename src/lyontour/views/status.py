from landscape.lib.fs import touch_file

__author__ = 'vcaen'
from lyontour import api, app
from lyontour.model.filter_manager import filter_manager
from lyontour.model.tour_manager import Tour
from flask.ext.restful import Resource
import urllib2
import json
import datetime

todos = {}
print("status")

@app.route('/')
def test():
    # dateDebut = "29/04/2015 12:00"
    # dateFin = "06/05/2015 12:00"
    # tour = Tour(dateDebut, dateFin)
    # f = urllib2.urlopen('http://www.infoclimat.fr/public-api/gfs/json?_ll=45.74846,4.84671&_auth=ARtXQA9xVnRVeAYxAnRReFU9U2ZbLQcgCnYGZVoyVSgHY1c3Vj0AZlA5BnsHKFJiV3oDa1tgUmwBZQdhCHoDfwFgVzoPZVYyVTMGYAI2UXpVeVMuW2UHIAp2BmBaNFUyB3pXMVY0AGZQIQZlBz9Sbld6A2JbYlJoAX0HfwhkA2QBYVczD29WNFU6BmMCNFFiVXlTLFthBzoKbQZhWmZVPgdhV2VWNABmUG4GZgc%2BUmJXegNlW2RSYwFqB2UIZwNpAWdXLA9zVk1VSQZ5AnJRJ1UzU3VbeQdqCjcGNQ%3D%3D&_c=cd00e152c42b3f31881e89f4f263728c')
    # json_string = f.read()
    # parsed_json = json.loads(json_string)
    # f.close()
    #for i in tour.getJours:
        # temp = parsed_json[i.getDate() + ' 12:00:00']["temperature"]["2m"]
        # pluie = parsed_json[i.getDate() + ' 12:00:00']["pluie"]
        # vent = parsed_json[i.getDate() + ' 12:00:00']["vent_moyen"]["10m"]
        # neige = parsed_json[i.getDate() + ' 12:00:00']["risque_neige"]
        # temp = temp - 273.15
        # print("date: %s \n Temp: %d \n Rain: %d \n Snow: %s \n wind: %d", i.getDate(), temp, pluie, neige, vent)
        # if pluie <= 2.5 and neige == "non":
        #     return  "it does not rain nor snow in Lyon, you should go out :-D \n"
        # elif pluie > 2.5 and neige == "non":
        #     return "it's raining in Lyon, you should go in ;-( \n"
        # elif pluie < 2.5 and neige == "oui":
        #     return "it's snowing in Lyon, you should go in ;-( \n"
        # elif pluie > 2.5 and neige == "oui":
        #     return "it's raining and snowing in Lyon, you should go in ;-( \n"
        # else:
        #     return "erreur \n"
    f_manager = filter_manager()
    #return "Rain: " + str(f_manager.getRainByDay("2015-04-30")) + "\n Snow: " + f_manager.getSnowByDay("2015-04-30")
    preference = ["food", "drinks", "coffee", "shops", "arts", "outdoors", "sights"]
    return str(f_manager.filtre_meteo("2015-04-30", preference))