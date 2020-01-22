from config import config
from contacts import Contacts
from contact import Contact
from electronic_mail import electronic_mail
from email_recipient import email_recipient
from pprint import pprint
import pdb
from datetime import datetime
from approve import approve_membership
import json

def send_timeout_mail(session, contact, id):
    with open('./emails/timeout.txt', 'r') as draft:
        email_body = draft.read()
    email_body.format(contact.name)
    recipient = email_recipient(id, contact, 0)
            
    mail = electronic_mail('Membership invoice timed out', email_body, [recipient])
    j_mail = json.dumps(mail, default = electronic_mail.convert_to_dic)
            
    session.request('POST', 'email/SendEmail', rpc=True, data=json.loads(j_mail))           

def timeout(session, contacts, now):
    
    balance_due = contacts.balance_due()

    for id in balance_due:
        temp = f'invoices?contactId={id}'
        invoice = session.request('GET', temp)
        datetime_object = datetime.strptime(invoice['Invoices'][0]['DocumentDate'], '%Y-%m-%dT%H:%M:%S%z')
            
        if(((now - datetime_object) >= config['application_stale']['timeout']) & 
                (invoice['Invoices'][0]['OrderType']=='MembershipApplication')):
            # email timeout draft
            contact = contacts.get(id)
            send_timeout_mail(session, contact, id)

            # void the invoice
      
            invoice_id = int(invoice['Invoices'][0]['Id'])
            temp = f'VoidInvoice?invoiceId={invoice_id}'
            invoice = session.request('POST', temp, rpc=True)

            # # cancel their application
            temp= f'RejectPendingMembership?contactId={id}'
            session.request('POST', temp, rpc=True)
            
            #assign membership level to New Applicant
            contact = contacts.get(id)
            data = {'Id': id,
                    'MembershipLevel': {
                        'Id': 1113397,
                        'Name': 'New Applicant'},
                    'MembershipEnabled': True}
            temp = f'contacts/{id}'  
            response = session.request('PUT', temp, data=data)

            #approve New Applicant Level and Archive the contact
            approve_membership(session, id)
            contact.archived = True
