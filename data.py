import argparse
import workerbee
import getpass

parser = argparse.ArgumentParser(description='Manage HoneyComb')
parser.add_argument('--username', required=True, help='Username')
parser.add_argument('--debug', required=False, help='Debug', action='store_true')
parser.add_argument('--device', required=True, help='Device list, comma delimited')
options = parser.parse_args()

hc = workerbee.workerbee(options.debug, options.username)

hc.login()
hc.nodes()
hc.showNodeAttribute(options.device.split(','), "temperature")
hc.logout()
