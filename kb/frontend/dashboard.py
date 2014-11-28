# -*- coding: utf-8 -*-


import os
import os.path as op


from flask.ext.admin.contrib import fileadmin

from flask import Blueprint, render_template, jsonify, request, current_app as app
from . import route, admin
from ..settings import APP_UPLOAD

bp = Blueprint('dashboard', __name__)

@route(bp, '/')
def index():
    return render_template('dashboard.html')


path = APP_UPLOAD
print path

# Create admin interface
admin.add_view(fileadmin.FileAdmin(path, '/files/', name='Files'))
