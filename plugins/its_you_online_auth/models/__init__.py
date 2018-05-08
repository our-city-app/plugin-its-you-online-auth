# -*- coding: utf-8 -*-
# Copyright 2017 GIG Technology NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @@license_version:1.3@@

from google.appengine.ext import ndb

from framework.models.common import NdbModel
from plugins.its_you_online_auth.libs import itsyouonline
from plugins.its_you_online_auth.plugin_consts import NAMESPACE


class OauthState(NdbModel):
    NAMESPACE = NAMESPACE
    timestamp = ndb.IntegerProperty(indexed=False)
    organization_id = ndb.StringProperty(indexed=False)
    source = ndb.StringProperty(indexed=False)
    completed = ndb.BooleanProperty(indexed=False)

    app_redirect_uri = ndb.StringProperty(indexed=False)

    @property
    def state(self):
        return self.key.id().decode('utf8')

    @classmethod
    def create_key(cls, state):
        return ndb.Key(cls, state, namespace=NAMESPACE)


class Profile(NdbModel):
    NAMESPACE = NAMESPACE
    organization_id = ndb.StringProperty()  # Only used in case user must be member of a suborganization to login
    app_email = ndb.StringProperty()  # Only use in case the deployed server is used for one app (and only one)
    language = ndb.StringProperty(indexed=False)
    information = ndb.JsonProperty()

    @property
    def username(self):
        return self.key.id().decode('utf8')

    @property
    def full_name(self):
        if self.info and self.info.firstname:
            return '%s %s' % (self.info.firstname, self.info.lastname)

    @property
    def email(self):
        if self.info:
            if self.info.validatedemailaddresses:
                return self.info.validatedemailaddresses[0].emailaddress
            if self.info.emailaddresses:
                return self.info.emailaddresses[0].emailaddress

    @property
    def info(self):
        return self.information and itsyouonline.userview(self.information)

    @property
    def phone(self):
        if self.info:
            if self.info.validatedphonenumbers:
                return self.info.validatedphonenumbers[0].phonenumber
            if self.info.phonenumbers:
                return self.info.phonenumbers[0].phonenumber

    @classmethod
    def create_key(cls, username):
        return ndb.Key(cls, username, namespace=NAMESPACE)

    @classmethod
    def list_with_app_user(cls):
        return cls.query(cls.app_email != None)  # noQA

    def to_dict(self, extra_properties=None, include=None, exclude=None):
        if not extra_properties:
            extra_properties = ['username']
        if not exclude:
            exclude = {'organization_id'}
        return super(Profile, self).to_dict(extra_properties, include, exclude)


class ProfileAppEmailMapping(NdbModel):
    username = ndb.StringProperty(indexed=False)

    @classmethod
    def create_key(cls, app_email):
        return ndb.Key(cls, app_email, namespace=NAMESPACE)

    @property
    def app_email(self):
        return self.key.id().decode('utf8')
