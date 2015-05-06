import lyontour

__author__ = 'vcaen'

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
HOME_DIR = os.path.expanduser('~')

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'mysql://h4312:password@webdb/lyon_tour?charset=utf8'
DATABASE_CONNECT_OPTIONS = {}
PHOTO_DIR_PATH = os.path.abspath(BASE_DIR + "../../../env/local/photos")
if not os.path.exists(PHOTO_DIR_PATH):
    os.makedirs(PHOTO_DIR_PATH)




