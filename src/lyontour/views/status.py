__author__ = 'vcaen'
from lyontour import api, app
from flask.ext.restful import Resource
from lyontour.model.tour_manager import Tour
from lyontour.model.filter_manager import filter_manager
from flask import Flask, request


todos = {}


@app.route('/tour', methods=['POST', 'GET'])
def Test():
    if(request.method == 'POST'):
        list = str(request.form['filtre']).split(',')
        return (Tour(request.form['datedebut'], request.form['datefin'], list)).toString()
    else:
        filtres = request.args.get('filtre')
        if filtres is None:
            list = {}
        else:
            list = str(request.args.get('filtre')).split(',')
        return (Tour(request.args.get('datedebut'),request.args.get('datefin'), list)).toString()

# @app.route('/')
# def Test():
#     tour = Tour('2015-06-04','2015-06-10')
#     liste_jours = tour.getJours()
#     filtre_user = ['shops', 'arts']
#     filtre_manager = filter_manager()
#     attractions = filtre_manager.getAttractionFiltred(liste_jours, filtre_user)
#     print("Hello World")
#     print ('%s',str(attractions))
#     return (str(attractions))