from args import args
from configparser import ConfigParser
from datetime import timedelta
import sys

# Defaults
config = {
        'account': None,
        'api_host': 'https://api.wildapricot.org',
        'archive-levels': [],
        'archive-threshold': timedelta(60),
        'auth_endpoint': 'https://oauth.wildapricot.org/auth/token'}

# Read configuration file
parser = ConfigParser()

if args.config_file:
    parser.read(args.config_file)

client = parser['client'] if 'client' in parser else {}
server = parser['server'] if 'server' in parser else {}
archive = parser['archive'] if 'archive' in parser else {}

# Configuration variable declarations
if args.account:
    config['account'] = args.account
elif 'account-id' in client:
    config['account'] = client['account-id']
if 'api' in server:
    config['api_host'] = server['api']
if 'levels' in archive:
    config['archive-levels'] = [level.strip() for level in archive['levels'].split(',')]
if 'threshold' in archive:
    config['archive-threshold'] = timedelta(int(archive['threshold']))
if 'auth' in server:
    config['auth_endpoint'] = server['auth']
