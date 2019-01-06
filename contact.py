from dateutil.parser import parse

class Contact:
    def __init__(self, response, session):
        self.session = session
        self.response = response

    def __str__(self):
        email = f'<{self.email}>'
        desc = f'{self.name:20} {email:30} ID# {self.ID:8}'

        if self.level:
            desc += f' {self.level:15}'

        if self.archived:
            desc += ' ARCHIVED'

        return desc

    def __field(self, name):
        for field in self.response['FieldValues']:
            if field['FieldName'] == name:
                return field

        return None

    def describe(self):
        f = { 'ID': self.ID }
        f['Name'] = self.name
        f['E-mail'] = self.email
        phone = self.field('Phone')
        if phone: f['Phone'] = phone
        f['Last login'] = self.last_login if self.last_login else 'Never'
        f['Last updated'] = self.last_updated if self.last_updated else 'Never'
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
        self.response = self.session.request(
                'PUT',
                f'contacts/{self.ID}',
                params,
                data)

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
        if self.field('Last login date') is None:
            return None

        return parse(self.field('Last login date'))

    @property
    def last_updated(self):
        if 'ProfileLastUpdated' not in self.response:
            return None

        return parse(self.response['ProfileLastUpdated'])

    @property
    def level(self):
        if 'MembershipLevel' in self.response:
            return self.response['MembershipLevel']['Name']

        return None

    @property
    def name(self):
        return f"{self.response['FirstName']} {self.response['LastName']}"
