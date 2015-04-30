from sqlalchemy import Enum
from models import Attraction


__author__ = 'vcaen'

import datetime
import json

class TypePI(Enum):
    MUSEE = 1
    PARC = 2
    CAFE = 3

class Tour:

    def __init__(self, dateDeb, dateFin):
        self.DateDebut = datetime.datetime.strptime(dateDeb, '%d/%m/%Y %H:%M')
        self.DateFin = datetime.datetime.strptime(dateFin, '%d/%m/%Y %H:%M')
        self.nbJour = (self.DateFin - self.DateDebut).days + 1

        response = JSONObject()
        response.DateDebut = str(self.DateDebut)
        response.DateFin = str(self.DateFin)
        response.nbJour = str(self.nbJour)

        response.PI = []
        response.Jours = []
        for i in range(0,self.nbJour,1):
            Temp = (self.DateDebut + datetime.timedelta(days = i))
            response.Jours.append(Jour(str(Temp)))

        response.PI.append(Attraction('Beaux Arts',TypePI.MUSEE, "descrition","Adresse" ))
        response.PI.append(Attraction("Tete d'Or",TypePI.PARC, "descrition","Adresse"))
        response.PI.append(Attraction("Cafe Mokxa",TypePI.CAFE, "descrition","Adresse"))

        self.response = response

    def toString(self):
        return str(self.response.to_JSON())

class Jour:
    def __init__(self, date):
        self.date = date

class JSONObject:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, separators=(',', ': '))





