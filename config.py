from args import args
from configparser import ConfigParser
from datetime import timedelta
import sys

# Defaults
config = {
        'account': None,
        'api-host': 'https://api.wildapricot.org',
        'secret': None,
        'archive': {
            'levels': [],
            'threshold': timedelta(60)},
        'auto-approve': {
            'searchName': None},
        'auth-endpoint': 'https://oauth.wildapricot.org/auth/token',
        'discourse': {
            'host': None,
            'username': 'system',
            'api-key': None},
        'options': {
            'debug': False}}

# Read configuration file
parser = ConfigParser()

if args.config_file:
    parser.read(args.config_file)

archive = parser['archive'] if 'archive' in parser else {}
client = parser['client'] if 'client' in parser else {}
discourse = parser['discourse'] if 'discourse' in parser else {}
options = parser['options'] if 'options' in parser else {}
server = parser['server'] if 'server' in parser else {}
autoApprove = parser['auto-approve'] if 'auto-approve' in parser else {}

# Configuration variable declarations
if args.account:
    config['account'] = args.account
elif 'account-id' in client:
    config['account'] = client['account-id']

if args.key:
    config['secret'] = args.key
elif 'secret' in client:
    config['secret'] = client['secret']

if 'api' in server:
    config['api-host'] = server['api']

if 'levels' in archive:
    config['archive']['levels'] = [level.strip() for level in archive['levels'].split(',')]

if 'threshold' in archive:
    config['archive']['threshold'] = timedelta(int(archive['threshold']))

if 'searchName' in autoApprove:
    config['auto-approve']['searchName'] = autoApprove['searchName']

if 'auth' in server:
    config['auth-endpoint'] = server['auth']

## Discourse 
if 'host' in discourse:
    config['discourse']['host'] = discourse['host']

if 'username' in discourse:
    config['discourse']['username'] = discourse['username']

if 'api-key' in discourse:
    config['discourse']['api-key'] = discourse['api-key']

if 'debug' in options:
    config['options']['debug'] = options['debug']

