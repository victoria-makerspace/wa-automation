from dateutil.parser import parse

class Contacts:
    from session import Session

    def __init__(self, session = Session()):
        self.session = session
        self.response = session.request('GET', 'contacts')['Contacts']
        self.list = {}

        for item in self.response:
            contact = Contact(item, session)
            self.list[contact.ID] = contact

    def get(self, ID):
        return self.list[ID] if ID in self.list else None

    def find(self, email):
        for contact in self.list.values():
            if contact.email == email:
                return contact

        return None

    @property
    def levels(self):
        levels = set()

        for contact in self.list.values():
            if contact.level is not None:
                levels.add(contact.level)

        return levels

class Contact:
    def __init__(self, response, session):
        self.session = session
        self.response = response

    def __str__(self):
        return f'{self.name} <{self.email}> #{self.ID}'

    def __field(self, name):
        for field in self.response['FieldValues']:
            if field['FieldName'] == name:
                return field

        return None

    def describe(self):
        f = {'ID': self.ID}
        f['Name'] = self.name
        f['E-mail'] = self.email
        phone = self.field('Phone')
        if phone: f['Phone'] = phone
        f['Last login'] = self.last_login
        f['Last updated'] = self.last_updated
        member_since = self.field('Member since')
        if member_since: f['Member since'] = member_since
        f['Created'] = self.field('Creation date')
        if self.archived: f['Archived'] = None
        if self.field('Suspended member'): f['Suspended'] = None
        if self.level: f["Membership level"] = self.level
        balance = self.field('Balance')
        if balance: f['Balance'] = balance
        donated = self.field('Total donated')
        if donated: f['Amount donated'] = donated

        for k, v in f.items():
            d = f'{k}:'
            f[k] = f'{d:<20} {v}' if v else k

        return '\n'.join(f.values())

    def field(self, name):
        field = self.__field(name)

        if field is not None:
            return field['Value']

        return None

    def fields(self):
        fields = {}

        for field in self.response['FieldValues']:
            fields[field['FieldName']] = field['Value']

        return fields

    def put(self, data = {}, params = {}):
        data['Id'] = self.ID
        self.response = self.session.request('PUT', f'contacts/{self.ID}', params, data)

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
    def ID(self):
        return self.response['Id']

    @property
    def last_login(self):
        return parse(self.field('Last login date'))

    @property
    def last_updated(self):
        return parse(self.response['ProfileLastUpdated'])

    @property
    def level(self):
        if 'MembershipLevel' in self.response:
            return self.response['MembershipLevel']['Name']

        return None

    @property
    def name(self):
        return f"{self.response['FirstName']} {self.response['LastName']}"
