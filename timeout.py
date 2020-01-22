import json
from datetime import datetime
from config import config
#from contacts import Contacts
#from contact import Contact
from electronic_mail import electronic_mail
from email_recipient import email_recipient
from approve import approve_membership


def send_timeout_mail(session, contact, contact_id):
    with open('./emails/timeout.txt', 'r') as draft:
        email_body = draft.read()
    email_body.format(contact.name)
    recipient = email_recipient(contact_id, contact, 0)

    mail = electronic_mail('Membership invoice timed out', email_body, [recipient])
    j_mail = json.dumps(mail, default=electronic_mail.convert_to_dic)

    session.request('POST', 'email/SendEmail', rpc=True, data=json.loads(j_mail))

def void_invoice(session, invoice):
    invoice_id = int(invoice['Invoices'][0]['Id'])
    temp = f'VoidInvoice?invoiceId={invoice_id}'
    invoice = session.request('POST', temp, rpc=True)

def assign_new_applicant(session, contact_id):
    data = {'Id': contact_id,
            'MembershipLevel': {
                'Id': 1113397,
                'Name': 'New Applicant'},
            'MembershipEnabled': True}
    temp = f'contacts/{contact_id}'
    session.request('PUT', temp, data=data)

def cancel_application(session, contact_id):
    temp = f'RejectPendingMembership?contactId={contact_id}'
    session.request('POST', temp, rpc=True)

def timeout(session, contacts, now):
    balance_due = contacts.balance_due()

    for contact_id in balance_due:
        temp = f'invoices?contactId={contact_id}'
        invoice = session.request('GET', temp)
        # FIX ME: Response could conceivably return multiple invoices. Only interested in the
        # invoice['Invoices'][0]['OrderType']=='MembershipApplication' kind. Also, unlikely we would
        # ever have an New Applicant with multiple invoices out.
        invoice_date = datetime.strptime(invoice['Invoices'][0]['DocumentDate'],
                                         '%Y-%m-%dT%H:%M:%S%z')

        #invoice is older than config file setting and its a Membership Application Invoice
        if(((now - invoice_date) >= config['application_stale']['timeout']) &
           (invoice['Invoices'][0]['OrderType'] == 'MembershipApplication')):
            contact = contacts.get(contact_id)
            #Steps to cancel application and archive contact as new applicant
            send_timeout_mail(session, contact, contact_id)
            void_invoice(session, invoice)
            cancel_application(session, contact_id)
            assign_new_applicant(session, contact_id)
            approve_membership(session, contact_id)
            contact.archived = True
