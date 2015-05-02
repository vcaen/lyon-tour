from sqlalchemy import Enum
from models import Attraction, Section
from foursquare_manager import executeRequests


__author__ = 'vcaen'

import datetime
import json

class Tour:

    def __init__(self, deb, fin, list=None):
        dateDebut = datetime.datetime.strptime(deb, '%d%m%Y')
        self.DateDebut = str(dateDebut.date())
        dateFin = datetime.datetime.strptime(fin, '%d%m%Y')
        self.DateFin = str(dateFin.date())
        self.nbJour = str((dateFin - dateDebut).days + 1)
        # self.PI.append(Attraction('Beaux Arts',"Musee", "descrition","Adresse"))
        # self.PI.append(Attraction("Tete d'Or","PARC", "descrition","Adresse"))
        # self.PI.append(Attraction("Cafe Mokxa","CAFE", "descrition","Adresse"))
        self.Filtre = list



        self.PI = executeRequests(self.nbJour, list)



    def toString(self):
        response = JSONObject()
        response.dateDebut = self.DateDebut
        response.dateFin = self.DateFin
        response.filtre = self.Filtre
        response.PI = []
        for a in self.PI:
            item = JSONObject()
            item.nom = a.name
            item.description = a.description
            item.adresse = a.address
            item.codePostal = a.postcode
            item.id = a.id
            response.PI.append(item)

        return str(response.toJson())

class Itineraire:
    def __init__(self):
        self.Jours = []
        for i in range(0,self.nbJour,1):
            Temp = ((self.DateDebut + datetime.timedelta(days = i)).date())
            self.Jours.append(Jour(str(Temp)))

class Jour:
    def __init__(self, date):
        self.date = date

class JSONObject:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4, separators=(',', ': '))








