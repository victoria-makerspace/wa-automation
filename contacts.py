from dateutil.parser import parse

class Contacts:
    from session import Session

    def __init__(self, session = Session()):
        self.session = session
        self.response = session.request('GET', 'contacts')['Contacts']
        self.levels = {}

        for contact in self.response:
            contact = Contact(contact, session)

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

    def find(self, email):
        for level in self.levels:
            for contact_id in self.levels[level]:
                contact = self.levels[level][contact_id]
                if contact.email == email:
                    return contact

        return None

class Contact:
    def __init__(self, response, session):
        self.response = response
        self.session = session
        self.ID = response['Id']

    def __field(self, name):
        for field in self.response['FieldValues']:
            if field['FieldName'] == name:
                return field

        return None

    def field(self, name):
        field = self.__field(name)

        if field is not None:
            return field['Value']

        return None

    def put(self, data = {}, params = {}):
        data['Id'] = self.ID
        self.response = self.session.request('PUT', 'contacts/%d' % self.ID, params, data)

    @property
    def archived(self):
        return self.field('Archived')

    @archived.setter
    def archived(self, archived):
        if self.archived == archived:
            return

        data = {'FieldValues': [self.__field('Archived')]}
        data['FieldValues'][0]['Value'] = archived
        self.put(data)

    @property
    def email(self):
        return self.response['Email']

    @property
    def last_login(self):
        return parse(self.field('Last login date'))

    @property
    def level(self):
        if 'MembershipLevel' in self.response:
            return self.response['MembershipLevel']['Name']

        return None

    @property
    def name(self):
        return '%s %s' % (self.response['FirstName'], self.response['LastName'])
