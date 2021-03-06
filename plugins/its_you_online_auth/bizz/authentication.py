# -*- coding: utf-8 -*-
# Copyright 2019 Green Valley Belgium NV
# NOTICE: THIS FILE HAS BEEN MODIFIED BY GREEN VALLEY BELGIUM NV IN ACCORDANCE WITH THE APACHE LICENSE VERSION 2.0
# Copyright 2018 GIG Technology NV
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
# @@license_version:1.6@@

import hashlib
import httplib
import logging
import time
import urllib
from urlparse import urlparse

from google.appengine.api import urlfetch, memcache
from google.appengine.api.app_identity import get_default_version_hostname
from google.appengine.ext import ndb

import requests
from framework.bizz.authentication import get_current_session
from framework.consts import get_base_url
from framework.models.session import Session
from framework.plugin_loader import get_config, get_auth_plugin, get_plugin
from framework.utils import now, urlencode, convert_to_str
from jose import jwt, ExpiredSignatureError
from mcfw.cache import cached
from mcfw.consts import DEBUG
from mcfw.exceptions import HttpException, HttpForbiddenException, HttpUnAuthorizedException
from mcfw.rpc import returns, arguments
from plugins.its_you_online_auth.bizz.profile import get_or_create_profile
from plugins.its_you_online_auth.libs import itsyouonline
from plugins.its_you_online_auth.plugin_consts import Scopes, NAMESPACE, JWT_ISSUER, \
    SOURCE_WEB
from plugins.its_you_online_auth.plugin_utils import get_users_organization, get_organization
from plugins.its_you_online_auth.to.config import ItsYouOnlineConfiguration


def get_iyo_plugin():
    # type: () -> ItsYouOnlineAuthPlugin
    from plugins.its_you_online_auth.its_you_online_auth_plugin import ItsYouOnlineAuthPlugin
    p = get_plugin(NAMESPACE)
    assert isinstance(p, ItsYouOnlineAuthPlugin)
    return p


def get_itsyouonline_client():
    # type: () -> itsyouonline.Client
    plugin = get_iyo_plugin()
    organization = plugin.configuration.root_organization.name
    client_secret = plugin.configuration.root_organization[SOURCE_WEB].client_secret
    if not organization:
        raise Exception('Missing configuration: root_organization.name must be set')
    if not client_secret:
        raise Exception('Missing configuration: root_organization.web.client_secret must be set')
    client = itsyouonline.Client(base_uri=plugin.api_uri)
    client.organizations.client.session.headers['Authorization'] = client.users.client.session.headers['Authorization'] = _get_client_auth_header(organization, client_secret)
    return client


@cached(1, 3600 * 23)
@returns(unicode)
@arguments(organization=unicode, client_secret=unicode)
def _get_client_auth_header(organization, client_secret):
    # Cache the auth header for 23 hours (token is valid 24h)
    plugin = get_iyo_plugin()
    url = plugin.oauth_base_url + '/access_token'
    params = {'grant_type': 'client_credentials',
              'client_id': organization,
              'client_secret': client_secret}
    request = requests.post(url, params=params)
    request.raise_for_status()
    token = request.json()['access_token']
    return 'token {token}'.format(token=token)


def get_itsyouonline_client_from_username(username):
    session = get_current_session()
    if not session:
        session = Session.list_active_user(username).get()
    jwt = session and session.jwt
    client = get_itsyouonline_client_from_jwt(jwt)
    return client


def get_itsyouonline_client_from_jwt(jwt):
    plugin = get_iyo_plugin()
    client = itsyouonline.Client(base_uri=plugin.api_uri)
    client.organizations.client.session.headers['Authorization'] = client.users.client.session.headers['Authorization'] = 'bearer {jwt}'.format(jwt=jwt)
    return client


