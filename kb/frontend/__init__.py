# -*- coding: utf-8 -*-
"""
    kb.frontend
    ~~~~~~~~~~~~~~~~~~

    launchpad frontend application package
"""

from functools import wraps

from flask import render_template, jsonify, g, request

from flask_security import login_required

# Imports for Flask-Admin
# from flask_wtf.csrf import CsrfProtect
from ..helpers import JSONEncoder

from .. import factory
from . import assets
from admin import setup_admin
from ..core import KBError, KBFormError

# csrf = CsrfProtect()


def create_app(settings_override=None):
    """Returns the kb dashboard application instance"""
    app = factory.create_app(__name__, __path__, settings_override)
    # Init assets
    assets.init_app(app)
    # csrf.init_app(app)
    setup_admin(app)

    app.json_encoder = JSONEncoder

    # Register custom error handlers
    if not app.debug:
        for e in [500, 404]:
            app.errorhandler(e)(handle_error)
    app.errorhandler(KBError)(on_kb_error)
    app.errorhandler(KBFormError)(on_kb_form_error)

    return app


def handle_error(e):
    e.code = getattr(e, 'code', 500)
    print e
    return render_template('errors/%s.html' % e.code), e.code


def on_kb_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_kb_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator


