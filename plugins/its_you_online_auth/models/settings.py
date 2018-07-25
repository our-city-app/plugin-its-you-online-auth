# -*- coding: utf-8 -*-
# Copyright 2018 Mobicage NV
# NOTICE: THIS FILE HAS BEEN MODIFIED BY MOBICAGE NV IN ACCORDANCE WITH THE APACHE LICENSE VERSION 2.0
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
# @@license_version:1.5@@

from google.appengine.ext import ndb

from plugins.its_you_online_auth import plugin_consts


class OrganizationRole(ndb.Model):
    service = ndb.StringProperty()  # service@example.com
    identity = ndb.StringProperty()  # '+default+'
    ids = ndb.IntegerProperty(repeated=True)  # type: (list of long): role ids


class ItsYouOnlineOrganization(ndb.Model):
    name = ndb.StringProperty()
    scopes = ndb.StringProperty(indexed=False, repeated=True)
    auto_connected_services = ndb.StringProperty(indexed=False, repeated=True)
    roles = ndb.LocalStructuredProperty(OrganizationRole, repeated=True)
    modules = ndb.StringProperty(indexed=False, repeated=True)

    @property
    def organization_id(self):
        return self.key.id().decode('utf8')

    @classmethod
    def create_key(cls, organization_id):
        return ndb.Key(cls, organization_id, namespace=plugin_consts.NAMESPACE)

    @classmethod
    def query(cls, *args, **kwargs):
        kwargs['namespace'] = plugin_consts.NAMESPACE
        return super(ItsYouOnlineOrganization, cls).query(*args, **kwargs)
