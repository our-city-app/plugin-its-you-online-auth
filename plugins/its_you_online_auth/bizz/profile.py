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
from mcfw.cache import cached
from mcfw.exceptions import HttpNotFoundException
from mcfw.rpc import returns, arguments
from transliterate import slugify

from framework.bizz.job import run_job
from framework.models.session import Session
from framework.plugin_loader import get_plugins
from framework.utils import convert_to_str
from plugins.its_you_online_auth.models import Profile, ProfileInfo, ProfileInfoAddress, ProfileInfoAvatar, \
    ProfileInfoBankAccount, ProfileInfoEmailAddress, ProfileInfoDigitalAssetAddress, ProfileInfoFacebook, \
    ProfileInfoOwnerOf, ProfileInfoPhoneNumber, ProfileInfoPublicKey, ProfileAppEmailMapping
from plugins.its_you_online_auth.plugin_consts import NAMESPACE

PROFILE_INDEX = search.Index('profile', namespace=NAMESPACE)


def _get_best_session(sessions):
    sorted_sessions = sorted(sessions, key=lambda s: len(s.scopes))
    return sorted_sessions[0] if sorted_sessions and sorted_sessions[0].jwt else None


def set_user_information(profile_key, session_key=None):
    from plugins.its_you_online_auth.bizz.authentication import get_itsyouonline_client_from_jwt
    iyo_username = profile_key.id()
    if session_key:
        session = session_key.get()
    else:
        sessions = Session.list_active_user(iyo_username)
        session = _get_best_session(sessions)
    if session:
        client = get_itsyouonline_client_from_jwt(session.jwt)
        data = client.api.users.GetUserInformation(convert_to_str(session.user_id)).json()
        logging.info('Saving user information %s', data)
        store_user_information(data)
    else:
        logging.info('No session found for user %s, not storing user information', iyo_username)


def store_user_information(data):
    profile = Profile.create_key(data['username']).get()
    profile.info = ProfileInfo(addresses=[ProfileInfoAddress(**address) for address in data['addresses']],
                               avatar=[ProfileInfoAvatar(**avatar) for avatar in data['avatar']],
                               bankaccounts=[ProfileInfoBankAccount(**bank) for bank in data['bankaccounts']],
                               digitalwallet=[ProfileInfoDigitalAssetAddress(**wallet) for wallet in
                                              data['digitalwallet']],
                               emailaddresses=[ProfileInfoEmailAddress(**email) for email in data['emailaddresses']],
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
    index_profile(profile, _get_extra_profile_fields(profile))


def _get_extra_profile_fields(profile):
    fields = []
    for plugin in get_plugins():
        if hasattr(plugin, 'get_extra_profile_fields'):
            fields.extend(plugin.get_extra_profile_fields(profile))
    return fields


def index_all_profiles():
    remove_all_from_index(PROFILE_INDEX)
    run_job(_get_all_profiles, [], index_profile, [])


def _get_all_profiles():
    return Profile.query()


def index_profile(profile_or_key, extra_profile_fields=None):
    # type: (ndb.Key, list[search.Field]) -> list[search.PutResult]
    profile = profile_or_key.get() if isinstance(profile_or_key, ndb.Key) else profile_or_key
    if extra_profile_fields is None:
        extra_profile_fields = _get_extra_profile_fields(profile)
    logging.debug('Indexing profile %s\nExtra fields: %s', profile.username, extra_profile_fields)
    document = create_profile_document(profile, extra_profile_fields)
    return PROFILE_INDEX.put(document)


def _add_slug_fields(key, value):
    if not value:
        return []
    value = value.lower().strip()
    return [
        search.TextField(name=key, value=value),
        search.TextField(name='%s_slug' % key, value=slugify(value) or value)
    ]


def create_profile_document(profile, extra_profile_fields):
    # type: (Profile, list[search.Field]) -> search.Document
    fields = [search.AtomField(name='username', value=profile.username.lower())]
    # complete this if needed
    if profile.info:
        fields.extend(_add_slug_fields('firstname', profile.info.firstname))
        fields.extend(_add_slug_fields('lastname', profile.info.lastname))
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
    else:
        # Adding username as firstname/lastname for sorting reasons
        fields.append(search.TextField(name='firstname_slug', value=profile.username.lower()))
        fields.append(search.TextField(name='lastname_slug', value=profile.username.lower()))
    fields.extend(extra_profile_fields)
    return search.Document(_encode_doc_id(profile), fields)


def _encode_doc_id(profile):
    # doc id must be ascii, base64 encode it
    return base64.b64encode(profile.username.encode('utf-8'))


def _decode_doc_id(doc_id):
    # type: (unicode) -> unicode
    return base64.b64decode(doc_id)


def normalize_search_string(search_string):
    return re.sub(r'[,\"\+\-:><=\\()~]', u' ', search_string)


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
    sort_expressions = [search.SortExpression(expression='firstname_slug', direction=search.SortExpression.ASCENDING),
                        search.SortExpression(expression='lastname_slug', direction=search.SortExpression.ASCENDING),
                        search.SortExpression(expression='username', direction=search.SortExpression.ASCENDING)]
    options = search.QueryOptions(limit=page_size,
                                  cursor=search.Cursor(cursor),
                                  sort_options=search.SortOptions(expressions=sort_expressions),
                                  ids_only=True)
    search_results = PROFILE_INDEX.search(search.Query(query, options=options))  # type: search.SearchResults
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


def remove_all_from_index(index):
    # type: (search.Index) -> long
    total = 0
    while True:
        result = index.search(search.Query(u'', options=search.QueryOptions(ids_only=True, limit=1000)))
        if not result.results:
            break
        logging.debug('Deleting %d documents from %s' % (len(result.results), index))
        total += len(result.results)
        for rpc in [index.delete_async([r.doc_id for r in chunk]) for chunk in chunks(result.results, 200)]:
            rpc.get_result()
    logging.info('Deleted %d documents from %s', total, index)
    return total
