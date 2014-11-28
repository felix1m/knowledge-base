# -*- coding: utf-8 -*-
# [SublimeLinter flake8-max-line-length:200]
"""
    kb.manage.seed_database
    ~~~~~~~~~~~~~~~~~~~~~~~~

    inserts sample data for kb api testing
"""

from flask.ext.security.utils import encrypt_password
from datetime import date, timedelta
from ..models import *
from ..services import *
from kb.core import db

import random

from inspect import ismethod


today = date.today()
default_start_date = today
default_end_date = date(2016,6,30)
default_pw = 'testpw'


class SeedDatabase():
    def seed(self, app):




        # return call_all(CreateContent())


# helper to call all class methods
def call_all(obj, *args, **kwargs):
    for name in dir(obj):
        attribute = getattr(obj, name)
        if ismethod(attribute):
            attribute(*args, **kwargs)



