from config import config
from contacts import Contacts
from emailRecipient import EmailRecipient
from email2 import Email2
from session import Session


def autoCancel(contacts):
  f= open("..\CancelTheseCards.txt", "a+")
  session = contacts.session
  
  for contact in contacts.getlevel("Cancel My Membership"):
    contact.archived = True
    
    f.write(contact.name)

    recipient = EmailRecipient(53173355, 'Kyle Bisley', 'grants@makerspace.ca', 'IndividualRecipient')

    mail = Email2('test subject', 'test body', recipient)
    temp = session.request('email', 'sendemail', rpc=True, data=mail)
    print('Response')
    print(temp)
    
  f.close()
