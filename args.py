from argparse import ArgumentParser

parser = ArgumentParser(
        description = 'Client for interacting with the Wild Apricot admin API.')
parser.add_argument(
        '-k',
        '--key',
        help = "API key, generated in Settings -> Security -> Authorized applications",
        metavar = "API key"
        )
parser.add_argument(
        '-a',
        '--account',
        help = 'Wild Apricot account ID',
        metavar = '<id>',
        type = int)
parser.add_argument(
        '-c',
        '--config',
        help = 'Path to configuration file',
        metavar = '<file>')
parser.add_argument(
        '-o',
        action = 'append',
        dest = 'operations',
        help = 'The operation to perform. Can be specified multiple times.',
        metavar = ('<operation>', '<argument>'),
        nargs = '+',
        required = True)

args = parser.parse_args()
