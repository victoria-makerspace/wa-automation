from time import sleep, time
import json
from config import config


class Session:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
    # Wild Apricot uses "APIKEY" as the client ID
    CLIENT_ID = 'APIKEY'

    def __init__(self):
        client = self.BackendApplicationClient(client_id = self.CLIENT_ID)
        self.oauth2_session = self.OAuth2Session(client = client)
        token = self.oauth2_session.fetch_token(
            config['auth-endpoint'],
            client_id = self.CLIENT_ID,
            client_secret = config['secret'],
            scope = 'auto')
        self.account = int(config['account'] or token['Permissions'][0]['AccountId'])

    # request synchronously communicates with the Wild Apricot API
    def request(self, verb, endpoint, params = {}, data = {}, rpc = False):
        path_prefix = 'rpc' if rpc else 'accounts'
        endpoint = f'/v2.1/{path_prefix}/{self.account}/{endpoint}'
        params['$async'] = False

        # Rate-limiting because Wild Apricot limits API requests to 60 per
        # minute.
        if hasattr(self, 'last_request') and time() < self.last_request + 1:
            sleep(1)
        
        self.last_request = time()
        response = self.oauth2_session.request(
            verb,
            config['api-host'] + endpoint,
            params = params,
            json = data)
        
        if not response.ok:
            raise Exception(f'{response.status_code}: {response.reason}')

        return response.json()
