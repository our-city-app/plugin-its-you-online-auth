# -*- coding: utf-8 -*-
# Copyright 2017 Green IT Globe NV
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

from google.appengine.ext import ndb
from plugins.its_you_online_auth import plugin_consts


class OauthLoginState(ndb.Model):
    timestamp = ndb.IntegerProperty(indexed=False)
    organization_id = ndb.StringProperty(indexed=False)
    source = ndb.StringProperty(indexed=False)
    completed = ndb.BooleanProperty(indexed=False)

    @property
    def state(self):
        return self.key.id().decode('utf8')

    @classmethod
    def create_key(cls, state):
        return ndb.Key(cls, state, namespace=plugin_consts.NAMESPACE)


class Profile(ndb.Model):
    access_token = ndb.StringProperty(indexed=False)  # This can also contain a JWT
    organization_id = ndb.StringProperty()
    app_email = ndb.StringProperty()
    language = ndb.StringProperty(indexed=False)

    @property
    def source(self):
        return self.key.parent().id().decode('utf8')

    @property
    def username(self):
        return self.key.id().decode('utf8')

    @classmethod
    def create_key(cls, source, username):
        parent_key = ndb.Key(cls, source, namespace=plugin_consts.NAMESPACE)
        return ndb.Key(cls, username, parent=parent_key)
