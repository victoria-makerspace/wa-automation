from dateutil.parser import parse

from session import Session

class Contacts:
    def __init__(self, session = Session()):
        self.session = session
        self.response = session.get('contacts')['Contacts']
        self.levels = {}

        for contact in self.response:
            contact = Contact(contact)

            if contact.archived:
                continue

            if contact.level not in self.levels:
                self.levels[contact.level] = {}

            self.levels[contact.level][contact.ID] = contact

    def get(self, ID):
        for level in self.levels:
            if ID in level:
                return self.levels[level][ID]

        return None

class Contact:
    def __init__(self, response):
        self.response = response
        self.level = None
        self.ID = response['Id']
        self.name = response['FirstName'] + ' ' + response['LastName']
        self.fields = {}

        if 'MembershipLevel' in response:
            self.level = response['MembershipLevel']['Name']

        for field in response['FieldValues']:
            self.fields[field['FieldName']] = field['Value']

        self.archived = self.fields['Archived']
        self.last_login = parse(self.fields['Last login date'])
