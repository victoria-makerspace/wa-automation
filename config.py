class Config:
    from argparse import ArgumentParser
    from configparser import ConfigParser

    def __init__(self):
        # Parse command-line arguments
        parser = self.ArgumentParser()
        parser.add_argument('-c', '--config', required = True, help = 'Path to configuration file')
        parser.add_argument('-a', '--account', help = 'Wild Apricot account ID')
        args = parser.parse_args()

        # Read configuration file
        config = self.ConfigParser()
        config.read(args.config)
        self.auth_endpoint = config['server']['auth']
        self.api_host = config['server']['api']
        self.secret = config['client']['secret']
        self.account = None

        if args.account:
            self.account = args.account
        elif 'account-id' in config['client']:
            self.account = config['client']['account-id']
