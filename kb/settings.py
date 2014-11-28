# -*- coding: utf-8 -*-
"""
    kb.settings
    ~~~~~~~~~~~~~~~

    kb settings module
"""

import os


DEBUG = True
SECRET_KEY = 'super-secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql://root@db_1:3306/kb'

# CELERY_BROKER_URL = 'redis://33.33.33.10:6379/0'

MAX_CONTENT_LENGTH = 1 * 1024 * 1024 # 1mb


SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_PASSWORD_HASH = 'des_crypt'
SECURITY_PASSWORD_SALT = 'password_salt'
SECURITY_REMEMBER_SALT = 'remember_salt'
SECURITY_RESET_SALT = 'reset_salt'
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_CONFIRMABLE = False


SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
# SECURITY_REGISTERABLE = True

JSON_AS_ASCII = False

DEFAULT_LOCALE = 'de'
# BABEL_DEFAULT_TIMEZONE = 'utc'

LANGUAGES = {
    'de': 'Deutsch',
    'en': 'English'
}

APP_ROOT = os.path.abspath(os.path.join(__file__, '..'))  # refers to application_top
APP_UPLOAD = os.path.join(APP_ROOT, 'files')

try:
    os.mkdir(APP_UPLOAD)
except OSError:
    pass
