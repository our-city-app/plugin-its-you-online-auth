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

from mcfw.properties import unicode_property, typed_property, unicode_list_property
from plugins.rogerthat_api.to.friends import RegistrationResultRolesTO


class OrganizationTO(object):
    client_id = unicode_property('1')
    name = unicode_property('2')
    auto_connected_services = unicode_list_property('3')
    roles = typed_property('4', RegistrationResultRolesTO, True)

    def __init__(self, client_id=None, name=None, auto_connected_services=None, roles=None):
        if auto_connected_services is None:
            auto_connected_services = []
        if roles is None:
            roles = []
        self.client_id = client_id
        self.name = name
        self.auto_connected_services = auto_connected_services
        self.roles = roles

    @classmethod
    def from_model(cls, organization):
        """
        Args:
            organization (plugins.its_you_online_auth.models.settings.ItsYouOnlineOrganization)
        """
        roles_to = []
        if organization.roles:
            for organization_role in organization.roles:
                to = RegistrationResultRolesTO()
                to.service = organization_role.service
                to.identity = organization_role.identity
                to.ids = organization_role.ids
                roles_to.append(to)

        return cls(organization.client_id, organization.name, organization.auto_connected_services, roles_to)
