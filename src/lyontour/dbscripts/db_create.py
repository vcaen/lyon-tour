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
        Section("food", "whatever", "whatever", 2),
        Section("drinks", "whatever", "evening/night", 3),
        Section("coffee", "whatever", "evening/night", 2),
        Section("shops", "bad", "morning/evening", 4),
        Section("arts", "bad", "evening", 2),
        Section("outdoors", "good", "day", 3),
        Section("sights", "good", "day", 3)
    ]

    db.session.add_all(sections)
    db.session.commit();
    print "Section table Filled "

if __name__=='__main__':
    from lyontour import db
    destroy()
    create()
    populate_sections()