from contact import Contact

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
