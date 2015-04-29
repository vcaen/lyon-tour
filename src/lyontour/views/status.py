__author__ = 'vcaen'
from lyontour import api
from flask.ext.restful import Resource

todos = {}
print("status")

class HelloWorld(Resource):
    def get(self):
            return {'hello': 'world'}

api.add_resource(HelloWorld, '/')