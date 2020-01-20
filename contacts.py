from contact import Contact
from pprint import pprint

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
            if contact.email.lower() == email.lower():
                return contact

        return None
    
    def balance_due(self):
        balance_due_ids = []
        for contact in self.list.values():
            if contact.field('Balance') != 0:
                balance_due_ids.append(contact.field('User ID'))
        if balance_due_ids:
            return balance_due_ids
        else:
            return None

    def getlevel(self, *levels):
        contacts = {}

        for contact in self.list.values():
            if contact.level in levels:
                yield contact

    @property
    def levels(self):
        levels = set()

        for contact in self.list.values():
            if contact.level is not None:
                levels.add(contact.level)

        return levels
