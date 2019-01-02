from config import Config

class Session:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
    # Wild Apricot uses "APIKEY" as the client ID, and the client secret is
    # generated in Settings -> Security -> Authorized applications.
    CLIENT_ID = 'APIKEY'

    def __init__(self, config = Config()):
        self.config = config
        client = self.BackendApplicationClient(client_id = self.CLIENT_ID)
        self.oauth2_session = self.OAuth2Session(client = client)
        self.token = self.oauth2_session.fetch_token(config.auth_endpoint, client_id = self.CLIENT_ID, client_secret = config.secret, scope = 'auto')
        self.account = int(config.account or token['Permissions'][0]['AccountId'])

    # request synchronously communicates with the Wild Apricot API
    def request(self, verb, endpoint, params = {}, data = {}):
        endpoint = '/v2.1/accounts/%d/%s' % (self.account, endpoint)
        params['$async'] = False
        response = self.oauth2_session.request(verb, self.config.api_host + endpoint, params = params, json = data)

        if not response.ok:
            raise Exception('%d: %s' % (response.status_code, response.reason))

        return response.json()
