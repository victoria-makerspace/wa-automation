


{
  "Subject": "string",
  "Body": "string",
  "Recipients": [
    {
      "Id": 0,
      "Type": "IndividualRecipient",
      "Name": "string",
      "Email": "string"
    }
  ],
  "EventId": 0
}
class Email:
  def __init__(self, subject, body, recipients):
    self.subject = subject
    self.body = body
    self.recipients = recipients
    self.eventId = 0
  
@property
def emailAddress(self):
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
def body(self, toAppend):
  self.body = self.body + '\n' + toAppend

@property
def eventId(self):
  if eventId is not 0:
    return self.eventId
  else:
    return "Email not associated with event"


