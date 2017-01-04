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

from mcfw.rpc import returns, arguments
from plugins.its_you_online_auth.exceptions.organizations import OrganizationAlreadyExistsException, \
    OrganizationNotFoundException
from plugins.its_you_online_auth.models.settings import ItsYouOnlineOrganization, OrganizationRole
from plugins.rogerthat_api.to.friends import RegistrationResultRolesTO


def get_organizations():
    return ItsYouOnlineOrganization.query()


@returns(ItsYouOnlineOrganization)
@arguments(client_id=unicode)
def get_organization(client_id):
    organization = ItsYouOnlineOrganization.create_key(client_id).get()
    if not organization:
        raise OrganizationNotFoundException(client_id)
    return organization


@returns(ItsYouOnlineOrganization)
@arguments(client_id=unicode, name=unicode, auto_connected_services=[unicode], roles=[RegistrationResultRolesTO])
def create_organization(client_id, name, auto_connected_services, roles):
    key = ItsYouOnlineOrganization.create_key(client_id)
    if key.get():
        raise OrganizationAlreadyExistsException(client_id)
    organization = ItsYouOnlineOrganization(key=key)
    organization.name = name
    organization.auto_connected_services = auto_connected_services
    organization.roles = [OrganizationRole(service=role.service, identity=role.identity, ids=role.ids) for role in roles]
    organization.put()
    return organization


@returns(ItsYouOnlineOrganization)
@arguments(client_id=unicode, name=unicode, auto_connected_services=[unicode], roles=[RegistrationResultRolesTO])
def update_organization(client_id, name, auto_connected_services, roles):
    key = ItsYouOnlineOrganization.create_key(client_id)
    organization = key.get()
    if not organization:
        raise OrganizationNotFoundException(client_id)
    organization.name = name
    organization.auto_connected_services = auto_connected_services
    organization.roles = [OrganizationRole(service=role.service, identity=role.identity, ids=role.ids) for role in roles]
    organization.put()
    return organization


@returns()
@arguments(client_id=unicode)
def delete_organization(client_id):
    key = ItsYouOnlineOrganization.create_key(client_id)
    key.delete()
