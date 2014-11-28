# -*- coding: utf-8 -*-
"""
    kb.forms
    ~~~~~~~~~~~~~~

    consolidated forms module
"""

from .core import KBError, KBFormError

# from .products.forms import *
# from .stores.forms import *
from .shouts.forms import *

from flask_wtf import Form as BaseForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import (TextField, PasswordField, TextAreaField, SelectField, BooleanField, RadioField, DateTimeField)
from wtforms.fields.html5 import DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Email

from wtforms.widgets import *
from .models import Industry

from flask_security.views import *
from flask_security.forms import *

import wtforms_json
wtforms_json.init()

class Form(BaseForm):
    """Validates form and returns parsed dict. Raises KBFormError when invalid."""
    def validated_result(self):
        if not self.validate_on_submit():
            raise KBFormError(self.errors)
        return self.patch_data


class BareListWidget(ListWidget):
    def __init__(self, html_tag='div', show_description=True):
        self.html_tag = html_tag
        self.show_description = show_description

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        if self.show_description:
            html.append('%s' % field.label)

        for subfield in field:
            html.append('%s%s' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class CustomRadioField(RadioField):
    widget = BareListWidget()


def get_label(obj):
    return obj.name


class GenderFieldMixin():
    gender = CustomRadioField(u'Geschlecht', [Optional()], choices=[('m', u'männlich'), ('f', u'weiblich')])

class EmailFieldMixin():
    email = TextField('email', validators=[DataRequired(), Email(), Length(min=2, max=160)])




class NewShoutForm(Form, GenderFieldMixin):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.affiliated_users.choices = [('1', u'Nutzer ohne Kundenkarte'),
                                         ('2', u'Nutzer mit Kundenkarte'),
                                         ('3', u'Alle Nutzer')]
        self.industries.query = Industry.query.order_by('name')

    name = TextAreaField('Text des Shouts', validators=[DataRequired(), Length(min=2, max=160)])
    affiliated_users = SelectField(u'Kundenkreis',)
    start = DateField(u'Startdatum', [DataRequired()])
    end = DateField(u'Enddatum', [DataRequired()])
    age_min = IntegerField(u'Alter von', [Optional()])
    age_max = IntegerField(u'Alter bis', [Optional()])
    returning_users = BooleanField(u'Wiederkehrende Nutzer', [Optional()])
    activity = BooleanField(u'Letztlich aktiv', [Optional()])
    budget_cap = DecimalField(u'Shout-Budget', [DataRequired()])
    industries = QuerySelectMultipleField(u'Branchen', [Optional()], get_label=get_label)
    stores = PatchedQuerySelectMultipleField(u'Stores', [PatchedDataRequired()], get_label=get_label)

class NewStoreForm(Form, EmailFieldMixin):
    name = TextField('Name des Stores', validators=[DataRequired(), Length(min=2, max=160)])
    address = TextField(u'Straße & Hausnummer', validators=[DataRequired(), Length(min=2, max=160)])
    city = TextField('Stadt', validators=[DataRequired(), Length(min=2, max=160)])
    zip_code = TextField('Postleitzahl', validators=[DataRequired(), Length(min=2, max=160)])
    country = TextField('Land', validators=[DataRequired(), Length(min=2, max=160)], default='Deutschland')
    phone = TextField('Telefon', validators=[DataRequired(), Length(min=2, max=160)])
    managers = PatchedQuerySelectMultipleField(u'Store Manager', [PatchedDataRequired()], get_label=lambda obj: obj.full_name)



class NewRewardForm(Form):
    name = TextAreaField('Beschreibung', validators=[DataRequired(), Length(min=2, max=160)])
    start = DateField(u'Startdatum', [DataRequired()])
    end = DateField(u'Enddatum', [DataRequired()])
    number_of_kbs_necessary = IntegerField(u'Benötigte kbs', [DataRequired()])
    stores = PatchedQuerySelectMultipleField(u'Stores', [PatchedDataRequired()], get_label=get_label)


class NewRewardClaimForm(Form):
    reward_id = IntegerField(u'Reward ID', [DataRequired()])
    date = DateTimeField(u'Date', [Optional()], format='%Y-%m-%dT%H:%M:%SZ')



class NewShoutShareForm(Form):
    shout_id = IntegerField(u'Shout ID', [DataRequired()])
    date = DateTimeField(u'Date', [Optional()], format='%Y-%m-%dT%H:%M:%SZ')

class NewShoutViewForm(Form):
    shout_id = IntegerField(u'Shout ID', [DataRequired()])
    date = DateTimeField(u'Date', [Optional()], format='%Y-%m-%dT%H:%M:%SZ')


class NewUserStoreAffiliationForm(Form):
    store_id = IntegerField(u'Store ID', [DataRequired()])

class UpdateUserStoreAffiliationForm(Form):
    favorite = BooleanField(u'Favorite')


class NewkbForm(Form):
    kb_device_id = IntegerField(u'kb Device ID', [DataRequired()])
    date = DateTimeField(u'Date', [Optional()], format='%Y-%m-%dT%H:%M:%SZ')


class FacebookLoginForm(Form):
    facebook_user_id = TextField('facebook user ID', [DataRequired(message='FACEBOOK_USER_ID_NOT_PROVIDED')])
    facebook_access_token = PasswordField('facebook access token', [DataRequired(message='FACEBOOK_ACCESS_TOKEN_NOT_PROVIDED')])


class ManualLoginForm(LoginForm):
    pass

class NameFormMixin():
    first_name = TextField(u'first_name', [Optional()])
    last_name = TextField(u'last_name', [Optional()])

class UserRegisterFormMixin(GenderFieldMixin, NameFormMixin):
    birthdate = DateField(u'birthdate', [Optional()])

class RegisterUserForm(ConfirmRegisterForm, UserRegisterFormMixin):
    pass

class UpdateUserForm(Form, UserRegisterFormMixin):
    pass

class RegisterManagerForm(Form, UniqueEmailFormMixin):
    first_name = TextField(u'Vorname', [Optional()])
    last_name = TextField(u'Nachname', [Optional()])
    stores = PatchedQuerySelectMultipleField(u'Stores', [PatchedDataRequired()], get_label=get_label)
    image = FileField(u'Image File', [FileRequired(message=u'Kein Bild ausgewählt'), FileAllowed(('jpg', 'jpeg', 'png'), message=u'Ungültige Datei. Valide Formate: jpg, png')])
