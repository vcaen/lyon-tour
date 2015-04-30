#!/usr/bin/python
#  -*- coding: utf-8 -*-

from lyontour import db
import os.path
from lyontour.model.models import Type

print "Creating Database..."
db.drop_all()
db.create_all()
print "Database created"



