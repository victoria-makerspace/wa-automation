from datetime import datetime, timezone
import config

def archive(contacts, now):
    archive_msg = f'Archiving non-members who have not logged in within {config.archive_threshold.days} days:'

    for contact in contacts.getlevel('New Applicant'):
        if not contact.archived and contact.last_login < now - config.archive_threshold:
            if archive_msg:
                print(archive_msg)
                archive_msg = None

            contact.archived = True
            print(f'\t{contact}')
