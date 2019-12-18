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

# for each member ID
#   approve members applications
#     - check to see if possible (might be a good addition to the contacts request )
          # In order to prevent failures it is recommended to get contact details with parameter getExtendedMembershipInfo=true and use list of allowed actions from Contact.ExtendedMembershipInfo.AllowedActions
#     - post approve
#       '/rpc/{accountId}/ApprovePendingMembership'

# def getSavedSearchList(session):
#   searchResults = session.request('GET', 'savedsearches')
#   return searchResults


# def getSavedSearchIdByName(session, searchResults, targetName):
#   for search in searchResults
#       if search.name.lower() == targetName
#           return search.ID
#   return None

# def getListToApprove(session, searchId):
#   contactsIdList = session.request('GET', 'AprovePendingMembership', searchId)
  
#   for contactId in contactsIdList
#     response = session.request('POST', /rpc/AprovePendingMembership', contactId)
#     if response != 200
#         do something with the response

