from argparse import ArgumentParser
from configparser import ConfigParser
from datetime import timedelta

# Defaults
AUTH_ENDPOINT = 'https://oauth.wildapricot.org/auth/token'
API_HOST = 'https://api.wildapricot.org'
ARCHIVE_THRESHOLD = 60

# Parse command-line arguments
parser = ArgumentParser()
parser.add_argument('-c', '--config', required = True, help = 'Path to configuration file')
parser.add_argument('-a', '--account', help = 'Wild Apricot account ID')
args = parser.parse_args()

# Read configuration file
config = ConfigParser()
config.read(args.config)
server = config['server'] if 'server' in config else {}
options = config['options'] if 'options' in config else {}

# Configuration variable declarations
auth_endpoint = server['auth'] if 'auth' in server else AUTH_ENDPOINT
api_host = server['api'] if 'api' in server else API_HOST
secret = config['client']['secret']
account = None
archive_threshold = timedelta(options['archive-threshold'] if 'archive-threshold' in options else ARCHIVE_THRESHOLD)

if args.account:
    account = args.account
elif 'account-id' in config['client']:
    account = config['client']['account-id']
