import argparse
import workerbee
import json
from bottle import route, run, template, get, post, request, static_file

parser = argparse.ArgumentParser(description='Manage HoneyComb')
parser.add_argument('--username', required=False, help='Username')
parser.add_argument('--debug', required=False, help='Debug', action='store_true')
options = parser.parse_args()

hc = workerbee.workerbee(options.debug, options.username)

@route('/')
def root():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" value="%s" />
            Password: <input name="password" type="password" value="%s" />
            <input value="Login" type="submit" />
        </form>
    ''' % (hc.getUsername(), hc.getPassword())

@route('/node/:nodename/attribute/:attribute/graph')
def graph(nodename, attribute):
    filename='node-%s-attribute-%s.png' % (nodename, attribute)
    print 'Creating file ' + filename
    hc.graphNodeAttribute([nodename], attribute, filename)
    return static_file(filename, root='.')

@route('/node/:nodename/attribute/:attribute')
def node(nodename, attribute):
    return 'Data: <code>' + json.dumps(hc.nodes()['nodesDict'][nodename]['attributes'][attribute], indent=2) + '</code><br/><a href="/node/' + nodename + '/attribute/' + attribute + '/graph">graph</a>'

@route('/node/:nodename')
def node(nodename):
    output='<ul>'
    attributes = hc.nodes()['nodesDict'][nodename]['attributes'].keys()
    attributes.sort()
    for attribute in attributes:
        output = output + '<li>' + '<a href="/node/' + nodename + '/attribute/' + attribute + '">' + attribute + '</a>' + '</li>'
    output = output + '</ul>'
    return output

@route('/nodes')
def nodes():
    output='<ul>'
    nodes = hc.nodes()['nodesDict'].keys()
    nodes.sort()
    for node in nodes:
        output = output + '<li>' + '<a href="node/' + node + '">' + node + '</a>' + '</li>'
    output = output + '</ul>'
    return output

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if hc.login(username, password):
        return '''
            <p>Your login information was correct.</p>
            <ul>
                <li><a href="/nodes">nodes</li>
                <li><a href="/logout">logout</li></ul>
        '''
    else:
        return '<p>Login failed.</p>'

@route('/logout')
def logout():
    hc.logout()

run(host='localhost', port=8080)
