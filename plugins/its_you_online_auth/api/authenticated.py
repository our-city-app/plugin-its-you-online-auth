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

from mcfw.exceptions import HttpNotFoundException, HttpConflictException
from mcfw.restapi import rest
from mcfw.rpc import arguments, returns
from plugins.its_you_online_auth.bizz.settings import get_organizations, get_organization, create_organization, \
    update_organization, delete_organization
from plugins.its_you_online_auth.exceptions.organizations import OrganizationNotFoundException, \
    OrganizationAlreadyExistsException
from plugins.its_you_online_auth.plugin_consts import Scopes
from plugins.its_you_online_auth.to.organizations import OrganizationTO


@rest('/organizations', 'get', [Scopes.ADMIN])
@returns([OrganizationTO])
@arguments()
def api_get_organizations():
    try:
        return [OrganizationTO.from_model(o) for o in get_organizations()]
    except OrganizationNotFoundException as e:
        raise HttpNotFoundException(e.message)


@rest('/organizations', 'post', [Scopes.ADMIN])
@returns(OrganizationTO)
@arguments(data=OrganizationTO)
def api_create_organization(data):
    try:
        organization = create_organization(data.id, data.name, data.auto_connected_services, data.roles, data.modules)
        return OrganizationTO.from_model(organization)
    except OrganizationAlreadyExistsException as e:
        raise HttpConflictException(e.message)


@rest('/organizations/<organization_id:[^/]+>', 'get', [Scopes.ADMIN, Scopes.ORGANIZATION_ADMIN])
@returns(OrganizationTO)
@arguments(organization_id=unicode)
def api_get_organization(organization_id):
    try:
        return OrganizationTO.from_model(get_organization(organization_id))
    except OrganizationNotFoundException as e:
        raise HttpNotFoundException(e.message)


@rest('/organizations/<organization_id:[^/]+>', 'put', [Scopes.ADMIN, Scopes.ORGANIZATION_ADMIN])
@returns(OrganizationTO)
@arguments(organization_id=unicode, data=OrganizationTO)
def api_update_organization(organization_id, data):
    try:
        organization = update_organization(organization_id,
                                           data.name,
                                           data.auto_connected_services,
                                           data.roles,
                                           data.modules)
        return OrganizationTO.from_model(organization)
    except OrganizationNotFoundException as e:
        raise HttpNotFoundException(e.message)


@rest('/organizations/<organization_id:[^/]+>', 'delete', [Scopes.ADMIN])
@returns(OrganizationTO)
@arguments(organization_id=unicode)
def api_delete_organization(organization_id):
    delete_organization(organization_id)
