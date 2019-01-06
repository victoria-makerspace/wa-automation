from config import config
from requests import request
from time import sleep, time
from contacts import Contacts

class Discourse:
    def __init__(self, host, username, api_key, wild_apricot_contacts):
        self.host = host
        self.username = username
        self.api_key = api_key
        self.wa_contacts = wild_apricot_contacts
        self.rate_limit = 1

    def request(self, verb, endpoint, params = {}, data = {}):
        params['api_key'] = self.api_key
        params['api_username'] = self.username

        if hasattr(self, 'last_request') and time() < self.last_request + self.rate_limit:
            sleep(self.rate_limit)

        self.last_request = time()
        response = request(
                verb,
                self.host + endpoint,
                params = params,
                json = data)

        if not response.ok:
            if response.status_code == 429:
                self.rate_limit *= 2
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
            yield {
                    'id': member['id'],
                    'email': self.request(
                        'GET',
                        # The /admin/users/{id}.json endpoint is not consistent
                        # in returning an e-mail address for the user, so we use
                        # this endpoint instead.
                        f"/users/{member['username']}/emails.json")['email'],
                    'name': member['name']}

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
        contacts = [contact.email for contact in self.wa_contacts.getlevel(*levels)]
        removed = []

        for user in self.group_members(group):
            contact = self.wa_contacts.find(user['email'])

            if contact is not None and contact.level in levels:
                continue

            removed.append(user)

        self.remove_from_group(group, removed)
        return removed

client = Discourse(
        config['discourse']['host'],
        config['discourse']['username'],
        config['discourse']['api-key'])

contacts = Contacts()

from pprint import pprint
for user in client.group_members('Members'):
    contact = contacts.find(user['email'])

    if contact is None:
        continue

    print(contact.describe())
