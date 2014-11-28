# -*- coding: utf-8 -*-
# [SublimeLinter flake8-max-line-length:110]

'''
    manage
    ~~~~~~

    Manager module
'''

from flask.ext.script import Manager
from flask import current_app
from kb.core import db

from kb.api import create_app
from kb.manage import DeleteUserCommand, ListUsersCommand, CreateMobileUserCommand, SeedDatabase


# create manager instance
manager = Manager(create_app())


@manager.command
def seed():
    """Seeds the database with realistic test data."""
    SeedDatabase().seed(current_app)


@manager.shell
def make_shell_context():
    return dict(app=current_app, db=db)


# manager.add_command('delete_user', DeleteUserCommand())
# manager.add_command('list_users', ListUsersCommand())
# manager.add_command('create_mobile_user', CreateMobileUserCommand())
# manager.add_command('seed', SeedDatabaseCommand())

if __name__ == '__main__':
    manager.run()
