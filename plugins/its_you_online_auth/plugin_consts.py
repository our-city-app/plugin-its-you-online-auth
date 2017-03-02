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
from plugins.its_you_online_auth.libs.itsyouonline import BASE_URI

NAMESPACE = 'its_you_online_auth'
OAUTH_BASE_URL = '{}v1/oauth'.format(BASE_URI)
ITS_YOU_ONLINE_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAES5X8XrfKdx9gYayFITc89wad4usrk0n2
7MjiGYvqalizeSWTHEpnd7oea9IQ8T5oJjMVH5cc0H5tFSKilFFeh//wngxIyny6
6+Vq5t5B0V0Ehy01+2ceEon2Y0XDkIKv
-----END PUBLIC KEY-----"""
JWT_AUDIENCE = 'rogerthat-control-center'
JWT_ISSUER = 'itsyouonline'

SOURCE_DEV = 'dev'
SOURCE_WEB = 'web'
SOURCE_APP = 'app'


class Scopes(object):
    ADMIN = u'admin'
    ORGANIZATION_MEMBER = u'memberof:{organization_id}'
    ORGANIZATION_ADMIN = u'memberof:{organization_id}:admin'

    @classmethod
    def get_organization_scope(cls, scope, organization_id):
        return scope.replace('{organization_id}', organization_id)
