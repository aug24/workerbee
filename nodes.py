import argparse
import workerbee
import getpass

parser = argparse.ArgumentParser(description='Manage HoneyComb')
parser.add_argument('--username', required=True, help='Username')
parser.add_argument('--debug', required=False, help='Debug', action='store_true')
options = parser.parse_args()

hc = workerbee.workerbee(options.username, options.debug)
hc.login()
hc.nodes()
hc.showNodes()
hc.logout()