def get_access_response(config, state, code, use_jwt=None, audience=None, redirect_uri=None):
    params = {
        'client_id': config.root_organization.name,
        'client_secret': config.root_organization[SOURCE_WEB].client_secret,
        'code': code,
        'redirect_uri': get_redirect_uri(config, SOURCE_WEB, redirect_uri),
        'state': state
    }
    if use_jwt:
        params['response_type'] = 'id_token'
        params['scope'] = 'offline_access'
        params['aud'] = audience
    access_token_url = '%s/access_token?%s' % (get_auth_plugin().oauth_base_url, urllib.urlencode(params))
    response = requests.post(access_token_url, params, timeout=55)

    if use_jwt:
        content = response.content
    else:
        content = response.json() if response.status_code == httplib.OK else response.content
    logging.debug('access_response: code %d, content %s', response.status_code, content)
    if response.status_code != httplib.OK:
        exception = HttpException()
        exception.http_code = response.status_code
        exception.error = content
        raise exception
    return content


def get_redirect_uri(config, source, redirect_uri=None):
    redirect_uri = redirect_uri or config.root_organization[source].redirect_uri
    parsed_redirect_uri = urlparse(redirect_uri)
    if 'http' in parsed_redirect_uri.scheme:
        parsed_current_base = urlparse(get_base_url())
        current_netloc = parsed_current_base.netloc.split(':')[0]
        # Support logging in from {version name}-dot-{application id}.appspot.com
        default_hostname = get_default_version_hostname()
        if current_netloc.endswith('.appspot.com') and current_netloc != default_hostname:
            new_redirect_uri = parsed_redirect_uri._replace(netloc=current_netloc).geturl()
            logging.debug('Patched redirect_uri from %s to %s\ndefault_version_hostname: %s\nparsed_current_base: %s',
                          redirect_uri, new_redirect_uri, default_hostname, parsed_current_base)
            redirect_uri = new_redirect_uri

    return redirect_uri


def create_jwt(access_token, scope, add_grants=True):
    params = {
        'scope': scope,
        'add_grants': 'true' if add_grants else 'false'
    }
    url = '%s/jwt?%s' % (get_auth_plugin().oauth_base_url, urlencode(params))
    headers = {
        'Authorization': 'token {token}'.format(token=access_token)
    }
    data = urlfetch.fetch(url, headers=headers)
    if data.status_code == 200:
        return data.content

    msg = 'Failed to create JWT\n{}: {}'.format(data.status_code, data.content)
    logging.debug(msg)
    if DEBUG:
        logging.debug(access_token)
    raise Exception(msg)


def refresh_jwt(old_jwt, validity=24 * 60 * 60, add_grants=True):
    args = {
        'validity': validity,
        'add_grants': 'true' if add_grants else 'false'
    }
    url = '%s/jwt/refresh?%s' % (get_auth_plugin().oauth_base_url, urlencode(args))
    headers = {
        'Authorization': 'bearer {jwt}'.format(jwt=old_jwt)
    }
    data = urlfetch.fetch(url, headers=headers)
    if data.status_code == 200:
        return data.content
    logging.debug('Failed to refresh JWT\n%s: %s', data.status_code, data.content)
    if DEBUG:
        logging.debug(old_jwt)
    raise HttpUnAuthorizedException(data={'login_url': get_base_url() + get_auth_plugin().get_login_url()})


def has_access_to_organization(client, organization_id, username):
    assert isinstance(client, itsyouonline.Client)
    r = client.organizations.UserIsMember(convert_to_str(username), organization_id).json()
    return r['IsMember']


