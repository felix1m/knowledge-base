# -*- coding: utf-8 -*-


import os
import os.path as op


from flask import Blueprint, render_template, jsonify, request, current_app as app
from . import route, admin
from ..git import receive_hook


bp = Blueprint('dashboard', __name__)

@route(bp, '/')
def index():
    return render_template('dashboard.html')



@bp.route('/githook', methods=['POST'])
def receive():
    return receive_hook()
