# -*- coding: utf-8 -*-
# Copyright 2017 Green IT Globe NV
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
# @@license_version:1.1@@

import httplib
import logging
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import requests
from framework.plugin_loader import get_config
from jose import jwt
from mcfw.consts import DEBUG
from mcfw.exceptions import HttpBadRequestException, HttpException, HttpForbiddenException
from plugins.its_you_online_auth.libs.itsyouonline import Client
from plugins.its_you_online_auth.models import OauthLoginState, Profile
from plugins.its_you_online_auth.plugin_consts import Scopes, OAUTH_BASE_URL, NAMESPACE, SOURCE_WEB, \
    ITS_YOU_ONLINE_PUBLIC_KEY, JWT_AUDIENCE, JWT_ISSUER
from plugins.its_you_online_auth.plugin_utils import get_sub_organization
from plugins.its_you_online_auth.to import ItsYouOnlineConfiguration


def get_access_response(config, login_state, code, use_jwt=None, scope=None, audience=None):
    params = {
        'client_id': config.root_organization.name,
        'client_secret': config.root_organization[SOURCE_WEB].client_secret,
        'code': code,
        'redirect_uri': config.root_organization[SOURCE_WEB].redirect_uri,
        'state': login_state.state
    }
    if use_jwt:
        params['response_type'] = 'id_token'
        params['scope'] = scope
        params['aud'] = audience
    access_token_url = '%s/access_token?%s' % (OAUTH_BASE_URL, urllib.urlencode(params))
    response = requests.post(access_token_url, params)

    if use_jwt:
        content = response.content
    else:
        content = response.json() if response.status_code == httplib.OK else response.content
    logging.debug('access_response: code %d, content %s', response.status_code, content)
    if response.status_code != httplib.OK:
        exception = HttpException()
        exception.http_code = response.status_code
        exception.error = content
        if use_jwt and response.status_code == httplib.UNAUTHORIZED:
            logging.error('https://github.com/itsyouonline/identityserver/issues/436')
        raise exception
    return content


def refresh_jwt(old_jwt):
    logging.debug('JWT expired, attempting to refresh')
    url = '{}/jwt/refresh'.format(OAUTH_BASE_URL)
    headers = {
        'Authorization': 'bearer {jwt}'.format(jwt=old_jwt)
    }
    data = urlfetch.fetch(url, headers=headers)
    if data.status_code == 200:
        return data.content
    logging.debug('Failed to refresh JWT\n{}: {}'.format(data.status_code, data.content))
    if DEBUG:
        logging.debug(old_jwt)
    e = HttpException()
    e.http_code = data.status_code
    e.error = data.content
    raise e


def has_access_to_organization(client, organization_id, username):
    r = client.api.organizations.GetOrganizationUsers(organization_id).json()
    for u in r.get('users', []):
        if u['username'] == username:
            return True
    return False


def get_user_scopes_from_access_token(code, state):
    """
    Args:
        code (unicode)
        state (unicode)
    """
    if not (code or state):
        logging.debug('Code or state are missing.\nCode: %s\nState:%s', code, state)
        raise HttpBadRequestException()

    login_state = OauthLoginState.create_key(state).get()
    if not login_state:
        logging.debug('Login state not found')
        raise HttpBadRequestException()

    config = get_config(NAMESPACE)
    assert isinstance(config, ItsYouOnlineConfiguration)

    access_result = get_access_response(config, login_state, code)

    username = access_result['info']['username']
    scope = access_result.get('scope')

    if login_state.organization_id == config.root_organization.name:
        if login_state.source == "app":
            raise HttpForbiddenException()
        else:
            users_organization = login_state.organization_id
    else:
        users_organization = get_sub_organization(config, login_state.organization_id)

    admins_organization = users_organization.replace('.users', '.admins')
    expected_scope = 'user:memberof:%s' % users_organization
    if not scope or expected_scope not in scope:
        raise HttpForbiddenException()

    save_profile_state(access_result.get('access_token'), login_state, username)

    client = Client()
    client.oauth.LoginViaClientCredentials(config.root_organization.name,
                                           config.root_organization[SOURCE_WEB].client_secret)

    scopes = []
    if has_access_to_organization(client, config.root_organization.name, username):
        scopes.append(Scopes.ADMIN)
    if has_access_to_organization(client, admins_organization, username):
        scopes.append(Scopes.get_organization_scope(Scopes.ORGANIZATION_ADMIN, login_state.organization_id))
        scopes.append(Scopes.get_organization_scope(Scopes.ORGANIZATION_MEMBER, login_state.organization_id))
    elif not has_access_to_organization(client, users_organization, username):
        raise HttpForbiddenException()
    return username, scopes


def save_profile_state(access_token_or_jwt, login_state, username):
    profile_key = Profile.create_key(login_state.source, username)
    profile = profile_key.get() or Profile(key=profile_key)
    profile.access_token = access_token_or_jwt
    profile.organization_id = login_state.organization_id
    login_state.completed = True
    ndb.put_multi([profile, login_state])


def get_jwt(code, state, scope=''):
    """
    Args:
        code (unicode)
        state (unicode)
        scope (unicode)
    """
    if not (code or state):
        logging.debug('Code or state are missing.\nCode: %s\nState:%s', code, state)
        raise HttpBadRequestException()

    login_state = OauthLoginState.create_key(state).get()
    if not login_state:
        logging.debug('Login state not found')
        raise HttpBadRequestException()

    config = get_config(NAMESPACE)  # type: ItsYouOnlineConfiguration
    json_web_token = get_access_response(config, login_state, code, True, scope, audience=JWT_AUDIENCE)
    decoded_jwt = jwt.decode(json_web_token, str(ITS_YOU_ONLINE_PUBLIC_KEY), audience=JWT_AUDIENCE,
                             issuer=JWT_ISSUER)
    if decoded_jwt['azp'] != config.root_organization.name:
        logging.error('Received invalid JWT: %s', decoded_jwt)
        raise HttpForbiddenException()
    username = decoded_jwt['username']
    scopes = []
    save_profile_state(json_web_token, login_state, username)
    return json_web_token, username, scopes
