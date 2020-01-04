from config import config
# return search id from given target name


def get_search_id(saved_search_list, target_name):
    for search in saved_search_list:
        if search["Name"].lower() == target_name:
            return search["Id"]
    return None

# method to approve contact by Id


def approve_membership(session, contact_id):
    temp = 'ApprovePendingMembership?contactId='+str(contact_id)
    session.RPCrequest('POST', temp)


def auto_approve(session):
    # Search for "list-of-members-to-approve" in the list of all saved searches
    saved_search_list = session.request('GET', 'savedsearches')
    search_id = get_search_id(
        saved_search_list, config['auto-approve']['searchName'])

    # Creat a temporary string for search endpoint
    temp = 'savedsearches/'+str(search_id)
    search_results = session.request('GET', temp)

    # for each contact returned within saved search call the approve method
    if search_results["ContactIds"]:
        contact_ids_to_approve = search_results["ContactIds"]
        for contact in contact_ids_to_approve:
            approve_membership(session, contact)
