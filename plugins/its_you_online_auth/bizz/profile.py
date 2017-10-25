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
import base64
import logging
import re

from google.appengine.api import search
from google.appengine.ext import ndb

from framework.bizz.job import run_job
from framework.models.session import Session
from mcfw.cache import cached
from mcfw.exceptions import HttpNotFoundException
from mcfw.rpc import returns, arguments
from plugins.its_you_online_auth.libs.itsyouonline import Client
from plugins.its_you_online_auth.models import Profile, ProfileInfo, ProfileInfoAddress, ProfileInfoAvatar, \
    ProfileInfoBankAccount, ProfileInfoEmailAddress, ProfileInfoDigitalAssetAddress, ProfileInfoFacebook, \
    ProfileInfoOwnerOf, ProfileInfoPhoneNumber, ProfileInfoPublicKey, ProfileAppEmailMapping
from plugins.its_you_online_auth.plugin_consts import NAMESPACE

PROFILE_INDEX = search.Index('profile', namespace=NAMESPACE)


def _get_best_session(sessions):
    sorted_sessions = sorted(sessions, key=lambda s: len(s.scopes))
    return sorted_sessions[0] if sorted_sessions and sorted_sessions[0].jwt else None


def set_user_information(profile_key):
    profile = profile_key.get()  # type: Profile
    sessions = Session.list_active_user(profile.username)
    session = _get_best_session(sessions)
    if session:
        client = Client()
        client.oauth.session.headers['Authorization'] = 'bearer %s' % session.jwt
        data = client.api.users.GetUserInformation(session.user_id).json()
        logging.info('Saving user information %s', data)
        profile.info = ProfileInfo(addresses=[ProfileInfoAddress(**address) for address in data['addresses']],
                                   avatar=[ProfileInfoAvatar(**avatar) for avatar in data['avatar']],
                                   bankaccounts=[ProfileInfoBankAccount(**bank) for bank in data['bankaccounts']],
                                   digitalwallet=[ProfileInfoDigitalAssetAddress(**wallet) for wallet in
                                                  data['digitalwallet']],
                                   emailaddresses=[ProfileInfoEmailAddress(**email) for email in
                                                   data['emailaddresses']],
                                   facebook=ProfileInfoFacebook(**data['facebook']),
                                   firstname=data['firstname'],
                                   lastname=data['lastname'],
                                   ownerof=ProfileInfoOwnerOf(
                                       emailaddresses=[ProfileInfoEmailAddress(**email) for email in
                                                       data['ownerof']['emailaddresses']]),
                                   phonenumbers=[ProfileInfoPhoneNumber(**phone) for phone in data['phonenumbers']],
                                   publicKeys=[ProfileInfoPublicKey(**phone) for phone in data['publicKeys']],
                                   username=data['username'],
                                   validatedemailaddresses=[ProfileInfoEmailAddress(**email) for email in
                                                            data['validatedemailaddresses']],
                                   validatedphonenumbers=[ProfileInfoPhoneNumber(**phone) for phone in
                                                          data['validatedphonenumbers']])
        profile.put()
    else:
        logging.info('No session found for user %s, not storing user information', profile.username)
    index_profile(profile)


def index_all_profiles():
    run_job(_get_all_profiles, [], index_profile, [])


def _get_all_profiles():
    return Profile.query()


def index_profile(profile_or_key):
    # type: (ndb.Key) -> list[search.PutResult]
    profile = profile_or_key.get() if isinstance(profile_or_key, ndb.Key) else profile_or_key
    logging.info('Indexing profile %s', profile.username)
    document = create_profile_document(profile)
    return PROFILE_INDEX.put(document)


