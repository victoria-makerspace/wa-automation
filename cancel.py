from config import config
from contacts import Contacts
from emailRecipient import *
from email2 import Email2
from session import Session
import json
#from emailRecipient import convert_to_dic


def autoCancel(contacts):
  f= open("..\CancelTheseCards.txt", "a+")
  session = contacts.session
  
  for contact in contacts.getlevel("Cancel My Membership"):
    # contact.archived = True
    
    f.write(contact.name)

    recipient = EmailRecipient(53173355, 'Kyle Bisley', 'grants@makerspace.ca', 'IndividualRecipient')

    j_recipient = json.dumps(recipient, default=convert_to_dic)

    mail = Email2('test subject', 'test body', j_recipient)

    j_mail = json.dumps(mail, default=convert_to_dic)
    temp = session.request('email', 'sendemail', rpc=True, data=j_mail)
    print('Response')
    print(temp)
    
  f.close()
    
def convert_to_dic(self):
#   A function takes in a custom object and returns a dictionary representation of the object.
#   This dict representation includes meta data such as the object's module and class names.
  
  #  Populate the dictionary with object meta data 
    obj_dict = {
        "__class__": self.__class__.__name__,
        "__module__": self.__module__
    }
  
  #  Populate the dictionary with object properties
    obj_dict.update(self.__dict__)
  
    return obj_dict
