__author__ = 'vcaen'
from lyontour import api, app
from flask.ext.restful import Resource
from lyontour.model.tour_manager import Tour
from flask import Flask, request

todos = {}
print("status")


@app.route('/Tour', methods=['POST'])
def Test():
    list = str(request.form['filtre']).split(',')

    return (Tour(request.form['datedebut'], request.form['datefin'], list)).toString()
