# -*- coding: utf-8 -*-
"""
    kb.users
    ~~~~~~~~~~~~~~

    kb users package
"""


from flask import json
from ..services import mobile_users
import urllib2


def fb_auth(**kwargs):
    fb_user_id = kwargs.get('facebook_user_id')
    token = kwargs.get('facebook_access_token')

    user = mobile_users.user_from_fb_user_id(fb_user_id)

    if user:
        if user.facebook_access_token is not token:
            fb_user = _verify_facebook_credentials(fb_user_id, token)
            if not fb_user:
                return False

            user.facebook_access_token = fb_user["token"]
    else:
        fb_user = _verify_facebook_credentials(fb_user_id, token)
        if not fb_user:
            return False

        user = mobile_users.create_from_facebook(fb_user)

    return user

def _verify_facebook_credentials(fb_user_id, fb_access_token):
    fb_user = _get_user_from_facebook(fb_access_token)
    if fb_user and fb_user['id'] == fb_user_id:
        fb_user["token"] = fb_access_token
        return fb_user
    else:
        return False

def _get_user_from_facebook(fb_access_token):
    url = 'https://graph.facebook.com/me?access_token=' + fb_access_token
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print e.code
        return None
    except urllib2.URLError, e:
        print e.args
        return None

    raw_response = urllib2.urlopen(url).read()
    response = json.loads(raw_response)
    return response
