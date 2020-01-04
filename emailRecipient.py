
class EmailRecipient:
    def __init__(self, id, name, email_address, recipient_type=1):
        # id refers to individual recipient or saved search identifier
        self.id = id
        # interger refering to recipient group type (assuming for now that integers are as follows)
        #   1 IndividualRecipient, 2 EventAttendees_All, 3 EventAttendees_Selected, 4 Contacts_All,
        #   5 Contacts_Selected, 6 Contacts_SavedSearch, 7 Members_All, 8 Members_SavedSearch,
        #   9 SentEmailRecipient, 10 EventWaitlist_All, 11 EventWaitlist_Selected
        self.type = recipient_type
        # name of recipient or name of saved search.
        self.name = name
        self.email = email.set_email(self, recipient_type, email_address)

    @property
    def email_address(self):
        return self.email

    #setter for emailAddress because it can only be set when type is IndividualRecipient
    # or SentEmailRecipient
    @email.setter
    def set_email(self, recipient_type, email_address):
        if recipient_type is not 1 or 8:
            self.email = email_address
        else:
            self.email = None
