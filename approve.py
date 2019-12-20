# (member ID's are going to have to be our identifier for endpoint work)
# Maybe no? https://gethelp.wildapricot.com/en/articles/502#filtering

# get sublist of members to auto-approve
#   - run search (appears to have to be a saved search)
#     - returns list of member ID's
#   '/accounts/{accountId}/savedsearches/{savedSearchId}'
# OR----------------------------------------------------
# search in contacts for contacts fitting discription
#     member status is Pending - New
#     Current ballance :NOT: Balance overdue Overpaid

from config import config
from session import Session
from datetime import datetime, timezone
#import pdb 

# for each member ID
#   approve members applications
#     - post approve
#       '/rpc/{accountId}/ApprovePendingMembership'

def getSavedSearchList(session):
  savedSearchList = session.request('GET', 'savedsearches')
  #print(savedSearchList)
  return savedSearchList


def getSavedSearchIdByName(session, savedSearchList, targetName):
  for search in savedSearchList:
    #print(search)
    if search["Name"].lower() == targetName:
      return search["Id"]
  return None

# def getListToApprove(session, searchId):
#   contactsIdList = session.request('GET', 'AprovePendingMembership', searchId)
  
#   # for contactId in contactsIdList:
#   #   response = session.request('POST', /rpc/AprovePendingMembership', contactId)
#   #   if response != 200:
#   #       do something with the response

def approveMembership(session, contactId):
  print(contactId)
  temp = 'ApprovePendingMembership?contactId='+str(contactId)
  print(temp)
  response = session.RPCrequest('POST', temp)
  print(response)

def autoApprove(contacts):
  session = contacts.session
  savedSearchList = getSavedSearchList(session)
  searchId = getSavedSearchIdByName(session, savedSearchList, "list-of-members-to-approve")
  #print("search Results")
  #print(searchId)
  temp = 'savedsearches/'+str(searchId)
  #print(temp)
  searchResults = session.request('GET', temp)
  contactIdsToApprove = searchResults["ContactIds"]
  #print(contactIdsToApprove)
  for contact in contactIdsToApprove:
    approveMembership(session, contact)
  


