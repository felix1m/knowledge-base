# -*- coding: utf-8 -*-
"""
    kb.manage.users
    ~~~~~~~~~~~~~~~~~~~~~

    user management commands
"""

from flask import current_app
from flask.ext.script import Command, prompt, prompt_pass
from flask_security.forms import RegisterForm
from flask_security.registerable import register_user
from werkzeug.datastructures import MultiDict
from flask.ext.security.utils import encrypt_password

from ..services import users


class CreateUserCommand(Command):
    """Creates and returns a new mobile user from the given parameters for API testing."""

    def run(self):
        first_name = prompt('First Name')
        last_name =  prompt('Last Name')

        email = prompt('Email')
        password = prompt('Password')
        password = encrypt_password(password)
        user = users.create(email=email, password=password, first_name=first_name, last_name=last_name)

        return user


class DeleteUserCommand(Command):
    """Delete a user"""

    def run(self):
        email = prompt('Email')
        user = users.first(email=email)
        if not user:
            print 'Invalid user'
            return
        users.delete(user)
        print 'User deleted successfully'


class ListUsersCommand(Command):
    """List all users"""

    def run(self):
        for u in users.all():
            print 'User(id=%s email=%s)' % (u.id, u.email)
