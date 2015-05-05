# coding=utf-8
import flask
from lyontour.model.picture_manager import PictureManager
from lyontour.model.tour_manager import Tour



__author__ = 'vcaen'

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import marshal_with
from lyontour import api
from Schema import tour_schema, filter_schema
from lyontour.model.tour_manager import Tour
from lyontour.model.filter_manager import filter_manager



# class AttractionResource(Resource):
#
#     FILTRE = 'filtre'
#     DATEFIN = 'datefin'
#     DATEDEBUT = 'datedebut'
#
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument(AttractionResource.DATEDEBUT, type=str, required=True, help='Merci de donner une date de début')
#         parser.add_argument(AttractionResource.DATEFIN, type=str, required=True, help="Merci de donner une date de fin")
#         parser.add_argument(AttractionResource.FILTRE, type=str, action='append')
#         args = parser.parse_args()
#
#         return tour_schema.dump(Tour(args[AttractionResource.DATEDEBUT],
#                      args[AttractionResource.DATEFIN],
#                      args[AttractionResource.FILTRE])).data
#
#
# api.add_resource(AttractionResource, '/attraction')

class PhotoResource(Resource):

    def get(self, photo_id):
        picture_manager = PictureManager()
        return flask.send_file(picture_manager.get_picture_path(photo_id), mimetype='image/jpeg')


api.add_resource(PhotoResource, '/photo/<string:photo_id>')

class filter_test(Resource):
    FILTRE = 'filtre'
    DATEFIN = 'datefin'
    DATEDEBUT = 'datedebut'

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(filter_test.DATEDEBUT, type=str, required=True, help='Merci de donner une date de début')
        parser.add_argument(filter_test.DATEFIN, type=str, required=True, help="Merci de donner une date de fin")
        parser.add_argument(filter_test.FILTRE, type=str, action='append')
        args = parser.parse_args()
        tour = Tour(args[filter_test.DATEDEBUT], args[filter_test.DATEFIN], args[filter_test.FILTRE])
        f_manager = filter_manager(tour.getJours(), args[filter_test.FILTRE])
        return "coucou"
        #return filter_schema.dump(f_manager).data
api.add_resource(filter_test, '/attraction')