from config import config
from contacts import Contacts
from datetime import datetime
from email_recipient import *
from electronic_mail import electronic_mail
from session import Session
import pdb 
import json



def autoCancel(contacts):
    
    # Build a set of members names found in the Cancel my Membership
    # membership level
    cancel_set = {""}
    for contact in contacts.getlevel("Cancel My Membership"):
        # contact.archived = True
        cancel_set.add(contact.name)

    # concatenates the list of members to cancel to the draft from file
    seperator = '\n'
    temp = seperator.join(cancel_set)
    with open('./emails/cancel.txt', 'r') as f:
        email_body = f.read()
    email_body += temp

    security = contacts.get(int(config['cancel']['id']))
    # pdb.set_trace()
    recipient = email_recipient(config['cancel']['id'], security, 0)

    mail = electronic_mail('Acces cards to deactivate: ', email_body, [recipient])
    j_mail = json.dumps(mail, default=electronic_mail.convert_to_dic)
    
    temp = contacts.session.request('POST', 'email/SendEmail', rpc=True, data=json.loads(j_mail))
