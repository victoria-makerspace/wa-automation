import sys

def describe(contacts, args):
    if len(args) != 1:
        print('Error: invalid number of arguments to `describe`: requires 1', file = sys.stderr)
        return

    contact = contacts.find(args[0])

    if contact is None:
        print(f'Error: e-mail <{args[0]}> not associated with a contact', file = sys.stderr)
        return

    print(contact.describe())
