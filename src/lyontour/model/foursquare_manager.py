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
    def first_photo_for_venue(self, venue_id):
        r = requests.get(self.VENUES + '/' + venue_id, params=params)
        if(r.status_code != requests.codes.ok) :
            print "Photo Request Error " + str(r.status_code)
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

    def has_local_photo_for_venue(self, venue_id):
        photoName = config.PHOTO_DIR_PATH+ "/" + venue_id + self.PHOTO_EXT
        return os.path.exists(photoName)

    def get_venues(self, limit, sections=None):
        print "getvenue"
        if sections is None or len(sections) == 0 :
            resp = Section.query.all()
            listSection = [ x.name for x in resp ]
        else:
            listSection = sections
        listAttraction = set()
        params['limit'] = limit

        print "\n".join(listSection)

        for section in listSection:
            params['section'] = section
            response = requests.get(url, params=params)
            # print response.url
            data = json.loads(response.text)
            for val in data["response"]["groups"]:
                for item in val['items']:
                    venue_id = item['venue']['id']
                    if db.session.query(Attraction).filter_by(foursquare_id=venue_id).first():
                        if not self.has_local_photo_for_venue(venue_id):
                            self.first_photo_for_venue(venue_id)
                        continue
                    attraction = Attraction()
                    # Basics
                    attraction.foursquare_id = venue_id
                    attraction.name = item['venue']['name']
                    if 'description' in item['venue']:
                        attraction.description = item['venue']['description']
                    elif 'tips' in item:
                        for tip in item['tips']:
                            if "e" in tip['text'] or "a" in tip['text']:
                                attraction.description = tip['text']
                                break

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
                    attraction.section = Section.query.filter_by(name=section).first()

                    if 'rating' in item['venue']:
                        attraction.rating = round(item['venue']['rating'],0)

                    attraction.photo = self.first_photo_for_venue(attraction.foursquare_id)
                    listAttraction.add(attraction)
                    #print attraction.name.encode('UTF-8')

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

    #print "limit " + str(limit)

    if not listSection:
        a = Attraction.query.limit(limit).all()
    else:
        a =  Attraction.query.join(Section).filter(Section.name.in_(listSection)).all()
    print "\n".join([x.name.encode('UTF-8') for x in a ])

    return a


if __name__=='__main__':
    executeRequests(10)


