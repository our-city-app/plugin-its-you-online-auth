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

import json
import logging

from google.appengine.ext import ndb
from mcfw.rpc import serialize_complex_value, parse_complex_value
from plugin_loader import get_config
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.exceptions.organizations import OrganizationNotFoundException
from plugins.its_you_online_auth.models import Profile, OauthLoginState
from plugins.its_you_online_auth.plugin_utils import get_sub_organization
from plugins.rogerthat_api.to.friends import RegistrationResultTO, ACCEPT_ID, DECLINE_ID, REGISTRATION_ORIGIN_OAUTH, \
    RegistrationResultRolesTO
from plugins.its_you_online_auth.plugin_consts import NAMESPACE


def friend_register(rt_settings, id_, service_identity, user_details, origin, data, **kwargs):
    try:
        if not data:
            raise Exception("data was null")
        if not origin:
            raise Exception("origin was null")
        if origin != REGISTRATION_ORIGIN_OAUTH:
            raise Exception("unknown origin %s" % origin)

        data = json.loads(data)
        access_token = data.get("result", {}).get("access_token")
        username = data.get("result", {}).get("info", {}).get("username")
        if not access_token or not username:
            return DECLINE_ID

        state = data.get("state")
        login_state = OauthLoginState.create_key(state).get() if state else None
        if not login_state:
            return DECLINE_ID

        scope = data.get("result", {}).get("scope")
        config = get_config(NAMESPACE)
        expected_scope = "user:memberof:%s" % get_sub_organization(config, login_state.organization_id)
        if not scope or scope != expected_scope:
            return DECLINE_ID

        profile_key = Profile.create_key(login_state.source, username)
        profile = profile_key.get() or Profile(key=profile_key)
        profile.access_token = access_token
        profile.organization_id = login_state.organization_id
        profile.app_email = u"%s:%s" % (user_details[0]['email'], user_details[0]['app_id'])
        login_state.completed = True
        ndb.put_multi([profile, login_state])

        r = RegistrationResultTO()
        r.result = ACCEPT_ID
        r.auto_connected_services = []
        r.roles = []
        try:
            organization = get_organization(login_state.organization_id)
            r.auto_connected_services = organization.auto_connected_services
            if organization.roles:
                r.roles = parse_complex_value(RegistrationResultRolesTO, json.loads(organization.roles), True)
        except OrganizationNotFoundException:
            pass

        return serialize_complex_value(r, RegistrationResultTO, False)
    except:
        logging.warn('friend_register failed', exc_info=True)
        return DECLINE_ID


def friend_register_result(rt_settings, id_, service_identity, user_details, origin, **kwargs):
    pass