from sqlalchemy import Enum


__author__ = 'vcaen'

import datetime
import json

class TypePI(Enum):
    MUSEE = 1
    PARC = 2
    CAFE = 3

class Tour:

    def __init__(self, dateDeb, dateFin):
        self.m_DateDebut = datetime.datetime.strptime(dateDeb, '%d/%m/%Y %H:%M')
        self.m_DateFin = datetime.datetime.strptime(dateFin, '%d/%m/%Y %H:%M')
        self.m_nbJour = (self.m_DateFin - self.m_DateDebut).days + 1

        self.jours = []
        for i in range(0,self.m_nbJour,1):
            self.jours.append(Jour(datetime.timedelta(i)))

            response = JSONObject()
            response.DateDebut = str(self.m_DateDebut)
            response.DateFin = str(self.m_DateFin)
            response.nbJour = str(self.m_nbJour)
            response.Jours = []
            response.PI = []

            response.PI.append(PointDInteret('Beaux Arts',TypePI.MUSEE))
            response.PI.append(PointDInteret("Tete d'Or",TypePI.PARC))
            response.PI.append(PointDInteret("Café Mokxa",TypePI.CAFE))

        self.response = response

    def toString(self):
        return str(self.response.to_JSON())

class Jour:

    def __init__(self, date):
        self.m_date = date

class PointDInteret:
    def __init__(self, nom, type):
        self.m_nom = nom
        self.m_type = type


class JSONObject:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, separators=(',', ': '))





