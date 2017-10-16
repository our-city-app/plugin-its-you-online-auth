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
from mcfw.exceptions import HttpNotFoundException
from plugins.its_you_online_auth.libs.itsyouonline import Client
from plugins.its_you_online_auth.models import Profile, ProfileInfo, ProfileInfoAddress, ProfileInfoAvatar, \
    ProfileInfoBankAccount, ProfileInfoEmailAddress, ProfileInfoDigitalAssetAddress, ProfileInfoFacebook, \
    ProfileInfoOwnerOf, ProfileInfoPhoneNumber, ProfileInfoPublicKey
from plugins.its_you_online_auth.plugin_consts import NAMESPACE, SOURCE_WEB, SOURCE_APP

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
                                   validatedphonenumbers=[ProfileInfoEmailAddress(**phone) for phone in
                                                          data['validatedphonenumbers']])
        profile.put()
    else:
        logging.info('No session found for profile %s, not storing user information')


def index_all_profiles():
    run_job(_get_all_profiles, [], index_profile, [])


def _get_all_profiles():
    return Profile.query()


def index_profile(profile_key):
    # type: (ndb.Key) -> list[search.PutResult]
    profile = profile_key.get()
    logging.info('Indexing profile %s', profile.username)
    document = create_investment_agreement_document(profile)
    return PROFILE_INDEX.put(document)


def create_investment_agreement_document(profile):
    # type: (Profile) -> search.Document
    fields = [search.AtomField(name='username', value=profile.username)]
    # complete this if needed
    if profile.info:
        if profile.info.firstname:
            fields.append(search.TextField(name='firstname', value=profile.info.firstname))
        if profile.info.lastname:
            fields.append(search.TextField(name='lastname', value=profile.info.lastname))
        if profile.info.validatedemailaddresses:
            for i, mail in enumerate(profile.info.validatedemailaddresses):
                fields.append(search.AtomField(name='validatedemailaddresses_%d' % i, value=mail.emailaddress))
            mails = ' '.join([email.emailaddress for email in profile.info.validatedemailaddresses])
            fields.append(search.TextField(name='validatedemailaddresses', value=mails))
    return search.Document(
        doc_id=_encode_doc_id(profile),
        fields=fields)


def _encode_doc_id(profile):
    # doc id must be ascii, base64 encode it
    # crappy hardcoded separator because having 'source' as parent was apparently a good idea
    return base64.b64encode('%s__separator__%s' % (profile.username.encode('utf-8'), profile.source.encode('utf-8')))


def _decode_doc_id(doc_id):
    # type: (unicode) -> tuple[unicode, unicode]
    return base64.b64decode(doc_id).split('__separator__')


def normalize_search_string(search_string):
    return re.sub(u'[, \"+\-:><=\\\\()~]', u' ', search_string)


def get_profile(username, fallback=True):
    """
    Args:
        username (unicode)
        fallback (bool): Fallback to web profile when app profile was not found
    Returns:
        Profile

    Raises:
        HttpNotFoundException in case the profile was not found
    """
    profile = Profile.create_key(SOURCE_APP, username).get()
    if not profile and fallback:
        profile = Profile.create_key(SOURCE_WEB, username).get()
    if not profile:
        raise HttpNotFoundException('profile_not_found', {'username': username})
    return profile


def search_profiles(query='', page_size=20, cursor=None):
    # type: (unicode, int, unicode) -> tuple[list[Profile], search.Cursor, bool]
    logging.warn(cursor)
    options = search.QueryOptions(limit=page_size,
                                  cursor=search.Cursor(cursor),
                                  ids_only=True)
    search_results = PROFILE_INDEX.search(
        search.Query(normalize_search_string(query), options=options))  # type: search.SearchResults
    results = search_results.results  # type: list[search.ScoredDocument]
    keys = []
    for result in results:
        username, source = _decode_doc_id(result.doc_id)
        keys.append(Profile.create_key(source, username))
    profiles = ndb.get_multi(keys)
    return profiles, search_results.cursor, search_results.cursor is not None
