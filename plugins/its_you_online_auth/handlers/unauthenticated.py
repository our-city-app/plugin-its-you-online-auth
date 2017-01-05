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
import os
import urllib
import uuid

from auth import login_user, logout_user, get_current_user_id
from google.appengine.ext.webapp import template
from handlers import render_error_page
from mcfw.exceptions import HttpException
from plugin_loader import get_config
from plugins.its_you_online_auth.bizz.authentication import get_user_scopes
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.exceptions.organizations import OrganizationNotFoundException
from plugins.its_you_online_auth.models import OauthLoginState
from plugins.its_you_online_auth.plugin_consts import OAUTH_BASE_URL, NAMESPACE, SOURCE_WEB, SOURCE_APP
from plugins.its_you_online_auth.plugin_utils import get_sub_organization
from utils import now
import webapp2


class SigninHandler(webapp2.RequestHandler):
    def get(self):
        user_id = get_current_user_id()
        if user_id:
            self.redirect('/')
            return

        path = os.path.join(os.path.dirname(__file__), 'templates', 'signin.html')
        with open(path, 'r') as f:
            self.response.out.write(f.read())


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        user_id = get_current_user_id()
        if user_id:
            logout_user(self.response)
        self.redirect('/')


class AppLoginHandler(webapp2.RequestHandler):
    def get(self):
        params = dict()
        params['source'] = 'app'
        self.redirect('/login/organization?%s' % urllib.urlencode(params))


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
                params = dict()
                params['source'] = source
                params['organization_id'] = organization_id
                self.redirect('/login/redirect?%s' % urllib.urlencode(params))
                return

        path = os.path.join(os.path.dirname(__file__), 'templates', 'organization.html')

        context = dict(source=self.request.GET.get('source', SOURCE_WEB),
                       error=error)
        self.response.out.write(template.render(path, context))


class DoLoginHandler(webapp2.RequestHandler):
    def get(self):
        organization_id = self.request.GET.get('organization_id', None)
        source = self.request.GET.get('source', SOURCE_WEB)

        if not organization_id:
            self.redirect('/login/organization')
            return

        config = get_config(NAMESPACE)
        if organization_id != config.root_organization.name:
            try:
                get_organization(organization_id)
            except OrganizationNotFoundException as e:
                render_error_page(self.response, httplib.BAD_REQUEST, e.message)
                return

        if source not in [SOURCE_WEB, SOURCE_APP]:
            render_error_page(self.response, httplib.BAD_REQUEST, 'Bad Request')
            return

        if organization_id == config.root_organization.name:
            if source == SOURCE_APP:
                render_error_page(self.response, httplib.BAD_REQUEST, 'Bad Request')
                return
            else:
                sub_org = organization_id
        else:
            sub_org = get_sub_organization(config, organization_id)

        params = {
            'response_type': 'code',
            'client_id': config.root_organization.name,
            'redirect_uri': config.root_organization[source].redirect_uri,
            'scope': 'user:memberof:%s' % sub_org,
            'state': str(uuid.uuid4())
        }

        login_state = OauthLoginState(key=OauthLoginState.create_key(params['state']))
        login_state.timestamp = now()
        login_state.organization_id = organization_id
        login_state.source = source
        login_state.completed = False
        login_state.put()

        oauth_url = '%s/authorize?%s' % (OAUTH_BASE_URL, urllib.urlencode(params))
        self.redirect(oauth_url)


class Oauth2CallbackHandler(webapp2.RequestHandler):
    def get(self):
        # should only be used by source web
        code = self.request.GET.get('code', None)
        state = self.request.GET.get('state', None)
        try:
            username, scopes = get_user_scopes(code, state)
        except HttpException as e:
            render_error_page(self.response, e.http_code, e.error)
            return

        login_user(self.response, username, scopes)
        self.redirect('/')
