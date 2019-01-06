from config import config
from datetime import datetime, timezone

def archive(contacts, now):
    level_msg = ''

    if len(config['archive']['levels']):
        level_msg = ', '.join([f'"{level}"' for level in config['archive']['levels']])
        level_msg = f'and members in the {level_msg} levels '

    archive_msg = f"Archiving non-members {level_msg}who have not logged in within {config['archive']['threshold'].days} days:"

    for contact in contacts.getlevel(None, *config['archive']['levels']):
        if contact.archived or contact.last_login is None:
            continue

        if now - config['archive']['threshold'] <= contact.last_login:
            continue

        # Print the "Archiving..." message, but only once and only if at least
        # one archival will occur.
        if archive_msg:
            print(archive_msg)
            archive_msg = None

        contact.archived = True
        print(f'\t{contact}')

    if archive_msg:
        print(f'\tNo non-members {level_msg}to archive.')
