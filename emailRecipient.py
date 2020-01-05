
class EmailRecipient:
    def __init__(self, id, name, email_address, recipient_type):
        # id refers to individual recipient or saved search identifier
        self.id = id
        # interger refering to recipient group type (assuming for now that integers are as follows)
        #IndividualRecipient, EventAttendees_All, EventAttendees_Selected, Contacts_All,
        #Contacts_Selected, 5 Contacts_SavedSearch, Members_All, Members_SavedSearch,
        #SentEmailRecipient, EventWaitlist_All, EventWaitlist_Selected
        self.type = recipient_type
        # name of recipient or name of saved search.
        self.name = name
        self.email = email_address
