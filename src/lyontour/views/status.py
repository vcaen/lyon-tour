__author__ = 'vcaen'
from lyontour import api, app
from flask.ext.restful import Resource
from lyontour.model.tour_manager import Jour,Tour
from flask import Flask, request

todos = {}
print("status")


@app.route('/', methods=['POST'])
def Test():
    return (Tour(request.form['DateDebut'], request.form['DateFin'])).toString()



