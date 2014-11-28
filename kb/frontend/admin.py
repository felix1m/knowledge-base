# -*- coding: utf-8 -*-


import os
import os.path as op


from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import AdminIndexView
from flask.ext.security import current_user
from flask.ext.security.utils import encrypt_password
from flask import Blueprint, render_template, jsonify, request, current_app as app, send_file

from ..settings import APP_REPOS, APP_FILES
from ..models import User
from ..core import db, admin
from wtforms.fields import PasswordField

def allowed():
    return (current_user.is_authenticated() and current_user.has_role('Admin'))

# the view that gets used for the admin home page
class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return allowed()

class BaseFileAdmin(FileAdmin):
    def is_accessible(self):
        return allowed()

    def is_accessible_path(self, path):
        if len(path):
             return path[0] != '.'
        return True


class CustomFileAdmin(BaseFileAdmin):
    can_mkdir = False
    can_delete_dirs = False
    allowed_extensions = ('jpeg', 'jpg', 'gif', 'png', 'pdf')


class RepoAdmin(BaseFileAdmin):
    can_mkdir = False
    can_delete = False
    can_rename = False
    can_delete_dirs = False
    can_upload = False


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


def setup_admin(app):
    admin.index_view = AdminIndex()
    # Create admin interface
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(CustomFileAdmin(APP_FILES, '/files/', name='Static Files'))
    admin.add_view(RepoAdmin(APP_REPOS, '/repos/', name='Git Repos'))
    admin.init_app(app)


bp = Blueprint('static-files', __name__)

@bp.route('/repos/<path:path>')
def static_repos(path):
    path = path.replace("..","")
    return send_file(os.path.join(APP_REPOS, path))

@bp.route('/files/<path:path>')
def static_files(path):
    path = path.replace("..","")
    return send_file(os.path.join(APP_FILES, path))
