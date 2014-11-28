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


class UserStoreAffiliationJsonSerializer(JsonSerializer):
    __json_hidden__ = ['user', 'store']


# many-to-many table between users and stores
class UserStoreAffiliation(UserStoreAffiliationJsonSerializer, db.Model):
    __tablename__ = 'user_store_affiliation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('mobile_users.id'))
    store_id = db.Column(db.Integer(), db.ForeignKey('stores.id'))
    favorite = db.Column(db.Boolean())
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    user = db.relationship('MobileUser', backref=db.backref('affiliations', lazy='dynamic'))


# many-to-many table between users and roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


stores_managers = db.Table(
    'stores_managers',
    db.Column('manager_id', db.Integer(), db.ForeignKey('store_managers.id')),
    db.Column('store_id', db.Integer(), db.ForeignKey('stores.id')))


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
    type = db.Column(db.String(50))

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

    __mapper_args__ = {
            'polymorphic_identity':'user',
            'polymorphic_on':type
        }

class MobileUserJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'gender', 'birthdate', 'first_name', 'last_name', 'email']

class MobileUser(MobileUserJsonSerializer, User):
    __tablename__ = 'mobile_users'
    __mapper_args__ = {'polymorphic_identity': 'mobile_user'}

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    facebook_user_id = db.Column(db.String(512))
    facebook_access_token = db.Column(db.String(512))
    birthdate = db.Column(db.DateTime())
    gender = db.Column(db.String(1))

    def age(self):
        today = datetime.date.today()
        born = self.birthdate
        if born is None:
            return 35 # FIXME: Think about what to do in this case
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class StoreManagerJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'first_name', 'last_name', 'email', 'customer_id', 'image_path']

class StoreManager(StoreManagerJsonSerializer, User):
    __tablename__ = 'store_managers'
    # same issue as in MobileUser
    __mapper_args__ = {'polymorphic_identity': 'store_manager'}

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    customer = db.relationship('Customer',
                               backref=db.backref('managers', lazy='dynamic'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    stores = db.relationship('Store', secondary=stores_managers, lazy='dynamic',
                             backref=db.backref('managers', lazy='dynamic'))

    image = db.Column(db.String(512), default='profile.png')

    @property
    def image_path(self):
        return 'img/managers/' + self.image

