#  -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from lyontour import config



app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config.from_object(config)

from lyontour.views import status
from lyontour.model import models