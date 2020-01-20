from configparser import ConfigParser
from datetime import timedelta
from args import args

# Defaults
config = {
        'account': None,
        'api-host': 'https://api.wildapricot.org',
        'secret': None,
        'archive': {
            'levels': [],
            'threshold': timedelta(60)},
        'auto-approve': {
            'search_name': None},
        'application_stale': {
            'timeout': timedelta(60)},
        'auth-endpoint': 'https://oauth.wildapricot.org/auth/token',
        'cancel': {
            'id': None},
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
auto_approve = parser['auto-approve'] if 'auto-approve' in parser else {}
application_stale = parser['application_stale'] if 'application_stale' in parser else {}
cancel = parser['cancel'] if 'cancel' in parser else {}

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

#auto_approve
if 'search_name' in auto_approve:
    config['auto-approve']['search_name'] = auto_approve['search_name']

# application_stale
if 'timeout' in application_stale:
    config['application_stale']['timeout'] = timedelta(int(application_stale['timeout']))

if 'auth' in server:
    config['auth-endpoint'] = server['auth']

if 'id' in cancel:
    config['cancel']['id'] = cancel['id']

## Discourse 
if 'host' in discourse:
    config['discourse']['host'] = discourse['host']

if 'username' in discourse:
    config['discourse']['username'] = discourse['username']

if 'api-key' in discourse:
    config['discourse']['api-key'] = discourse['api-key']

if 'debug' in options:
    config['options']['debug'] = options['debug']

