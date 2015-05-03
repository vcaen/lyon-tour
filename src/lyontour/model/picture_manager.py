from lyontour import config
import os
from lyontour.model.foursquare_manager import FoursquareManager

__author__ = 'vcaen'


class PictureManager:

    def get_picture_path(self, id):

        path = config.PHOTO_DIR_PATH + "/" + id + ".jpg"
        if not os.path.exists(path):
            fm = FoursquareManager()
            fm.first_photo_for_venue(id)

        return path
