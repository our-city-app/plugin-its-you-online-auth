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

from .client import Client as APIClient
import requests
from urlparse import urljoin
BASE_URI = "https://itsyou.online/"

class Oauth:
    def __init__(self):
        self.url = urljoin(BASE_URI, '/v1/oauth/')
        self.session = requests.Session()

    def LoginViaClientCredentials(self, client_id, client_secret):
        url = urljoin(self.url, 'access_token')
        params = {'grant_type': 'client_credentials',
                  'client_id': client_id,
                  'client_secret': client_secret}
        data = self.session.post(url, params=params)
        if data.status_code != 200:
            raise RuntimeError("Failed to login")
        token = data.json()['access_token']
        self.session.headers['Authorization'] = 'token {token}'.format(token=token)

    def CreateJWTToken(self, scopes=None, audiences=None):
        url = urljoin(self.url, 'jwt')
        params = {
            'scope': scopes,
            'aud': audiences
        }
        data = self.session.get(url, params=params)
        return data.text


class Client:
    def __init__(self):
        session = requests.Session()
        self.api = APIClient()
        self.api.session = session
        self.oauth = Oauth()
        self.oauth.session = session
