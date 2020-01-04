
class EmailRecipient:
    def __init__(self, id, name, email_address, recipient_type=1):
        # id refers to individual recipient or saved search identifier
        self.id = id
        # interger refering to recipient group type (assuming for now that integers are as follows)
        #   0 IndividualRecipient, 1 EventAttendees_All, 2 EventAttendees_Selected, 3 Contacts_All,
        #   4 Contacts_Selected, 5 Contacts_SavedSearch, 6 Members_All, 7 Members_SavedSearch,
        #   8 SentEmailRecipient, 9 EventWaitlist_All, 10 EventWaitlist_Selected
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
