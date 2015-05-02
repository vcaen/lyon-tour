# coding=utf-8
__author__ = 'Sonia'

import requests
import requests_cache
import urllib
import json
from lyontour.model import models
from lyontour import db


requests_cache.install_cache(expire_after=3600)


#from models import Type

client_id = 'LMF4BB0X4XLOO4QGB02QU3XH20Z0HR5ZFCPHLR4KPJR4VTC0'
client_secret = 'L3JAOZNUQ0MIIDWIP5OI44CEJCOIDMCVO22VCQHPTKOTTUQ3'
version = '20130815'
near = 'Lyon'
url = 'https://api.foursquare.com/v2/venues/explore?'
params= {'client_id': client_id, 'client_secret': client_secret, 'near': near, 'v': version}


def executeRequests(limit, listSection=None):
    if listSection is None or len(listSection) == 0 :
        listSection = models.Section.query.all()
    listAttraction = set()
    params['limit'] = limit
    for section in listSection:
        params['section'] = section.name
        response = requests.get(url, params=params)
        # print response.url
        data = json.loads(response.text)
        for val in data["response"]["groups"]:
            for val2 in val['items']:
                id = val2['venue']['id']
                nom = val2['venue']['name']
                if 'description' not in val2['venue']:
                    description = ''
                else:
                    description = val2['venue']['description']
                if 'location' in val2['venue'] :
                    if 'address' not in val2['venue']['location']:
                        adresse = ''
                    else:
                        adresse = val2['venue']['location']['address']

                    if 'lat' not in val2['venue']['location']:
                        latitude = ''
                    else:
                        latitude = val2['venue']['location']['lat']

                    if 'lng' not in val2['venue']['location']:
                        longitude = ''
                    else:
                        longitude = val2['venue']['location']['lng']

                    if 'postalCode' not in val2['venue']['location']:
                        codePostal = ''
                    else:
                        codePostal = val2['venue']['location']['postalCode']

                    if 'city' not in val2['venue']['location']:
                        ville = ''
                    else:
                        ville = val2['venue']['location']['city']

                if 'phone' not in val2['venue']['contact']:
                    telephone = ' '
                else:
                    telephone = val2['venue']['contact']['phone']

                attraction = models.Attraction(nom, section, description, adresse)
                attraction.foursquare_id = id
                # attraction.hours = 'NULL'
                attraction.latitude = latitude
                attraction.longitude = longitude
                # attraction.photo = 'NULL'
                attraction.postcode = codePostal
                listAttraction.append(attraction)
                db.session.add(attraction)
    for attract in listAttraction:
        print attract.name
    return listAttraction




if __name__=='__main__':
    executeRequests(5)


