from urlparse import urljoin

import requests

from plugins.its_you_online_auth.libs.itsyouonline.client import Client as APIClient

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
