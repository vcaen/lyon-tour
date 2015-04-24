#  -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

from lyontour.views import status