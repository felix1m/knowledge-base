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

      roles_to_insert = [
          dict(name='Admin', description='System Administrator; has access to admin panel')
      ]
      for item in roles_to_insert:
          roles.create(**item)

      users_to_insert = [
          ['Philipp', 'Müller', 'philipp@user.de'],
          ['Felix', 'Müller', 'felix@user.de'],
      ]
      for item in users_to_insert:
          users.create(first_name=item[0],
                              last_name=item[1],
                              email=item[2],
                              roles=[roles.by_name('Admin')],
                              password=default_pw)



      # return call_all(CreateContent())


# helper to call all class methods
def call_all(obj, *args, **kwargs):
    for name in dir(obj):
        attribute = getattr(obj, name)
        if ismethod(attribute):
            attribute(*args, **kwargs)



