# -*- coding: utf-8 -*-
# Copyright 2016 Mobicage NV
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

from google.appengine.ext import ndb
from mcfw.exceptions import HttpBadRequestException, HttpException, HttpForbiddenException
from plugin_loader import get_config
from plugins.its_you_online_auth.libs.itsyouonline import Client
from plugins.its_you_online_auth.models import OauthLoginState, Profile
from plugins.its_you_online_auth.plugin_consts import Scopes, OAUTH_BASE_URL, NAMESPACE
from plugins.its_you_online_auth.plugin_utils import get_sub_organization
import requests


def get_access_response(config, login_state, code):
    params = {
        'client_id': config.root_organization.name,
        'client_secret': config.root_organization.web.client_secret,
        'code': code,
        'redirect_uri': config.root_organization.web.redirect_uri,
        'state': login_state.state
    }
    access_token_url = '%s/access_token?%s' % (OAUTH_BASE_URL, urllib.urlencode(params))
    response = requests.post(access_token_url, params)

    content = response.json() if response.status_code == httplib.OK else response.content
    logging.debug('access_response: code %d, content %s', response.status_code, content)
    return response.status_code, content


def has_access_to_organization(client, organization_id, username):
    r = client.api.organizations.GetOrganizationUsers(organization_id).json()
    for u in r.get('users', []):
        if u['username'] == username:
            return True
    return False


def get_user_scopes(code, state):
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

    status_code, access_result = get_access_response(config, login_state, code)
    if status_code != httplib.OK:
        exception = HttpException()
        exception.http_code = status_code
        exception.error = access_result
        raise exception

    username = access_result['info']['username']
    scope = access_result.get('scope')


    if login_state.client_id == config.root_organization.name:
        if login_state.source == "app":
            raise HttpForbiddenException()
        else:
            sub_org = login_state.client_id
    else:
        sub_org = get_sub_organization(config, login_state.client_id)

    expected_scope = 'user:memberof:%s' % sub_org
    if not scope or expected_scope not in scope:
        raise HttpForbiddenException()

    profile_key = Profile.create_key(login_state.source, username)
    profile = profile_key.get() or Profile(key=profile_key)
    profile.access_token = access_result.get('access_token')
    profile.client_id = login_state.client_id
    login_state.completed = True
    ndb.put_multi([profile, login_state])

    client = Client()
    client.oauth.LoginViaClientCredentials(config.root_organization.name, config.root_organization.web.client_secret)

    scopes = []
    uber_admin_organization = '%s.admins' % config.root_organization.name
    admin_organization = '%s.admins' % sub_org
    if has_access_to_organization(client, uber_admin_organization, username):
        scopes.append(Scopes.ADMIN)
    if has_access_to_organization(client, admin_organization, username):
        scopes.append(Scopes.get_organization_scope(Scopes.ORGANIZATION_ADMIN, login_state.client_id))
        scopes.append(Scopes.get_organization_scope(Scopes.ORGANIZATION_MEMBER, login_state.client_id))
    elif not has_access_to_organization(client, sub_org, username):
        raise HttpForbiddenException()
    return username, scopes
