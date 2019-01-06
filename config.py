from args import args
from configparser import ConfigParser
from datetime import timedelta
import sys

# Defaults
config = {
        'account': None,
        'api-host': 'https://api.wildapricot.org',
        'archive': {
            'levels': [],
            'threshold': timedelta(60)},
        'auth-endpoint': 'https://oauth.wildapricot.org/auth/token',
        'discourse': {
            'host': None,
            'username': None,
            'api-key': None}}

# Read configuration file
parser = ConfigParser()

if args.config_file:
    parser.read(args.config_file)

archive = parser['archive'] if 'archive' in parser else {}
client = parser['client'] if 'client' in parser else {}
discourse = parser['discourse'] if 'discourse' in parser else {}
server = parser['server'] if 'server' in parser else {}

# Configuration variable declarations
if args.account:
    config['account'] = args.account
elif 'account-id' in client:
    config['account'] = client['account-id']
if 'api' in server:
    config['api-host'] = server['api']
if 'levels' in archive:
    config['archive']['levels'] = [level.strip() for level in archive['levels'].split(',')]
if 'threshold' in archive:
    config['archive']['threshold'] = timedelta(int(archive['threshold']))
if 'auth' in server:
    config['auth-endpoint'] = server['auth']
if 'host' in discourse:
    config['discourse']['host'] = discourse['host']
if 'username' in discourse:
    config['discourse']['username'] = discourse['username']
if 'api-key' in discourse:
    config['discourse']['api-key'] = discourse['api-key']
