from config import config
from session import Session
from datetime import datetime, timezone

def getSavedSearchList(session):
  savedSearchList = session.request('GET', 'savedsearches')
  return savedSearchList

def getSavedSearchIdByName(session, savedSearchList, targetName):
  for search in savedSearchList:
    if search["Name"].lower() == targetName:
      return search["Id"]
  return None

def approveMembership(session, contactId):
  print(contactId)
  temp = 'ApprovePendingMembership?contactId='+str(contactId)
  response = session.RPCrequest('POST', temp)

def autoApprove(contacts):
  session = contacts.session
  savedSearchList = getSavedSearchList(session)
  searchId = getSavedSearchIdByName(session, savedSearchList, "list-of-members-to-approve")
  temp = 'savedsearches/'+str(searchId)
  searchResults = session.request('GET', temp)
  contactIdsToApprove = searchResults["ContactIds"]

  for contact in contactIdsToApprove:
    approveMembership(session, contact)
  


