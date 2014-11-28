# -*- coding: utf-8 -*-


import os
import os.path as op


from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import AdminIndexView
from flask.ext.security import current_user
from flask.ext.security.utils import encrypt_password
from flask import Blueprint, render_template, jsonify, request, current_app as app

from ..settings import APP_UPLOAD
from ..models import User
from ..core import db, admin
from wtforms.fields import PasswordField

def allowed():
    return (current_user.is_authenticated() and current_user.has_role('Admin'))


# the view that gets used for the admin home page
class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return allowed()


class CustomFileAdmin(FileAdmin):
    can_mkdir = False
    can_delete_dirs = False
    allowed_extensions = ('jpeg', 'jpg', 'gif', 'png', 'pdf')

    def is_accessible(self):
        return allowed()

class UserAdmin(ModelView):
    column_exclude_list = list = ('password',)
    form_excluded_columns = ('password',)
    column_auto_select_related = True

    def is_accessible(self):
        return allowed()

    def scaffold_form(self):

        form_class = super(UserAdmin, self).scaffold_form()

        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = encrypt_password(model.password2)


path = APP_UPLOAD


def setup_admin(app):
    admin.index_view = AdminIndex()
    admin.init_app(app)
    # Create admin interface
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(CustomFileAdmin(path, '/files/', name='Static Files'))


