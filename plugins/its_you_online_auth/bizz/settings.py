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

from google.appengine.ext import ndb

from mcfw.rpc import returns, arguments
from plugins.its_you_online_auth.exceptions.organizations import OrganizationAlreadyExistsException, \
    OrganizationNotFoundException
from plugins.its_you_online_auth.models.settings import ItsYouOnlineOrganization, OrganizationRole
from plugins.rogerthat_api.to.friends import RegistrationResultRolesTO


@returns(ndb.Query)
@arguments()
def get_organizations():
    """
    Returns:
        query(ndb.Query)
    """
    return ItsYouOnlineOrganization.query()


@returns(ItsYouOnlineOrganization)
@arguments(organization_id=unicode)
def get_organization(organization_id):
    organization = ItsYouOnlineOrganization.create_key(organization_id).get()
    if not organization:
        raise OrganizationNotFoundException(organization_id)
    return organization


@returns(ItsYouOnlineOrganization)
@arguments(organization_id=unicode, name=unicode, auto_connected_services=[unicode],
           roles=[RegistrationResultRolesTO], modules=[unicode])
def create_organization(organization_id, name, auto_connected_services, roles, modules):
    key = ItsYouOnlineOrganization.create_key(organization_id)
    if key.get():
        raise OrganizationAlreadyExistsException(organization_id)
    organization = ItsYouOnlineOrganization(key=key)
    organization.name = name
    organization.auto_connected_services = auto_connected_services
    organization.roles = [OrganizationRole(service=role.service, identity=role.identity, ids=role.ids)
                          for role in roles]
    organization.modules = modules
    organization.put()
    return organization


@returns(ItsYouOnlineOrganization)
@arguments(organization_id=unicode, name=unicode, auto_connected_services=[unicode],
           roles=[RegistrationResultRolesTO], modules=[unicode])
def update_organization(organization_id, name, auto_connected_services, roles, modules):
    key = ItsYouOnlineOrganization.create_key(organization_id)
    organization = key.get()
    if not organization:
        raise OrganizationNotFoundException(organization_id)
    organization.name = name
    organization.auto_connected_services = auto_connected_services
    organization.roles = [OrganizationRole(service=role.service, identity=role.identity, ids=role.ids)
                          for role in roles]
    organization.modules = modules
    organization.put()
    return organization


@returns()
@arguments(organization_id=unicode)
def delete_organization(organization_id):
    key = ItsYouOnlineOrganization.create_key(organization_id)
    key.delete()
