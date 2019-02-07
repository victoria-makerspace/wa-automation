from config import config
from datetime import datetime, timezone

def archive(contacts, now):
    """
    Archives all non-members after a configurable number of days.
    Additionally, specific membership levels may also be configured to be
    archived.
    """
    level_msg = ''

    # The 'levels' configuration property is a list of membership levels that we
    # auto-archive in addition to all non-members.
    if len(config['archive']['levels']):
        # Format list of membership levels as a comma-delineated string for
        # readability.
        level_msg = ', '.join([f'"{level}"' for level in config['archive']['levels']])
        level_msg = f'and members in the {level_msg} levels '

    archive_msg = f"Archiving non-members {level_msg}who have not logged in within {config['archive']['threshold'].days} days:"

    for contact in contacts.getlevel(None, *config['archive']['levels']):
        # Ignore contacts that are already archived or have never logged in.
        if contact.archived or contact.last_login is None:
            continue

        # Ignore contacts that have logged in recently.
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
