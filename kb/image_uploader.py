# -*- coding: utf-8 -*-
"""
    kb.image_uploader
    ~~~~~~~~~~~~~~~~

    kb image uploader module
"""
import uuid
import os
from flask import current_app as app
import boto
from boto.s3.key import Key


# valid groups:
# - "store_manager"
# - "customer"

# returns the resulting filename
def upload_image(file, group=None, random_name=True):
    if file :
        if random_name:
            extension = os.path.splitext(file.filename)[1][1:]
            file.filename = '.'.join(str(uuid.uuid4()), extension)
        else:
            file.filename = secure_filename(file.filename)

        if app.config['USE_S3_FOR_UPLOADS']:
            save_to_s3(file, group)
        else:
            save_locally(file, group)

        return file.filename

# e.g. https://s3-eu-west-1.amazonaws.com/kb-upload/store_manager/dummy_avatar.png
def save_to_s3(file, group):
    key = '/'.join(group, file.filename) if group else file.filename
    upload_to_bucket(app.config.get('S3_UPLOAD_BUCKET_NAME'), key)

def create_s3_connection():
    return boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"], app.config["AWS_SECRET_ACCESS_KEY"])

def upload_to_bucket(bucket_name, key):
    s3 = create_s3_connection()
    bucket = s3.get_bucket(s3_upload_bucket_name())
    k = Key(bucket, key)
    k.set_contents_from_string(file.read())


def save_locally(file, group):
    path = os.path.join(app.config['LOCAL_UPLOAD_FOLDER'], group)
    ensure_path_exists(path)

    file.save(os.path.join(path, file.filename))


def ensure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
