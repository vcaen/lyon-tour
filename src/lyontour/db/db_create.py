#!/usr/bin/python
#  -*- coding: utf-8 -*-

from lyontour import db
from lyontour.model.models import Section
import os.path

print "Creating Database..."
db.drop_all()
db.create_all()
print "Database created"

print "Filling Section table .."
food = Section("food", "whatever", "whatever", 2)
drinks = Section("drinks", "whatever", "evening/night", 3)
coffee = Section("coffee", "whatever", "evening/night", 2)
shops = Section("shops", "bad", "morning/evening", 4)
arts = Section("arts", "bad", "evening", 2)
outdoors = Section("outdoors", "good", "day", 3)
sights = Section("sights", "good", "day", 3)

db.session.add(food)
db.session.add(drinks)
db.session.add(coffee)
db.session.add(shops)
db.session.add(arts)
db.session.add(outdoors)
db.session.add(sights)
db.session.commit()
print "Section table Filled "