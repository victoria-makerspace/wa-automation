from config import config
from datetime import datetime, timezone

def archive(contacts, now):
    archive_msg = f"Archiving non-members who have not logged in within {config['archive-threshold'].days} days:"

    #for contact in contacts.getlevel(None, *config['archive-levels']):
    for contact in contacts.getlevel(*config['archive-levels']):
        if not contact.archived and contact.last_login < now - config['archive-threshold']:
            if archive_msg:
                print(archive_msg)
                archive_msg = None

            #contact.archived = True
            print(f'\t{contact}')
