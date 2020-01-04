# {
#   "Subject": "string",
#   "Body": "string",
#   "Recipients": [
#     {
#       "Id": 0,
#       "Type": "IndividualRecipient",
#       "Name": "string",
#       "Email": "string"
#     }
#   ],
#   "EventId": 0
# }
class Email:
    def __init__(self, subject, body, recipients):
        self.subject = subject
        self.body = body
        self.recipients = recipients
        self.event_id = 0

    @property
    def email_address(self):
        for email in self.recipients['Email']:
            emails = emails + ', ' + email
        return emails

    @property
    def subject(self):
        return self.subject

    @property
    def body(self):
        return self.body

    @body.setter
    #setter to force all additions to email to be proceeded by a new line
    def body(self, to_append):
        self.body = self.body + '\n' + to_append

    @property
    def event_id(self):
        if event_id is not 0:
            return self.event_id
        return "Email not associated with event"
