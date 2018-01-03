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


class ProfileInfoAddress(NdbModel):
    city = ndb.StringProperty()
    country = ndb.StringProperty()
    label = ndb.StringProperty()
    nr = ndb.StringProperty()
    other = ndb.StringProperty()
    postalcode = ndb.StringProperty()
    street = ndb.StringProperty()


class ProfileInfoAvatar(NdbModel):
    label = ndb.StringProperty()
    source = ndb.StringProperty()


class ProfileInfoBankAccount(NdbModel):
    bic = ndb.StringProperty()
    country = ndb.StringProperty()
    iban = ndb.StringProperty()
    label = ndb.StringProperty()


class ProfileInfoDigitalAssetAddress(NdbModel):
    address = ndb.StringProperty()
    currencysymbol = ndb.StringProperty()
    expire = ndb.StringProperty()
    label = ndb.StringProperty()
    noexpiration = ndb.BooleanProperty()


class ProfileInfoEmailAddress(NdbModel):
    emailaddress = ndb.StringProperty()
    label = ndb.StringProperty()


class ProfileInfoFacebook(NdbModel):
    id = ndb.StringProperty()
    link = ndb.StringProperty()
    name = ndb.StringProperty()
    picture = ndb.StringProperty()


class ProfileInfoGithubAccount(NdbModel):
    avatar_url = ndb.StringProperty()
    html_url = ndb.StringProperty()
    id = ndb.StringProperty()
    login = ndb.StringProperty()
    name = ndb.StringProperty()


class ProfileInfoOwnerOf(NdbModel):
    emailaddresses = ndb.StructuredProperty(ProfileInfoEmailAddress, repeated=True)


class ProfileInfoPhoneNumber(NdbModel):
    label = ndb.StringProperty()
    phonenumber = ndb.StringProperty()


class ProfileInfoPublicKey(NdbModel):
    label = ndb.StringProperty()
    publickey = ndb.StringProperty()


class ProfileInfo(NdbModel):
    """
    Args:
        addresses(list[ProfileInfoAddress])
        avatar(list[ProfileInfoAvatar])
        bankaccounts(list[ProfileInfoBankAccount])
        digitalwallet(list[ProfileInfoDigitalAssetAddress])
        emailaddresses(list[ProfileInfoEmailAddress])
        facebook(ProfileInfoFacebook)
        firstname(unicode)
        github(ProfileInfoGithubAccount)
        lastname(unicode)
        ownerof(ProfileInfoOwnerOf)
        phonenumbers(list[ProfileInfoPhoneNumber])
        publicKeys(list[ProfileInfoPublicKey])
        username(unicode)
        validatedemailaddresses(list[ProfileInfoEmailAddress])
        validatedphonenumbers(list[ProfileInfoPhoneNumber])
    """
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
    def username(self):
        return self.key.id().decode('utf8')

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
