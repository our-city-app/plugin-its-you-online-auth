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


class ProfileInfoAddress(ndb.Model):
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    label = ndb.StringProperty()
    nr = ndb.StringProperty()
    other = ndb.StringProperty()
    postalcode = ndb.StringProperty()
    street = ndb.StringProperty()


class ProfileInfoAvatar(ndb.Model):
    label = ndb.StringProperty()
    source = ndb.StringProperty()


class ProfileInfoBankAccount(ndb.Model):
    bic = ndb.StringProperty()
    country = ndb.StringProperty()
    iban = ndb.StringProperty()
    label = ndb.StringProperty()


class ProfileInfoDigitalAssetAddress(ndb.Model):
    address = ndb.StringProperty()
    currencysymbol = ndb.StringProperty()
    expire = ndb.StringProperty()
    label = ndb.StringProperty()
    noexpiration = ndb.BooleanProperty()


class ProfileInfoEmailAddress(ndb.Model):
    emailaddress = ndb.StringProperty()
    label = ndb.StringProperty()


class ProfileInfoFacebook(ndb.Model):
    id = ndb.StringProperty()
    link = ndb.StringProperty()
    name = ndb.StringProperty()
    picture = ndb.StringProperty()


class ProfileInfoGithubAccount(ndb.Model):
    avatar_url = ndb.StringProperty()
    html_url = ndb.StringProperty()
    id = ndb.StringProperty()
    login = ndb.StringProperty()
    name = ndb.StringProperty()


class ProfileInfoOwnerOf(ndb.Model):
    emailaddresses = ndb.StructuredProperty(ProfileInfoEmailAddress, repeated=True)


class ProfileInfoPhoneNumber(ndb.Model):
    label = ndb.StringProperty()
    phonenumber = ndb.StringProperty()


class ProfileInfoPublicKey(ndb.Model):
    label = ndb.StringProperty()
    publickey = ndb.StringProperty()


class ProfileInfo(ndb.Model):
    NAMESPACE = NAMESPACE
    addresses = ndb.StructuredProperty(ProfileInfoAddress, repeated=True)
    avatar = ndb.StructuredProperty(ProfileInfoAvatar, repeated=True)
    bankaccounts = ndb.StructuredProperty(ProfileInfoBankAccount, repeated=True)
    digitalwallet = ndb.StructuredProperty(ProfileInfoDigitalAssetAddress, repeated=True)
    emailaddresses = ndb.StructuredProperty(ProfileInfoEmailAddress, repeated=True)
    facebook = ndb.StructuredProperty(ProfileInfoFacebook)
    firstname = ndb.StringProperty()
    github = ndb.StructuredProperty(ProfileInfoGithubAccount)
    lastname = ndb.StringProperty()
    ownerof = ndb.StructuredProperty(ProfileInfoOwnerOf)
    phonenumbers = ndb.StructuredProperty(ProfileInfoPhoneNumber, repeated=True)
    publicKeys = ndb.StructuredProperty(ProfileInfoPublicKey, repeated=True)
    username = ndb.StringProperty()
    validatedemailaddresses = ndb.StructuredProperty(ProfileInfoEmailAddress, repeated=True)
    validatedphonenumbers = ndb.StructuredProperty(ProfileInfoPhoneNumber, repeated=True)


class Profile(NdbModel):
    NAMESPACE = NAMESPACE
    organization_id = ndb.StringProperty()  # Only used in case user must be member of a suborganization to login
    app_email = ndb.StringProperty()  # Only use in case the deployed server is used for one app (and only one)
    language = ndb.StringProperty(indexed=False)
    info = ndb.LocalStructuredProperty(ProfileInfo)  # type: ProfileInfo

    @property
    def source(self):
        return self.key.parent().id().decode('utf8')

    @property
    def username(self):
        return self.key.id().decode('utf8')

    @classmethod
    def create_key(cls, username):
        return ndb.Key(cls, username, namespace=NAMESPACE)

    def to_dict(self):
        result = super(Profile, self).to_dict()
        del result['organization_id']
        del result['app_email']
        result['username'] = self.username
        return result
