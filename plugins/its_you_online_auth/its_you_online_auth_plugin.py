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

import logging

from auth import get_current_session
from mcfw.consts import AUTHENTICATED
from mcfw.restapi import rest_functions
from plugin_loader import AuthPlugin, get_plugins, get_config
from plugin_loader import get_plugin
from plugins.its_you_online_auth.api import authenticated
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.handlers.unauthenticated import SigninHandler, LogoutHandler, AppLoginHandler, \
    PickOrganizationHandler, DoLoginHandler, Oauth2CallbackHandler
from plugins.its_you_online_auth.models import Profile
from plugins.its_you_online_auth.plugin_consts import Scopes, NAMESPACE, SOURCE_WEB
from plugins.its_you_online_auth.rogerthat_callbacks import friend_register, friend_register_result
from plugins.its_you_online_auth.to import ItsYouOnlineConfiguration
from plugins.rogerthat_api.rogerthat_api_plugin import RogerthatApiPlugin
import requests_toolbelt.adapters.appengine
from utils import Handler, Module


requests_toolbelt.adapters.appengine.monkeypatch()


class ItsYouOnlineAuthPlugin(AuthPlugin):
    def __init__(self, configuration):
        super(ItsYouOnlineAuthPlugin, self).__init__(configuration)
        self.configuration = ItsYouOnlineConfiguration(configuration)
        rogerthat_api_plugin = get_plugin('rogerthat_api')
        assert (isinstance(rogerthat_api_plugin, RogerthatApiPlugin))
        rogerthat_api_plugin.subscribe('friend.register', friend_register)
        rogerthat_api_plugin.subscribe('friend.register_result', friend_register_result)

    def get_handlers(self, auth):
        if auth == Handler.AUTH_UNAUTHENTICATED:
            yield Handler(url='/login', handler=SigninHandler)
            yield Handler(url='/logout', handler=LogoutHandler)
            yield Handler(url='/login/app', handler=AppLoginHandler)
            yield Handler(url='/login/organization', handler=PickOrganizationHandler)
            yield Handler(url='/login/redirect', handler=DoLoginHandler)
            yield Handler(url='/oauth2_callback', handler=Oauth2CallbackHandler)
            for url, handler in rest_functions(authenticated, authentication=AUTHENTICATED):
                yield Handler(url=url, handler=handler)

    def get_modules(self):
        # TODO: create an admin page organization admins
        # yield Module(name="its_you_online_settings", scopes=[Scopes.ORGANIZATION_ADMIN])
        yield Module(name="its_you_online_settings", scopes=[Scopes.ADMIN])

    def get_login_url(self):
        return self.configuration.login_url

    def get_cookie_name(self):
        return self.configuration.cookie_name

    def get_cookie_key(self):
        return self.configuration.cookie_key

    def get_visible_modules(self):
        session = get_current_session()
        user_id = session.user_id
        scopes = session.scopes

        profile = Profile.create_key(SOURCE_WEB, user_id).get()
        if not profile:
            return []

        organization_id = profile.organization_id
        logging.debug("get_visible_modules\n- organization_id: %s\n- user_id: %s\n- scopes: %s", organization_id, user_id, scopes)
        if not organization_id:
            return []

        config = get_config(NAMESPACE)
        if organization_id == config.root_organization.name:
            return ['its_you_online_settings']

        try:
            organization = get_organization(organization_id)
            visible_modules = set()
            for p in get_plugins():
                for m in p.get_modules():
                    if m.name not in organization.modules:
                        continue

                    if m.scopes and not any([True if Scopes.get_organization_scope(scope, organization_id) in scopes else False for scope in m.scopes]):
                        continue

                    visible_modules.add(m.name)

            return list(visible_modules)
        except:
            logging.debug('Failed to get visible modules', exc_info=True)
            return []