def create_profile_document(profile):
    # type: (Profile) -> search.Document
    fields = [search.AtomField(name='username', value=profile.username.lower())]
    # complete this if needed
    if profile.info:
        if profile.info.firstname:
            fields.append(search.TextField(name='firstname', value=profile.info.firstname.lower()))
        if profile.info.lastname:
            fields.append(search.TextField(name='lastname', value=profile.info.lastname.lower()))
        if profile.info.validatedemailaddresses:
            for i, mail in enumerate(profile.info.validatedemailaddresses):
                fields.append(search.AtomField(name='validatedemailaddresses_%d' % i, value=mail.emailaddress))
            mails = ' '.join([email.emailaddress for email in profile.info.validatedemailaddresses])
            fields.append(search.TextField(name='validatedemailaddresses', value=mails))
        if profile.info.validatedphonenumbers:
            for i, phone in enumerate(profile.info.validatedphonenumbers):
                fields.append(search.AtomField(name='validatedphonenumbers_%d' % i, value=phone.phonenumber))
            phones = ' '.join([phone.phonenumber for phone in profile.info.validatedphonenumbers])
            fields.append(search.TextField(name='validatedphonenumbers', value=phones))
    return search.Document(_encode_doc_id(profile), fields)


def _encode_doc_id(profile):
    # doc id must be ascii, base64 encode it
    return base64.b64encode(profile.username.encode('utf-8'))


def _decode_doc_id(doc_id):
    # type: (unicode) -> unicode
    return base64.b64decode(doc_id)


def normalize_search_string(search_string):
    return re.sub(r'[, \"+-:><=\\()~]', u' ', search_string)


def get_profile(username):
    """
    Args:
        username (unicode)
    Returns:
        Profile

    Raises:
        HttpNotFoundException in case the profile was not found
    """
    profile = Profile.create_key(username).get()
    if not profile:
        raise HttpNotFoundException('profile_not_found', {'username': username})
    return profile


def get_or_create_profile(username, app_email=None):
    profile_key = Profile.create_key(username)
    profile = profile_key.get() or Profile(key=profile_key)
    if app_email:
        profile.app_email = app_email
        mapping_key = ProfileAppEmailMapping.create_key(app_email)
        mapping_key.get() or ProfileAppEmailMapping(key=mapping_key, username=username).put()
    return profile


def search_profiles(query='', page_size=20, cursor=None):
    # type: (unicode, int, unicode) -> tuple[list[Profile], search.Cursor, bool]
    sort_expressions = [search.SortExpression(expression='firstname', direction=search.SortExpression.ASCENDING),
                        search.SortExpression(expression='lastname', direction=search.SortExpression.ASCENDING),
                        search.SortExpression(expression='username', direction=search.SortExpression.ASCENDING)]
    options = search.QueryOptions(limit=page_size,
                                  cursor=search.Cursor(cursor),
                                  sort_options=search.SortOptions(expressions=sort_expressions),
                                  ids_only=True)
    search_results = PROFILE_INDEX.search(
        search.Query(normalize_search_string(query), options=options))  # type: search.SearchResults
    results = search_results.results  # type: list[search.ScoredDocument]
    keys = []
    for result in results:
        username = _decode_doc_id(result.doc_id)
        keys.append(Profile.create_key(username))
    profiles = ndb.get_multi(keys) if keys else []
    return profiles, search_results.cursor, search_results.cursor is not None


@cached(1, lifetime=0)
@returns(unicode)
@arguments(rogerthat_email=unicode)
def get_username_from_rogerthat_email(rogerthat_email):
    # type: (unicode) -> unicode
    mapping = ProfileAppEmailMapping.create_key(rogerthat_email).get()
    return mapping and mapping.username


@returns(dict)
@arguments(rogerthat_emails=[unicode])
def get_usernames_from_rogerthat_emails(rogerthat_emails):
    # type: (list[unicode]) -> dict[unicode, unicode]
    result = {}
    mappings = ndb.get_multi([ProfileAppEmailMapping.create_key(app_email) for app_email in rogerthat_emails])
    for app_email, mapping in zip(rogerthat_emails, mappings):
        if mapping:
            result[app_email] = mapping.username
        else:
            logging.error('No ProfileAppEmailMapping found for app email %s!', app_email)
            result[app_email] = None
    return result


@cached(1, lifetime=0)
@returns(unicode)
@arguments(username=unicode)
def get_rogerthat_email_from_username(username):
    # type: (unicode) -> unicode
    profile = Profile.create_key(username).get()
    return profile and profile.app_email
