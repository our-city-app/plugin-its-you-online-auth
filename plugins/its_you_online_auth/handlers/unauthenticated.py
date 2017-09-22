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

import httplib
import logging
import os
import urllib
import uuid

import webapp2

from framework.bizz.authentication import login_user, logout_user, get_current_user_id, get_current_session
from framework.bizz.session import is_valid_session
from framework.handlers import render_error_page, render_page
from framework.plugin_loader import get_config, get_auth_plugin
from framework.utils import now, get_server_url
from mcfw.consts import MISSING
from mcfw.exceptions import HttpException, HttpBadRequestException, HttpNotFoundException
from plugins.its_you_online_auth.bizz.authentication import get_user_scopes_from_access_token, get_jwt
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.exceptions.organizations import OrganizationNotFoundException
from plugins.its_you_online_auth.models import OauthState
from plugins.its_you_online_auth.plugin_consts import NAMESPACE, SOURCE_WEB, SOURCE_APP
from plugins.its_you_online_auth.plugin_utils import get_users_organization
from plugins.its_you_online_auth.to.config import ItsYouOnlineConfiguration


class SigninHandler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        if is_valid_session(session):
            self.redirect('/')
            return

        config = get_config(NAMESPACE)
        if not config.login_with_organization:
            self.redirect('/login/continue?%s' % self.request.query)
            return
        render_page(self.response, os.path.join('unauthenticated', 'signin.html'), plugin_name=NAMESPACE)


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        user_id = get_current_user_id()
        if user_id:
            logout_user(self.response)
        self.redirect('/')


class AppLoginHandler(webapp2.RequestHandler):
    def get(self):
        params = {
            'source': SOURCE_APP
        }
        config = get_config(NAMESPACE)
        if config.login_with_organization:
            self.redirect('/login/organization?%s' % urllib.urlencode(params))
        else:
            params['organization_id'] = config.root_organization.name
            if config.required_scopes and config.required_scopes is not MISSING:
                # provide extra scopes
                params['scope'] = config.required_scopes
            self.redirect('/login/redirect?%s' % urllib.urlencode(params))


class PickOrganizationHandler(webapp2.RequestHandler):
    def get(self):
        organization_id = self.request.GET.get('organization_id', None)
        source = self.request.GET.get('source', SOURCE_WEB)

        error = None
        if organization_id:
            config = get_config(NAMESPACE)
            if organization_id != config.root_organization.name:
                try:
                    get_organization(organization_id)
                except OrganizationNotFoundException as e:
                    error = e.message

            if not error:
                self.redirect('/login/redirect?%s' % self.request.query)
                return

        template_parameters = {
            'source': source,
            'error': error
        }
        render_page(self.response, os.path.join('unauthenticated', 'organization.html'), plugin_name=NAMESPACE,
                    template_parameters=template_parameters)


class OauthAuthorizeHandler(webapp2.RequestHandler):
    def get(self):
        organization_id = self.request.GET.get('organization_id', None)
        source = self.request.GET.get('source', SOURCE_WEB)
        extra_scopes = self.request.GET.get('scope', '').lstrip(',')
        register = self.request.GET.get('register', False)

        config = get_config(NAMESPACE)
        assert isinstance(config, ItsYouOnlineConfiguration)

        if not organization_id and config.login_with_organization:
            self.redirect('/login/organization')
            return

        if config.login_with_organization:
            if organization_id != config.root_organization.name:
                try:
                    get_organization(organization_id)
                except OrganizationNotFoundException as e:
                    render_error_page(self.response, httplib.BAD_REQUEST, e.message)
                    return

        if source not in [SOURCE_WEB, SOURCE_APP]:
            render_error_page(self.response, httplib.BAD_REQUEST, 'Bad Request')
            return

        if config.login_with_organization:
            if organization_id == config.root_organization.name:
                if source == SOURCE_APP:
                    render_error_page(self.response, httplib.BAD_REQUEST, 'Bad Request')
                    return
                else:
                    sub_org = organization_id
            else:
                sub_org = get_users_organization(config, organization_id)
            scope = 'user:memberof:%s' % sub_org
        elif config.require_memberof:
            scope = 'user:memberof:%s' % config.root_organization.name
        else:
            scope = ''

        if scope:
            scope += ','
        scope += extra_scopes

        params = {
            'response_type': 'code',
            'client_id': config.root_organization.name,
            'redirect_uri': config.root_organization[source].redirect_uri,
            'scope': scope,
            'state': str(uuid.uuid4())
        }

        login_state = OauthState(key=OauthState.create_key(params['state']))
        login_state.timestamp = now()
        login_state.organization_id = organization_id
        login_state.source = source
        login_state.completed = False
        login_state.put()

        if register:
            params['register'] = 1
        oauth_url = '%s/authorize?%s' % (get_auth_plugin().oauth_base_url, urllib.urlencode(params))
        logging.info('Redirecting to %s', oauth_url)
        self.redirect(str(oauth_url))


