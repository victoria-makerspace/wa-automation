
Enum:
[ ]
Name	string
Display name of recipient or name of saved search.

Email	string
recipient email. for IndividualRecipient and SentEmailRecipient types only

}

class SentEmailRecipient:
  def __init__(self, id, name, emailAddress, recipientType = 1):
    # id refers to individual recipient or saved search identifier
    self.Id = id

    # interger refering to recipient group type (assuming for now that integers are as follows)
    #   1 IndividualRecipient, 
    #   2 EventAttendees_All, 
    #   3 EventAttendees_Selected,
    #   4 Contacts_All,
    #   5 Contacts_Selected,
    #   6 Contacts_SavedSearch,
    #   7 Members_All, 
    #   8 Members_SavedSearch, 
    #   9 SentEmailRecipient, 
    #   10 EventWaitlist_All, 
    #   11 EventWaitlist_Selected 
    self.type = recipientType

    # name of recipient or name of saved search.
    self.name = name

    self.email = email.setter(self, recipientType, emailAddress)

  @property
  def emailAddress(self):
    return self.email
  
  #setter for emailAddress because it can only be set when type is IndividualRecipient or SentEmailRecipient
  @email.setter
  def emailAddress(self, recipientType, email):
    if recipientType is not 1 or 8:
      self.email = email
    else:
      self.email = None