def get_user_scopes_from_access_token(code, state_model):
    config = get_config(NAMESPACE)
    assert isinstance(config, ItsYouOnlineConfiguration)

    access_result = get_access_response(config, state_model.state, code)

    username = access_result['info']['username']
    scope = access_result.get('scope')

    if state_model.organization_id == config.root_organization.name:
        if state_model.source == "app":
            logging.debug('Invalid login source')
            raise HttpForbiddenException()
        else:
            users_organization = state_model.organization_id
    else:
        users_organization = get_users_organization(config, state_model.organization_id)

    admins_organization = get_organization(config.root_organization.name, state_model.organization_id)
    expected_scope = 'user:memberof:%s' % users_organization
    if not scope or expected_scope not in scope:
        logging.debug('Missing or invalid scope.Expected: {} - Received: {}'.format(expected_scope, scope))
        raise HttpForbiddenException()

    save_profile_state(state_model, username)

    client = get_itsyouonline_client()
    scopes = [Scopes.get_organization_scope(Scopes.ORGANIZATION_MEMBER, state_model.organization_id)]
    if has_access_to_organization(client, config.root_organization.name, username):
        scopes.append(Scopes.ADMIN)
    if has_access_to_organization(client, admins_organization, username):
        scopes.append(Scopes.get_organization_scope(Scopes.ORGANIZATION_ADMIN, state_model.organization_id))
    elif not has_access_to_organization(client, users_organization, username):
        # Should never happen as the memberof scope requires this
        logging.debug('User is not a member of organization {}'.format(users_organization))
        raise HttpForbiddenException()
    return username, scopes


def save_profile_state(state_model, username):
    profile = get_or_create_profile(username)
    profile.organization_id = state_model.organization_id
    state_model.completed = True
    ndb.put_multi([profile, state_model])


def get_jwt(code, state_model, redirect_uri=None):
    config = get_config(NAMESPACE)  # type: ItsYouOnlineConfiguration
    json_web_token = get_access_response(config, state_model.state, code, True, audience=config.jwt_audience,
                                         redirect_uri=redirect_uri)
    decoded_jwt = jwt.decode(json_web_token, str(config.iyo_public_key), audience=config.jwt_audience,
                             issuer=JWT_ISSUER)
    if decoded_jwt['azp'] != config.root_organization.name:
        logging.error('Received invalid JWT: %s', decoded_jwt)
        raise HttpForbiddenException()
    username = decoded_jwt['username']
    scopes = decoded_jwt['scope']
    save_profile_state(state_model, username)
    return json_web_token, username, scopes


def decode_jwt_cached(token):
    # memcache key should be shorter than 250 bytes
    """
    Args:
        token (unicode): jwt

    Returns:
        decoded jwt
    Raises:
        ExpiredSignatureError: In case the JWT has expired
    """
    memcache_key = 'jwt-cache-{}'.format(hashlib.sha256(token).hexdigest())
    decoded_jwt = memcache.get(key=memcache_key, namespace=NAMESPACE)  # @UndefinedVariable
    if decoded_jwt:
        return decoded_jwt
    timestamp = now()
    t = time.time()
    config = get_config(NAMESPACE)
    decoded_jwt = jwt.decode(token, str(config.iyo_public_key), audience=config.jwt_audience, issuer=JWT_ISSUER)
    logging.debug('Decoding JWT took %ss', time.time() - t)
    # Cache JWT for as long as it's valid

    memcache.set(key=memcache_key, value=decoded_jwt, time=decoded_jwt['exp'] - timestamp,  # @UndefinedVariable
                 namespace=NAMESPACE)
    return decoded_jwt


def validate_session(session, force_refresh=False):
    """
    Args:
        session (framework.models.session.Session)
        force_refresh (bool)

    Returns:
        bool: True if the session is valid
    """
    if session.jwt:
        try:
            logging.info('Validating JWT %s', session.jwt)
            jwt = decode_jwt_cached(session.jwt)
            # This function is executed every 12 hours and JWT's are only valid for 24h
            if jwt['exp'] > now() + 3600 * 12 and not force_refresh:
                logging.debug('JWT is fine %s', jwt)
                return True
        except ExpiredSignatureError:
            pass
        logging.debug('Refreshing JWT for session %s', session)
        try:
            new_jwt = refresh_jwt(session.jwt)
            session.jwt = new_jwt
            decoded_jwt = decode_jwt_cached(new_jwt)
            session.timeout = decoded_jwt['exp']
            session.scopes = decoded_jwt['scope']
            session.put()
            return True
        except HttpUnAuthorizedException as e:
            logging.warn(e.message, exc_info=True)
            # This probably happens because the JWT did not contain a refresh_token.
            logging.debug('Error while refreshing JWT', exc_info=True)
            session.key.delete()
            return False
