# -*- coding: utf-8 -*-
"""
    kb.factory
    ~~~~~~~~~~~~~~~~

    kb factory module
"""

import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .core import db, mail, security, api_manager
from .helpers import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware
from .models import User, Role
from .logger import setup_logging


def create_app(package_name, package_path, settings_override=None,
               register_security_blueprint=True, create_api_manager=False):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the kb platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults
                                        to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('kb.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)
    mail.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint)

    if create_api_manager:
        # Init the Flask-Restless API manager.
        api_manager.init_app(app, flask_sqlalchemy_db=db)

    register_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    if not app.debug:
        setup_logging(app)

    return app
