from config import config
from session import Session
from datetime import datetime, timezone

def getSavedSearchList(session):
  savedSearchList = session.request('GET', 'savedsearches')
  return savedSearchList

def getSavedSearchIdByName(session, savedSearchList, targetName):
  # return search id from given target name
  for search in savedSearchList:
    if search["Name"].lower() == targetName:
      return search["Id"]
  return None

# method to approve contact by Id
def approveMembership(session, contactId):
  temp = 'ApprovePendingMembership?contactId='+str(contactId)
  response = session.RPCrequest('POST', temp)

def autoApprove(session):
  # Search for "list-of-members-to-approve" in the list of all saved searches
  savedSearchList = getSavedSearchList(session)
  searchId = getSavedSearchIdByName(session, savedSearchList, "list-of-members-to-approve")
  
  # Creat a temporary string for search endpoint
  temp = 'savedsearches/'+str(searchId)
  searchResults = session.request('GET', temp)
  
  # for each contact returned within saved search call the approve method
  if searchResults["ContactIds"]:
    contactIdsToApprove = searchResults["ContactIds"]
    for contact in contactIdsToApprove:
      approveMembership(session, contact)
  


