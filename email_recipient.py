import pdb 
from contacts import Contacts
from contact import Contact

class email_recipient:
    def __init__(self, id, contact, recipient_type):
        # id refers to individual recipient or saved search identifier
        self.Id = id
        # interger refering to recipient group type (assuming for now that integers are as follows)
        # 0 IndividualRecipient, 1 EventAttendees_All, 2 EventAttendees_Selected, 3 Contacts_All,
        # 4 Contacts_Selected, 5 Contacts_SavedSearch, 6 Members_All, 7 Members_SavedSearch,
        # 8 SentEmailRecipient, 9 EventWaitlist_All, 10 EventWaitlist_Selected
        self.Type = recipient_type
        # name of recipient or name of saved search.
        self.Name = contact.name
        self.Email = contact.email
