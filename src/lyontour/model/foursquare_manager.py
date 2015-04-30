# coding=utf-8
__author__ = 'Sonia'

import requests
import json
from lyontour.model import models
from lyontour import db


#from models import Type

client_id = 'LMF4BB0X4XLOO4QGB02QU3XH20Z0HR5ZFCPHLR4KPJR4VTC0'
client_secret = 'L3JAOZNUQ0MIIDWIP5OI44CEJCOIDMCVO22VCQHPTKOTTUQ3'
version = '20130815'
near = 'Lyon'
url = 'https://api.foursquare.com/v2/venues/explore?'
params= {'client_id': client_id, 'client_secret': client_secret, 'near': near, 'v': version}


def executeRequests(limit, listSection):
    listAttraction = []
    params['limit'] = limit
    for section in listSection:
        params['section'] = section.name
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        for val in data["response"]["groups"]:
            for val2 in val['items']:
                id = val2['venue']['id']
                nom = val2['venue']['name']
                #type = val2['venue']['categories'][0]['name']
                if 'description' not in val2['venue']:
                    description = ''
                else:
                    description = val2['venue']['description']
                if 'address' not in val2['venue']['location']:
                    adresse = ''
                else:
                    adresse = val2['venue']['location']['address']
                latitude = val2['venue']['location']['lat']
                longitude = val2['venue']['location']['lng']
                codePostal = val2['venue']['location']['postalCode']
                ville = val2['venue']['location']['city']
                if 'phone' not in val2['venue']['contact']:
                    telephone = ' '
                else:
                    telephone = val2['venue']['contact']['phone']

                attraction = models.Attraction(nom, section, description, adresse)
                # attraction.address = adresse
                # #attraction.description = description
                # attraction.foursquare_id = id
                # attraction.hours = 'NULL'
                # attraction.latitude = latitude
                # attraction.longitude = longitude
                # attraction.name = nom
                # attraction.photo = 'NULL'
                # attraction.postcode = codePostal
                # attraction.type = type

                listAttraction.append(attraction)
                
    return listAttraction

section = models.Section()
section.name = 'coffee'
section.id = 1
db.session.add(section)
section2 = models.Section()
section2.name = 'arts'
section2.id = 2
db.session.add(section2)
listSection = []
listSection.append(section)
listSection.append(section2)
executeRequests(5, listSection)
