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

    def get_categories(self, section, venue):
        if section == 'food':
            if 'categories' in venue:
                for cat in venue['categories']:
                    if "French Restaurant" in cat['name']:
                        print venue['name']
                        return True
                    else:
                        return False
        return True


    def get_venues(self, limit, section):
        # listSection = []
        # if sections is None or len(sections) == 0 :
        #      resp = Section.query.all()
        #      listSection = [ x.name for x in resp ]
        # else:
        #     listSection = sections
        #

        countAttraction = 0
        loop = 0
        listAttraction = set()
        currentLimit = limit
        while(countAttraction<limit):
            loop=loop+1
            if loop > 1:
                currentLimit = currentLimit+10
                params['limit'] = currentLimit
            else:
                params['limit'] = currentLimit

            #for section in listSection:
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

                    if self.get_categories(section, item['venue']) is True:
                        if 'description' in item['venue']:
                            attraction.description = item['venue']['description']
                        elif 'tips' in item:
                            for tip in item['tips']:
                                if "le" in tip['text']:
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
                            if 'postalCode' in item['venue']['location'] and item['venue']['location'] is int:
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
                        countAttraction = countAttraction+1
                        db.session.add(attraction)
        return listAttraction


def executeRequests(limit, listSection=None):
    listAttraction = []
    if listSection is None:
        resp = Section.query.all()
        listSection = [ x.name for x in resp ]

    for section in listSection:
        listAttractionSection = set()
        attractions_count = 0
        for attraction in Attraction.query.join(Section).filter(Section.name==section).limit(limit):
            listAttractionSection.add(attraction)
            attractions_count = attractions_count+1
        if attractions_count < limit :
            foursquare_manager = FoursquareManager()
            for attraction in foursquare_manager.get_venues(limit, section):
                listAttractionSection.add(attraction)
        listAttraction.append(listAttractionSection)
    db.session.commit()
    for section in listAttraction:
        print '   '
        for attraction in section:
            print attraction.name
    return listAttraction

def executeRequests1(limit, listSection=None):
    listAttraction = []
    if listSection is None:
        resp = Section.query.all()
        listSection = [ x.name for x in resp ]

    for section in listSection:
        attractions_count = 0
        for attraction in Attraction.query.join(Section).filter(Section.name==section).limit(limit):
            listAttraction.append(attraction)
            attractions_count = attractions_count+1
        if attractions_count < limit :
            foursquare_manager = FoursquareManager()
            for attraction in foursquare_manager.get_venues(limit, section):
                listAttraction.append(attraction)
    db.session.commit()
    # for section in listAttraction:
    #     print '   '
    #     for attraction in section:
    #         print attraction.name
    return listAttraction


if __name__=='__main__':
    listSection = []
    listSection.append('food')
    #listSection.append('drinks')
    executeRequests(20, listSection)#, listSection)


