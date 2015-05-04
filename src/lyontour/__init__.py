#  -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from lyontour import config



app = Flask(__name__)
api = Api(app)
app.config.from_object(config)
db = SQLAlchemy(app)
from lyontour.views import status
from lyontour.views import ressources