class DoLoginHandler(OauthAuthorizeHandler):
    def get(self, **kwargs):
        super(DoLoginHandler, self).get()


class Oauth2CallbackHandler(webapp2.RequestHandler):
    def get(self):
        # should only be used by source web
        code = self.request.GET.get('code', None)
        state = self.request.GET.get('state', None)
        try:
            if not (code or state):
                logging.debug('Code or state are missing.\nCode: %s\nState:%s', code, state)
                raise HttpBadRequestException()

            login_state = OauthState.create_key(state).get()
            if not login_state:
                logging.debug('Login state not found')
                raise HttpBadRequestException()

            config = get_config(NAMESPACE)
            assert isinstance(config, ItsYouOnlineConfiguration)
            if config.login_with_organization:
                username, scopes = get_user_scopes_from_access_token(code, login_state)
                jwt = None
            else:
                jwt, username, scopes = get_jwt(code, login_state)
        except HttpException as e:
            render_error_page(self.response, e.http_code, e.error)
            return

        login_user(self.response, username, scopes, jwt)
        self.redirect('/')


class ContinueLoginHandler(webapp2.RequestHandler):
    def get(self, register=False, **kwargs):
        # Redirect to /login/organization if an organization is required to login
        # else immediately redirect to to itsyou.online
        config = get_config(NAMESPACE)  # type: ItsYouOnlineConfiguration
        if config.login_with_organization:
            self.redirect('/login/organization')
        else:
            params = {
                'source': self.request.GET.get('source', SOURCE_WEB),
                'organization_id': config.root_organization.name,
                'scope': self.request.GET.get('scope') or ''
            }
            if register:
                params['register'] = 1
            if config.required_scopes and config.required_scopes is not MISSING:
                # provide extra scopes
                if params['scope']:
                    params['scope'] += ','
                params['scope'] += config.required_scopes
            self.redirect(str('/login/redirect?%s' % urllib.urlencode(params)))


class RegisterHandler(ContinueLoginHandler):
    def get(self, **kwargs):
        super(RegisterHandler, self).get(register=True, **kwargs)


class RefreshHandler(webapp2.RequestHandler):

    def get(self):
        app_redirect_uri = self.request.GET.get('app_redirect_uri', None)

        try:
            if not app_redirect_uri:
                logging.debug('app_redirect_uri is missing')
                raise HttpNotFoundException()

        except HttpException as e:
            render_error_page(self.response, e.http_code, e.error)
            return

        config = get_config(NAMESPACE)  # type: ItsYouOnlineConfiguration
        if config.required_scopes and config.required_scopes is not MISSING:
            scope = config.required_scopes
        else:
            scope = ''

        organization_id = config.root_organization.name

        params = {
            'response_type': 'code',
            'client_id': config.root_organization.name,
            'redirect_uri': '%s/refresh/callback' % get_server_url(),
            'scope': scope,
            'state': str(uuid.uuid4())
        }

        refresh_state = OauthState(key=OauthState.create_key(params['state']))
        refresh_state.timestamp = now()
        refresh_state.organization_id = organization_id
        refresh_state.source = SOURCE_APP
        refresh_state.app_redirect_uri = app_redirect_uri
        refresh_state.completed = False
        refresh_state.put()

        oauth_url = '%s/authorize?%s' % (get_auth_plugin().oauth_base_url, urllib.urlencode(params))
        logging.info('Redirecting to %s', oauth_url)
        self.redirect(oauth_url)


class RefreshCallbackHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.GET.get('code', None)
        state = self.request.GET.get('state', None)
        try:
            if not (code and state):
                logging.debug('Code or state are missing.\nCode: %s\nState:%s', code, state)
                raise HttpBadRequestException()

            refresh_state = OauthState.create_key(state).get()
            if not refresh_state:
                logging.debug('Refresh state not found')
                raise HttpBadRequestException()

        except HttpException as e:
            render_error_page(self.response, e.http_code, e.error)
            return

        try:
            jwt, username, scopes = get_jwt(code, refresh_state, '%s/refresh/callback' % get_server_url())
            login_user(self.response, username, scopes, jwt)
            params = {'success': 'OK'}

        except HttpException as e:
            params = {
                'error': e.error,
                'error_description': 'An error occurred. Please try again.'
            }

        url = '%s?%s' % (refresh_state.app_redirect_uri, urllib.urlencode(params))
        logging.info('Redirecting to %s', url)
        self.redirect(str(url))
