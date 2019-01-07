from config import config
from contacts import Contacts
from requests import request
import sys
from time import sleep, time

class Discourse:
    def __init__(self, host, username, api_key, wild_apricot_contacts):
        self.host = host
        self.username = username
        self.api_key = api_key
        self.users = {}
        self.wa_contacts = wild_apricot_contacts
        self.rate_limit = 0.1

    def request(self, verb, endpoint, params = {}, data = {}):
        params['api_key'] = self.api_key
        params['api_username'] = self.username

        if hasattr(self, 'last_request') and time() < self.last_request + self.rate_limit:
            sleep(self.rate_limit)

        self.last_request = time()

        if config['options']['debug']:
            name = type(self).__name__
            debug = f'DEBUG {name}: {verb} {endpoint}'
            orig_params = params.copy()
            del orig_params['api_key']
            del orig_params['api_username']

            if len(orig_params) is not 0:
                debug += f'\n\tquery: {orig_params}'

            if len(data) is not 0:
                debug += f'\n\tbody: {data}'

            print(debug, file = sys.stderr)

        response = request(
                verb,
                self.host + endpoint,
                params = params,
                json = data)

        if not response.ok:
            name = type(self).__name

            if response.status_code is 429:
                self.rate_limit *= 2
                print(f'DEBUG {name}: doubling rate limit to {self.rate_limit} seconds', file = sys.stderr)
                sleep(30)
                return self.request(verb, endpoint, params, data)

            raise Exception(f'{response.status_code}: {response.reason}')

        return response.json()

    def fetch_all(self):
        # Because the Discourse API offers no way to query for a list of all
        # users (the `/admin/users/list.json` endpoint is limited to 100, with
        # no capability of paging), we need this hacky method to retrieve the
        # list.
        for _ in self.group_users('trust_level_0'): pass

    def find(self, user_id):
        if user_id not in self.users:
            user = self.request('GET', f'/admin/users/{user_id}.json')
            self.users[user_id] = {
                    'id': user['id'],
                    # Retrieving members by group won't return their e-mail
                    # address, so we unfortunately need to make a separate
                    # request _per_ user.
                    'email': self.request('GET',
                        # The `/admin/users/{id}.json` endpoint is not
                        # consistent in returning an e-mail address for a user,
                        # so we use this endpoint instead.
                        f"/users/{user['username']}/emails.json")['email'],
                    'name': user['name'],
                    'username': user['username']}

        return self.users[user_id]

    def find_by_email(self, email):
        for user in self.users.values():
            if user['email'].lower() == email.lower():
                return user

        users = client.request('GET', '/admin/users/list.json', {
            'filter': email,
            'show_emails': 'true'})

        if len(users) is 0:
            return None

        for user in users:
            self.users[user['id']] = {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'username': user['username']}

            if user['email'].lower() == email.lower():
                return self.users[user['id']]

        return None

    def group_users(self, group):
        total = self.request(
                'GET',
                f'/groups/{group}/members.json',
                {'limit': 0})['meta']['total']
        members = self.request(
                'GET',
                f'/groups/{group}/members.json',
                {'limit': total})['members']

        for member in members:
            if member['id'] not in self.users:
                self.users[member['id']] = {
                        'id': member['id'],
                        # Retrieving members by group won't return their e-mail
                        # address, so we unfortunately need to make a separate
                        # request _per_ user.
                        'email': self.request('GET',
                            # The `/admin/users/{id}.json` endpoint is not
                            # consistent in returning an e-mail address for the
                            # user, so we use this endpoint instead.
                            f"/users/{member['username']}/emails.json")['email'],
                        'name': member['name'],
                        'username': member['username']}

            yield self.users[member['id']]

    def _pass_group_users(self, verb, group, user_ids):
        if len(user_ids) is 0:
            return

        group_id = self.request('GET', f'/groups/{group}.json')['group']['id']
        self.request(
                verb,
                f'/groups/{group_id}/members.json',
                data = {'user_ids': ','.join(str(user_ids))})

    def add_to_group(self, group, user_ids):
        self._pass_group_users('PUT', group, user_ids)

    def remove_from_group(self, group, user_ids):
        self._pass_group_users('DELETE', group, user_ids)

    # This method cross-references members of a Discourse group with a Wild
    # Apricot membership level(s), and ensures only e-mails matching the Wild
    # Apricot members remain in or are added to the Discourse group. Returns a
    # tuple of `(added, removed)` lists of user IDs.
    def sync_group_to_levels(self, group, levels):
        to_add = []
        to_remove = []
        contacts = self.wa_contacts.getlevel(*levels)

        for contact in contacts:
            user = self.find_by_email(contact.email)

            if user is not None:
                to_add.append(user['id'])

        for user_id in self.group_users(group):
            if user_id in to_add:
                to_add.remove(user_id)
            else:
                to_remove.append(user_id)

        #self.add_to_group(group, to_add)
        #self.remove_from_group(group, to_remove)
        return (to_add, to_remove)

client = Discourse(
        config['discourse']['host'],
        config['discourse']['username'],
        config['discourse']['api-key'],
        Contacts())
