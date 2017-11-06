import argparse
import workerbee
import getpass

parser = argparse.ArgumentParser(description='Manage HoneyComb')
parser.add_argument('--username', required=True, help='Username')
parser.add_argument('--debug', required=False, help='Debug', action='store_true')
parser.add_argument('--device', required=True, help='Device list, comma delimited')
parser.add_argument('--attribute', required=False, help='Attribute, eg temperature', default='temperature')
parser.add_argument('--filename', required=True, help='Filename')
options = parser.parse_args()

hc = workerbee.workerbee(options.debug, options.username)

hc.login()
hc.nodes()
hc.graphNodeAttribute(options.device.split(','), options.attribute, options.filename)
hc.logout()
