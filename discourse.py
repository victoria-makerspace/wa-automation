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
        self.wa_discourse_users = {}
        self.rate_limit = 0.1

        # Because the Discourse API offers no way to query for a list of all
        # users (the `/admin/users/list.json` endpoint is limited to 100, with
        # no capability of paging), we need this hacky method to retrieve the
        # list.
        for user in self.group_members('trust_level_0'):
            user['contact'] = self.wa_contacts.find(user['email'])

            if user['contact'] is not None:
                self.wa_discourse_users[user['id']] = user['contact']

                if config['options']['debug']:
                    print(f"DEBUG discourse: found contact:\n\t{user['contact']}", file = sys.stderr)

    def request(self, verb, endpoint, params = {}, data = {}):
        params['api_key'] = self.api_key
        params['api_username'] = self.username

        if hasattr(self, 'last_request') and time() < self.last_request + self.rate_limit:
            sleep(self.rate_limit)

        self.last_request = time()

        if config['options']['debug']:
            print(f'DEBUG discourse: {verb} {endpoint}', file = sys.stderr)

        response = request(
                verb,
                self.host + endpoint,
                params = params,
                json = data)

        if not response.ok:
            if response.status_code == 429:
                self.rate_limit *= 2
                sleep(30)
                return self.request(verb, endpoint, params, data)

            raise Exception(f'{response.status_code}: {response.reason}')

        return response.json()

    def group_members(self, group):
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

    def add_to_group(self, group, users):
        group_id = self.request('GET', f'/groups/{group}.json')['id']
        self.request(
                'PUT',
                f'/groups/{group_id}/members.json',
                data = {'usernames': ','.join(users)})

    def remove_from_group(self, group, users):
        group_id = self.request('GET', f'/groups/{group}.json')['id']

        for user in users:
            self.request(
                    'DELETE',
                    f'/groups/{group_id}/members.json',
                    data = {'user_id': user['id']})

    # This method cross-references members of a Discourse group with a Wild
    # Apricot membership level(s), and ensures only e-mails matching the Wild
    # Apricot members remain in or are added to the Discourse group. Returns
    # the list of Discourse users that were removed from the group.
    def sync_group_to_levels(self, group, levels):
        to_add = {}
        to_remove = {}

        for user_id in self.wa_discourse_users:
            contact = self.wa_discourse_users[user_id]

            if contact.level in levels:
                to_add[user_id] = self.users[user_id]

        for user in self.group_members(group):
            if user['id'] in to_add:
                del to_add[user['id']]
            else:
                to_remove[user['id']]  user

        self.add_to_group(group, to_add)
        self.remove_from_group(group, to_remove)
        return to_remove

client = Discourse(
        config['discourse']['host'],
        config['discourse']['username'],
        config['discourse']['api-key'],
        Contacts())


