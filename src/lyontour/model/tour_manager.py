from sqlalchemy import Enum
from models import Attraction


__author__ = 'vcaen'

import datetime
import json

class Tour:

    def __init__(self, deb, fin, list):
        dateDebut = datetime.datetime.strptime(deb, '%d%m%Y')
        self.DateDebut = str(dateDebut.date())
        dateFin = datetime.datetime.strptime(fin, '%d%m%Y')
        self.DateFin = str(dateFin.date())
        self.nbJour = str((dateFin - dateDebut).days + 1)
        self.PI = []
        self.PI.append(Attraction('Beaux Arts',"Musee", "descrition","Adresse"))
        self.PI.append(Attraction("Tete d'Or","PARC", "descrition","Adresse"))
        self.PI.append(Attraction("Cafe Mokxa","CAFE", "descrition","Adresse"))
        self.Filtre = list



    def toString(self):
        response = JSONObject()
        response.tour = self.__dict__
        return str(response.to_JSON())

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
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, separators=(',', ': '))





