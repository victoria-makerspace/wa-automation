import json
from config import config
from email_recipient import email_recipient
from electronic_mail import electronic_mail

def auto_cancel(contacts):

    # Build a set of members names found in the Cancel my Membership
    # membership level
    cancel_set = {''}
    for contact in contacts.getlevel('Cancel My Membership'):
        # contact.archived = True
        cancel_set.add(contact.name)

    # concatenates the list of members to cancel to the draft from file
    seperator = '<br>'
    temp = seperator.join(cancel_set)
    with open('./emails/cancel.txt', 'r') as draft:
        email_body = draft.read()
    email_body = email_body + '<br>' + temp

    # constructs email_recipient object for mail to security
    security = contacts.get(int(config['cancel']['id']))
    # pdb.set_trace()
    recipient = email_recipient(config['cancel']['id'], security, 0)

    # constructs electronic_mail object and converts object to json
    mail = electronic_mail('Acces cards to deactivate: ', email_body, [recipient])
    j_mail = json.dumps(mail, default=electronic_mail.convert_to_dic)

    # API call to send email
    contacts.session.request('POST', 'email/SendEmail', rpc=True, data=json.loads(j_mail))
