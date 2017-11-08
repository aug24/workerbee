import argparse
import workerbee
import getpass

parser = argparse.ArgumentParser(description='Manage HoneyComb')
parser.add_argument('--username', required=True, help='Username')
parser.add_argument('--debug', required=False, help='Debug', action='store_true')
parser.add_argument('--node', required=False, help='Show a specific node')
parser.add_argument('--list-attributes', required=False, help='Debug', action='store_true')
parser.add_argument('--attribute', required=False, help='Attribute, eg temperature', default='temperature')
options = parser.parse_args()

hc = workerbee.workerbee(options.debug, options.username)

hc.login()
hc.nodes()
if options.node == None:
   hc.showNodes()
else:
   if options.list_attributes:
       hc.showNodeAttributes(options.node)
   else:
       if options.attribute:
           hc.showLiveNodeAttribute(options.node, options.attribute)
       else:
           hc.showNode(options.node)
hc.logout()
