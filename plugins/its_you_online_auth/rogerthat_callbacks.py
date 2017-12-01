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

import json
import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from framework.plugin_loader import get_config
from mcfw.rpc import serialize_complex_value
from plugins.its_you_online_auth.bizz.authentication import decode_jwt_cached, get_itsyouonline_client
from plugins.its_you_online_auth.bizz.profile import get_or_create_profile, set_user_information, store_user_information
from plugins.its_you_online_auth.bizz.settings import get_organization
from plugins.its_you_online_auth.exceptions.organizations import OrganizationNotFoundException
from plugins.its_you_online_auth.models import OauthState, Profile
from plugins.its_you_online_auth.plugin_consts import NAMESPACE
from plugins.its_you_online_auth.plugin_utils import get_users_organization
from plugins.rogerthat_api.to.friends import RegistrationResultTO, ACCEPT_ID, DECLINE_ID, REGISTRATION_ORIGIN_OAUTH, \
    RegistrationResultRolesTO, REGISTRATION_ORIGIN_QR, RegistrationUserInfoTO


def friend_register(rt_settings, id_, service_identity, user_details, origin, data, **kwargs):
    try:
        if origin == REGISTRATION_ORIGIN_QR:
            return _friend_register_qr(rt_settings, id_, service_identity, user_details, origin, data, **kwargs)
        elif origin == REGISTRATION_ORIGIN_OAUTH:
            return _friend_register_oauth(rt_settings, id_, service_identity, user_details, origin, data, **kwargs)

    except:
        logging.warn('friend_register failed', exc_info=True)

    return DECLINE_ID


def friend_register_result(rt_settings, id_, service_identity, user_details, origin, **kwargs):
    pass


def _friend_register_qr(rt_settings, id_, service_identity, user_details, origin, data, **kwargs):
    if not data:
        raise Exception('data was null')

    data = json.loads(data)
    qr_type = data.get('qr_type', None)
    qr_content = data.get('qr_content', None)
    if not qr_type or not qr_content:
        logging.warn('Could not find qr_type or qr_content, denying installation.')
        return DECLINE_ID

    if qr_type != 'jwt':
        return DECLINE_ID

    decoded_jwt = decode_jwt_cached(qr_content)
    username = decoded_jwt.get('username', None)
    if not username:
        logging.warn('Could not find username in jwt denying installation.')
        return DECLINE_ID

    profile = get_or_create_profile(username, u'%s:%s' % (user_details[0]['email'], user_details[0]['app_id']))
    profile.put()

    result = RegistrationResultTO(result=ACCEPT_ID, auto_connected_services=[], roles=[],
                                  user_details=RegistrationUserInfoTO(name=None, avatar=None))

    if get_config(NAMESPACE).fetch_information:
        deferred.defer(set_user_information, Profile.create_key(username))
    return serialize_complex_value(result, RegistrationResultTO, False)


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
    client.api.session.headers['Authorization'] = 'token %s' % access_token
    user_info = client.api.users.GetUserInformation(username).json()
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
