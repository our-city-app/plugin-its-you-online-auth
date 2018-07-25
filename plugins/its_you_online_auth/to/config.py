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

from mcfw.consts import DEBUG
from mcfw.properties import unicode_property, typed_property, bool_property

from plugins.its_you_online_auth.plugin_consts import SOURCE_WEB, SOURCE_APP


class OauthConfig(object):
    client_secret = unicode_property('client_secret')
    redirect_uri = unicode_property('redirect_uri')


class RootOrganization(object):
    name = unicode_property('name')
    dev = typed_property('dev', OauthConfig)
    web = typed_property('web', OauthConfig)
    app = typed_property('app', OauthConfig)

    def __getitem__(self, key):
        if isinstance(key, (str, unicode)):
            if key == SOURCE_WEB:
                return self.dev if DEBUG else self.web
            if key == SOURCE_APP:
                return self.app
        raise KeyError(key)


class ItsYouOnlineConfiguration(object):
    login_url = unicode_property('login_url')
    login_with_organization = bool_property('login_with_organization')
    cookie_name = unicode_property('cookie_name')
    cookie_key = unicode_property('cookie_key')
    root_organization = typed_property('root_organization', RootOrganization)  # type: RootOrganization
    require_memberof = bool_property('require_memberof')
    required_scopes = unicode_property('required_scopes')
    jwt_audience = unicode_property('jwt_audience')
    # e.g. staging.itsyou.online
    api_domain = unicode_property('api_domain')
    iyo_public_key = unicode_property('iyo_public_key')
    fetch_information = bool_property('fetch_information')
