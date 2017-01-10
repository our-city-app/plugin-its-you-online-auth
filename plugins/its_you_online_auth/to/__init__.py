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
from mcfw.consts import DEBUG
from plugins.its_you_online_auth.plugin_consts import SOURCE_WEB, SOURCE_APP, SOURCE_DEV


class OauthConfig(object):
    def __init__(self, config):
        self.client_secret = config['client_secret']
        self.redirect_uri = config['redirect_uri']


class RootOrganization(object):
    def __init__(self, config):
        self.name = config['name']
        self.dev = OauthConfig(config[SOURCE_DEV])
        self.web = OauthConfig(config[SOURCE_WEB])
        self.app = OauthConfig(config[SOURCE_APP])

    def __getitem__(self, key):
        if isinstance(key, (str, unicode)):
            if key == SOURCE_WEB:
                return self.dev if DEBUG else self.web
            if key == SOURCE_APP:
                return self.app
        raise KeyError(key)


class ItsYouOnlineConfiguration(object):
    def __init__(self, config):
        self.login_url = config['login_url']
        self.cookie_name = config['cookie_name'].encode('utf8')
        self.cookie_key = config['cookie_key'].encode('utf8')
        self.root_organization = RootOrganization(config['root_organization'])
