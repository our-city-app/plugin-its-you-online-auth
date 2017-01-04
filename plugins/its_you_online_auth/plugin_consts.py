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

NAMESPACE = 'its_you_online_auth'
ITS_YOU_ONLINE_DOMAIN = 'itsyou.online'
OAUTH_BASE_URL = 'https://itsyou.online/v1/oauth'


class Scopes(object):
    ADMIN = 'admin'
    ORGANIZATION_MEMBER = 'memberof:{organization}'
    ORGANIZATION_ADMIN = 'memberof:{organization}:admin'

    @classmethod
    def get_organization_scope(cls, scope, organization):
        return scope.replace('{organization}', organization)
