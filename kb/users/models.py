# -*- coding: utf-8 -*-
"""
    kb.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""

from flask_security import UserMixin, RoleMixin
from flask_security.utils import verify_password

from ..core import db
from ..helpers import JsonSerializer
import datetime

# many-to-many table between users and roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class RoleJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'name']


class Role(RoleMixin, db.Model, RoleJsonSerializer):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime(), default=datetime.datetime.now())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def verify_password(self, password):
        return verify_password(password, self.password)
