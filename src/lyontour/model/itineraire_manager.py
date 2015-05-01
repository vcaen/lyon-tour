
import json

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4, separators=(',', ': '))

class CalculItineraire:
    def __init__(self):
        pass

    def getTest(self):
        me = Object()
        me.DateDebut = "28/04/15"
        me.DateFin = "30/04/15"
        me.Etape = []
        for i in range(1,10):
            me.Etape.append(str(i))


        return me.to_JSON()
