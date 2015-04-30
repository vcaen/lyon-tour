# coding=utf-8
__author__ = 'Sonia'

import requests
import json
#from models import Type

client_id = 'LMF4BB0X4XLOO4QGB02QU3XH20Z0HR5ZFCPHLR4KPJR4VTC0'
client_secret = 'L3JAOZNUQ0MIIDWIP5OI44CEJCOIDMCVO22VCQHPTKOTTUQ3'
version = '20130815'
near = 'Lyon'
url = 'https://api.foursquare.com/v2/venues/explore?'
params= {'client_id': client_id, 'client_secret': client_secret, 'near': near, 'v': version, 'limit': 1}

def executeRequests(*listType):
    for type in listType:
        if type == 'café':
            params['section'] = 'coffee'
            response = requests.get(url, params=params)
            data = json.loads(response.text)
            print data
            for val in data["response"]:
                if val == 'groups':
                print val
            print 'FINISHED'


executeRequests('café')