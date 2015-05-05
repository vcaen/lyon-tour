#!/usr/bin/python
#  -*- coding: utf-8 -*-


import lyontour.model.models


def destroy():
    print "Destroying Database"
    db.drop_all()

def create():
    print "Creating Database..."
    db.create_all()
    print "Database created"

def populate_sections():
    from lyontour.model.models import Section
    print "Filling Section table .."
    sections = [
        Section("food", "whatever", "eat", 2),
        Section("drinks", "whatever", "evening/night", 2),
        Section("coffee", "whatever", "day", 1),
        Section("shops", "bad", "day", 1),
        Section("arts", "bad", "day", 3),
        Section("outdoors", "good", "day/evening", 2),
        Section("sights", "good", "day/evening", 1)
    ]
    db.session.add_all(sections)
    db.session.commit();
    print "Section table Filled "

if __name__=='__main__':
    from lyontour import db
    destroy()
    create()
    populate_sections()