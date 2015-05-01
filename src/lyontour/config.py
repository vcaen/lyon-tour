__author__ = 'vcaen'

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "../../../env/local/database/migrate")
HOME_DIR = os.path.expanduser('~')

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'mysql://h4312:password@127.0.0.1/lyon_tour'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')



