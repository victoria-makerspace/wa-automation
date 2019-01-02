class Session:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
    # Wild Apricot uses "APIKEY" as the client ID, and the client secret is
    # generated in Settings -> Security -> Authorized applications.
    CLIENT_ID = 'APIKEY'

    def __init__(self, config):
        self.config = config
        client = self.BackendApplicationClient(client_id = self.CLIENT_ID)
        self.oauth2_session = self.OAuth2Session(client = client)
        self.token = self.oauth2_session.fetch_token(config.auth_endpoint, client_id = self.CLIENT_ID, client_secret = config.secret, scope = 'auto')
        self.account = config.account or token['Permissions'][0]['AccountId']

    # get synchronously queries the Wild Apricot API
    def get(self, endpoint, params = {}):
        endpoint = '/v2.1/accounts/' + str(self.account) + '/' + endpoint
        params['$async'] = False
        response = self.oauth2_session.get(self.config.api_host + endpoint, params = params)

        if not response.ok:
            raise Exception(str(response.status_code) + ': ' + response.reason)

        return response.json()
