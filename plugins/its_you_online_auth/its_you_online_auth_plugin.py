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

from __future__ import unicode_literals

import logging

import requests_toolbelt.adapters.appengine

from framework.bizz.authentication import get_current_session
from framework.bizz.session import is_valid_session
from framework.configuration import get_configuration
from framework.plugin_loader import AuthPlugin, get_auth_plugin, get_plugin, get_plugins, get_config
from framework.utils.plugins import Handler, Module
from mcfw.consts import AUTHENTICATED, MISSING
from mcfw.restapi import rest_functions
from mcfw.rpc import parse_complex_value
from plugins.its_you_online_auth.api import authenticated
from plugins.its_you_online_auth.bizz.authentication import validate_session
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.cron.refresh_jwts import RefreshJwtsHandler
from plugins.its_you_online_auth.handlers.unauthenticated import SigninHandler, LogoutHandler, AppLoginHandler, \
    PickOrganizationHandler, DoLoginHandler, Oauth2CallbackHandler, ContinueLoginHandler, RegisterHandler,\
    RefreshHandler, RefreshCallbackHandler
from plugins.its_you_online_auth.libs import itsyouonline
from plugins.its_you_online_auth.models import Profile
from plugins.its_you_online_auth.plugin_consts import Scopes, NAMESPACE, SOURCE_WEB
from plugins.its_you_online_auth.rogerthat_callbacks import friend_register, friend_register_result
from plugins.its_you_online_auth.to.config import ItsYouOnlineConfiguration
from plugins.rogerthat_api.rogerthat_api_plugin import RogerthatApiPlugin


requests_toolbelt.adapters.appengine.monkeypatch()


class ItsYouOnlineAuthPlugin(AuthPlugin):
    def __init__(self, configuration):
        super(ItsYouOnlineAuthPlugin, self).__init__(configuration)
        self.configuration = parse_complex_value(ItsYouOnlineConfiguration, configuration,
                                                 False)  # type: ItsYouOnlineConfiguration
        if self.configuration.api_domain is MISSING:
            self.configuration.api_domain = u'itsyou.online'
        rogerthat_api_plugin = get_plugin('rogerthat_api')
        assert isinstance(rogerthat_api_plugin, RogerthatApiPlugin)
        rogerthat_api_plugin.subscribe('friend.register', friend_register)
        rogerthat_api_plugin.subscribe('friend.register_result', friend_register_result)
        itsyouonline.BASE_URI = u'https://%s/' % self.configuration.api_domain

    def get_handlers(self, auth):
        if auth == Handler.AUTH_UNAUTHENTICATED:
            yield Handler(url='/login', handler=SigninHandler)
            yield Handler(url='/logout', handler=LogoutHandler)
            yield Handler(url='/login/app', handler=AppLoginHandler)
            yield Handler(url='/login/continue', handler=ContinueLoginHandler)
            yield Handler(url='/login/organization', handler=PickOrganizationHandler)
            yield Handler(url='/login/redirect', handler=DoLoginHandler)
            yield Handler(url='/register', handler=RegisterHandler)
            yield Handler(url='/oauth2_callback', handler=Oauth2CallbackHandler)
            yield Handler(url='/refresh', handler=RefreshHandler)
            yield Handler(url='/refresh/callback', handler=RefreshCallbackHandler)
            for url, handler in rest_functions(authenticated, authentication=AUTHENTICATED):
                yield Handler(url=url, handler=handler)
        elif auth == Handler.AUTH_ADMIN:
            yield Handler(url='/admin/cron/its_you_online_auth/refresh_jwts', handler=RefreshJwtsHandler)

    def get_client_routes(self):
        return ['/itsyouonlinesettings<route:.*>']

    def get_modules(self):
        yield Module('its_you_online_settings', [Scopes.ADMIN, Scopes.ORGANIZATION_ADMIN], 10000)

    def get_login_url(self):
        return self.configuration.login_url

    def get_logout_url(self):
        server_url = get_configuration().server_url
        if not server_url or server_url is MISSING:
            server_url = ''
            logging.debug('Using default logout url')
        return '%s/logout' % server_url

    def get_profile_url(self):
        return itsyouonline.BASE_URI

    def get_cookie_name(self):
        return self.configuration.cookie_name

    def get_cookie_key(self):
        return self.configuration.cookie_key.encode('utf-8')

    def get_visible_modules(self):
        session = get_current_session()
        user_id = session.user_id
        scopes = session.scopes

        profile = Profile.create_key(SOURCE_WEB, user_id).get()
        if not profile:
            return []

        visible_modules = set()
        config = get_config(NAMESPACE)
        try:
            if config.login_with_organization:
                organization_id = profile.organization_id
                if not organization_id:
                    return []

                if organization_id == config.root_organization.name:
                    return [u'its_you_online_settings']
                organization = get_organization(organization_id)
                for plugin in get_plugins():
                    for module in plugin.get_modules():
                        if config.login_with_organization and module.name not in organization.modules:
                            continue
                        module_scopes = []
                        for scope in module.scopes:
                            if Scopes.get_organization_scope(scope, organization_id) in scopes:
                                module_scopes.append(True)
                            else:
                                module_scopes.append(False)

                        if module.scopes and not any(module_scopes):
                            continue
                        visible_modules.add(module)
            else:
                auth_plugin = get_auth_plugin()
                for plugin in get_plugins():
                    if plugin != auth_plugin:
                        for module in plugin.get_modules():
                            visible_modules.add(module)
            return map(lambda m: m.name, sorted(visible_modules, key=lambda m: m.sort_order))

        except:
            logging.debug('Failed to get visible modules', exc_info=True)
            return []

    def set_user_language(self, language):
        session = get_current_session()
        profile = Profile.create_key(SOURCE_WEB, session.user_id).get()
        profile.language = language
        profile.put()

    def get_user_language(self):
        session = get_current_session()
        if not is_valid_session(session):
            return None
        return Profile.create_key(SOURCE_WEB, session.user_id).get().language

    def validate_session(self, session):
        """
        Args:
            session (framework.models.session.Session)
        """
        return validate_session(session)
