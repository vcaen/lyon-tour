# coding=utf-8
import os
import shutil
from lyontour.model.models import Attraction, Section

__author__ = 'Sonia'

import requests
import requests_cache
import urllib
import json
from lyontour.model import models
from lyontour import db, config


requests_cache.install_cache(expire_after=3600)


#from models import Type

client_id = 'LMF4BB0X4XLOO4QGB02QU3XH20Z0HR5ZFCPHLR4KPJR4VTC0'
client_secret = 'L3JAOZNUQ0MIIDWIP5OI44CEJCOIDMCVO22VCQHPTKOTTUQ3'
version = '20130815'
near = 'Lyon'
url = 'https://api.foursquare.com/v2/venues/explore?'
params= {'client_id': client_id, 'client_secret': client_secret, 'near': near, 'v': version}


class FoursquareManager:
    PHOTO_SIZE = "width300"
    PHOTO_EXT = ".jpg"
    VENUES = 'https://api.foursquare.com/v2/venues'
    EXPLORE = VENUES + '/explore?'

    """
        Retreive and save if not exist a photo for the given venue
    """
    def first_photo_url_for_venue(self, venue_id):
        r = requests.get(self.VENUES + '/' + venue_id, params=params)
        if(r.status_code != requests.codes.ok) :
            print "Photo Request Error " + r.status_code
            return None
        photos = r.json()['response']['venue']['photos']
        if photos['count'] > 0 :
            photo = photos['groups'][0]['items'][0]
            photoUrl = photo['prefix'] + self.PHOTO_SIZE + photo['suffix']
            photoUrl.replace('\\', '')
            photoName = config.PHOTO_DIR_PATH+ "/" + venue_id + self.PHOTO_EXT
            if not os.path.exists(photoName) :
                r = requests.get(photoUrl, stream=True)
                if r.status_code == 200:
                    with open(photoName, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                             if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
                                f.flush()
        return venue_id

    def get_venues(self, limit, sections=None):
        if sections is None or len(sections) == 0 :
            resp = Section.query.all()
            listSection = [ x.name for x in resp ]
        else:
            listSection = sections
        listAttraction = set()
        params['limit'] = limit

        for section in listSection:
            params['section'] = section
            response = requests.get(url, params=params)
            # print response.url
            data = json.loads(response.text)
            for val in data["response"]["groups"]:
                for item in val['items']:
                    if db.session.query(Attraction).filter_by(foursquare_id=item['venue']['id']).first():
                        continue
                    attraction = Attraction()
                    # Basics
                    attraction.foursquare_id = item['venue']['id']
                    attraction.name = item['venue']['name']
                    if 'description' in item['venue']:
                        attraction.description = item['venue']['description']
                    elif 'tips' in item:
                        attraction.description = item['tips'][0]['text']

                    # Location
                    if 'location' in item['venue'] :
                        if 'address' in item['venue']['location']:
                            attraction.address = item['venue']['location']['address']
                        if 'lat' in item['venue']['location']:
                            attraction.latitude = item['venue']['location']['lat']
                        if 'lng' in item['venue']['location']:
                            attraction.longitude = item['venue']['location']['lng']
                        if 'postalCode' in item['venue']['location']:
                            attraction.postcode = item['venue']['location']['postalCode']
                        if 'city' in item['venue']['location']:
                            attraction.ville = item['venue']['location']['city']

                    if 'phone' in item['venue']['contact']:
                        attraction.phone = item['venue']['contact']['phone']
                    attraction.section = section

                    attraction.photo = self.first_photo_url_for_venue(attraction.foursquare_id)
                    listAttraction.add(attraction)
                    print attraction.name
        return listAttraction




def executeRequests(limit, listSection=None):

    if not listSection:
        attractions_count = Attraction.query.limit(limit).count()
    else:
        attractions_count = Attraction.query.join(Section).filter(Section.name.in_(listSection)).count()



    if attractions_count < limit :
        foursquare_manager = FoursquareManager()
        attractions = foursquare_manager.get_venues(limit, listSection)
        db.session.add_all(attractions)
        db.session.commit()

    if not listSection:
        return Attraction.query.limit(limit).all()
    else:
        return Attraction.query.join(Section).filter(Section.name.in_(listSection)).all()


if __name__=='__main__':
    executeRequests(10)


