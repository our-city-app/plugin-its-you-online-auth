from urlparse import urljoin

import requests


class Oauth2ClientOauth_2_0(object):
    def __init__(self):
        from . import BASE_URI
        self.access_token_uri = urljoin(BASE_URI, '/v1/oauth/access_token')

    def get_access_token(self, client_id, client_secret, scopes=[], audiences=[]):
        params = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        if len(scopes) > 0:
            params['scope'] = ",".join(scopes)
        if len(audiences) > 0:
            params['aud'] = ",".join(audiences)

        return requests.post(self.access_token_uri, params=params)
