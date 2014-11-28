# -*- coding: utf-8 -*-
"""
    kb.users
    ~~~~~~~~~~~~~~~

    kb users services
"""

from .models import *
from ..core import Service, kbError

from flask import json, current_app, g

import urllib2, urllib
from sqlalchemy.exc import IntegrityError

from flask.ext.security import current_user, user_registered
from flask.ext.security.utils import encrypt_password, config_value
from flask.ext.security.confirmable import generate_confirmation_link

from werkzeug.local import LocalProxy
_security = LocalProxy(lambda: current_app.extensions['security'])

class UserService(Service):
    __model__ = User

    def current(self):
        user = current_user
        if not user:
            raise kbError(u'No current user')
        return user._get_current_object()

    def update_current(self, **kwargs):
        user = self.current()
        valid_keys = ['gender', 'birthdate', 'first_name', 'last_name']
        items = {k: v for k, v in kwargs.items() if k in valid_keys}
        return super(UserService, self).update(user, **items)

    def create(self, **kwargs):
        kwargs['password'] = encrypt_password(kwargs['password'])
        user = self.new(**kwargs)
        self.after_register(user)
        return self.save(user)

    def after_register(self, user):
        user.active = True

        if _security.confirmable:
            confirmation_link, token = generate_confirmation_link(user)

        if config_value('SEND_REGISTER_EMAIL'):
            send_mail(config_value('EMAIL_SUBJECT_REGISTER'), user.email, 'welcome',
                      user=user, confirmation_link=confirmation_link)


class RoleService(Service):
    __model__ = Role

    def by_name(self, name):
        return self.find(name=name).first()


def generate_random_pw():
    secret_key = current_app.config.get('SECRET_KEY')
    return _security.login_serializer.dumps(secret_key)
