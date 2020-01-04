from config import config
from contacts import Contacts

def autoCancel(contacts):
  f= open("..\CancelTheseCards.txt", "a+")
  
  for contact in contacts.getlevel("Cancel My Membership"):
    contact.archived = True
    f.write(contact.name)
    
  f.close()
