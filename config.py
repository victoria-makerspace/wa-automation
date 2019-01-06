from args import args
from configparser import ConfigParser
from datetime import timedelta
import sys

# Defaults
account = None
api_host = 'https://api.wildapricot.org'
archive_threshold = timedelta(60)
auth_endpoint = 'https://oauth.wildapricot.org/auth/token'

# Read configuration file
config = ConfigParser()
if args.config:
    config.read(args.config)
client = config['client'] if 'client' in config else {}
server = config['server'] if 'server' in config else {}
options = config['options'] if 'options' in config else {}

# Configuration variable declarations
if args.account:
    account = args.account
elif 'account-id' in client:
    account = client['account-id']
if 'api' in server:
    api_host = server['api']
if 'archive-threshold' in options:
    archive_threshold = timedelta(options['archive-threshold'])
if 'auth' in server:
    auth_endpoint = server['auth']
