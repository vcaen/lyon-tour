from lyontour import config

__author__ = 'vcaen'


class PictureManager:

    def get_picture_path(self, id):
        return config.PHOTO_DIR_PATH + "/" + id + ".jpg"
