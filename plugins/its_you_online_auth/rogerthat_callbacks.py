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

import json
import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from framework.plugin_loader import get_config
from mcfw.rpc import serialize_complex_value
from plugins.its_you_online_auth.bizz.authentication import get_itsyouonline_client
from plugins.its_you_online_auth.bizz.profile import get_or_create_profile, store_user_information
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.exceptions.organizations import OrganizationNotFoundException
from plugins.its_you_online_auth.models import OauthState
from plugins.its_you_online_auth.plugin_consts import NAMESPACE
from plugins.its_you_online_auth.plugin_utils import get_users_organization
from plugins.rogerthat_api.to.friends import RegistrationResultTO, ACCEPT_ID, DECLINE_ID, REGISTRATION_ORIGIN_OAUTH, \
    RegistrationResultRolesTO, RegistrationUserInfoTO


def friend_register(rt_settings, id_, service_identity, user_details, origin, data, **kwargs):
    try:
        if origin == REGISTRATION_ORIGIN_OAUTH:
            return _friend_register_oauth(rt_settings, id_, service_identity, user_details, origin, data, **kwargs)

    except:
        logging.warn('friend_register failed', exc_info=True)

    return DECLINE_ID


def _friend_register_oauth(rt_settings, id_, service_identity, user_details, origin, data, **kwargs):
    if not data:
        raise Exception('data was null')

    data = json.loads(data)
    access_token = data.get('result', {}).get('access_token')
    username = data.get('result', {}).get('info', {}).get('username')
    if not access_token or not username:
        logging.warn('Could not find access token or username, denying installation.\nAccess token: %s\n',
                     access_token)
        return DECLINE_ID

    state = data.get('state')
    login_state = OauthState.create_key(state).get() if state else None
    if not login_state:
        logging.warn('Could not find login state, denying installation.')
        return DECLINE_ID

    config = get_config(NAMESPACE)
    if config.require_memberof:
        scope = data.get('result', {}).get('scope')
        expected_scope = 'user:memberof:%s' % get_users_organization(config, login_state.organization_id)
        if not scope or expected_scope not in scope:
            logging.warn('Could not find expected organization scope %s in scope %s. Denying installation.',
                         expected_scope, scope)
            return DECLINE_ID

    profile = get_or_create_profile(username, u'%s:%s' % (user_details[0]['email'], user_details[0]['app_id']))
    profile.organization_id = login_state.organization_id
    login_state.completed = True
    ndb.put_multi([profile, login_state])

    client = get_itsyouonline_client()
    client.users.client.session.headers['Authorization'] = client.organizations.client.session.headers['Authorization'] = 'token %s' % access_token
    user_info = client.users.GetUserInformation(username).json()
    if user_info['firstname'] and user_info['lastname']:
        name = '%s %s' % (user_info['firstname'], user_info['lastname'])
    else:
        name = username
    result = RegistrationResultTO(result=ACCEPT_ID, auto_connected_services=[], roles=[],
                                  user_details=RegistrationUserInfoTO(name=name, avatar=None))

    if login_state.organization_id:
        try:
            organization = get_organization(login_state.organization_id)
            result.auto_connected_services = organization.auto_connected_services
            if organization.roles:
                for role in organization.roles:
                    roleTO = RegistrationResultRolesTO()
                    roleTO.service = role.service
                    roleTO.identity = role.identity
                    roleTO.ids = role.ids
                    result.roles.append(roleTO)
        except OrganizationNotFoundException:
            pass

    if config.fetch_information:
        deferred.defer(store_user_information, user_info)
    return serialize_complex_value(result, RegistrationResultTO, False)
