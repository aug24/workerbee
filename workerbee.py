import requests
import getpass
import sys
import json
import os
from urlparse import urlparse
import plotly.plotly as py
import plotly.graph_objs as go
import time
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import table
import numpy as np

def time_millis_ago (ms): return lambda: int(round(time.time() * 1000) - int(ms))
current_time_millis = time_millis_ago(0)
yesterday_millis = time_millis_ago(24 * 60 * 60 * 1000)
one_hour_ago_millis = time_millis_ago(60 * 60 * 1000)

class workerbee:

  def __init__(self, debug, username=None):
    self.clientName='workerbee'
    self.username=username
    self.loggedin=False
    self.honeycomb='https://api-prod.bgchprod.info:8443/'
    self.userInfo=None
    self.nodeInfo=None
    self.eventInfo=None
    self.channelInfo=None
    try:
      self.password=os.environ['WORKERBEE_PASSWORD'] 
    except KeyError:
      self.password=None
    self.headers = {}
    self.debug_flag = debug

  def getUsername(self):
    return self.username

  def getPassword(self):
    return self.password

  def debug(self, message):
    if (self.debug_flag):
      print message

  def login(self, username=None, password=None):
    if username: 
      self.username==username
    if password: 
      self.password==password
    if self.password==None:
      self.password=getpass.getpass()

    data = {u"username": self.username, u"password": self.password, u"caller": u"workerbee"}
    response = requests.post(self.honeycomb + 'api/login', params=data)
    if response.status_code!=200:
      print "Failed to log in; got return code " + str(response.status_code)
      return False
    else:
      print "Logged in; got return code " + str(response.status_code)
      self.userInfo=response.json()
      self.headers['X-Omnia-Access-Token']=str(self.userInfo['ApiSession'])
      self.headers['Accept']='application/vnd.alertme.zoo-6.4+json'
      self.headers['X-AlertMe-Client']=self.clientName
      self.debug("Logged on")
      return True

  def logout(self):
    if self.userInfo==None:
      return
    response = self.post('api/logout', None)
    if response.status_code!=204:
      print "Failed to log off; got return code " + str(response.status_code)
      print response.text
      sys.exit(1)
    self.userInfo==None
    self.headers = {}
    self.debug("Logged off")

  def events(self):
    if self.userInfo==None:
      return
    if self.eventInfo:
      return self.eventInfo

    response = self.get('omnia/events', None)
    self.eventInfo=response.json()
    print self.eventInfo

    self.eventInfo['eventsDict']={}
    for event in self.eventInfo['events']:
      self.eventInfo['eventsDict'][event['name']]=event
    return self.eventInfo

  def channels(self):
    if self.userInfo==None:
      return
    if self.channelInfo:
      return self.channelInfo

    response = self.get('omnia/channels', None)
    self.channelInfo=response.json()
    print self.channelInfo

    self.channelInfo['channelsDict']={}
    for channel in self.channelInfo['channels']:
      self.channelInfo['channelsDict'][channel['id']]=channel
    return self.channelInfo

  def nodes(self):
    if self.userInfo==None:
      return
    if self.nodeInfo:
      return self.nodeInfo

    response = self.get('omnia/nodes', None)
    self.nodeInfo=response.json()
    #for node in self.nodeInfo:
    #self.nodeMap=response.json()

    self.nodeInfo['nodesDict']={}
    for node in self.nodeInfo['nodes']:
      self.nodeInfo['nodesDict'][node['name']]=node
    return self.nodeInfo

  def get(self, address, data):
    headers = {'X-Omnia-Access-Token': str(self.userInfo['ApiSession'])}
    return requests.get(self.honeycomb + address, headers=self.headers, params=data)

  def post(self, address, data):
    return requests.post(self.honeycomb + address, headers=self.headers, params=data)

  def getNode(self, name):
    for node in self.nodeInfo["nodes"]: 
      if node["name"] == name:
        return node
    print "No such node as " + name
    sys.exit(1)

  def showNodes(self):
    nodes=[]
    for node in self.nodeInfo["nodes"]: 
      nodes.append(node)
    print json.dumps(nodes, indent=4, sort_keys=True)

  def showNode(self, nodeName):
    for node in self.nodeInfo["nodes"]: 
      if node['name'] == nodeName:
        print json.dumps(node, indent=4, sort_keys=True)

  def showNodeAttributes(self, name):
    for node in self.nodeInfo["nodes"]: 
      if node["name"] == name:
        print json.dumps(node['attributes'], indent=4, sort_keys=True)

  def showLiveNodeAttribute(self, name, attribute):
    for node in self.nodeInfo["nodes"]: 
      if node["name"] == name:
        attributes=node['attributes']
        if attribute in attributes:
           print json.dumps(node['attributes'][attribute], indent=4, sort_keys=True)
        else:
           print "Device '" + name + "' does not include live '" + attribute + "' data"

  def showNodeAttribute(self, names, attribute, start=None, end=None):
    results={}
    for name in names:
      results[name]=self.getNodeAttribute(name, attribute, start, end)
    print json.dumps(results)

  def getNodeAttribute(self, name, attribute, start=None, end=None):
    node=self.getNode(name)
    deviceId=node["href"].split('/')[-1]
    url="omnia/channels/" + attribute + "%40" + deviceId
    options = {
      "start": yesterday_millis(),
      "end": current_time_millis(),
      "timeUnit": "MILLISECONDS", 
      "rate": "60",
      "operation": "AVG",
      "interval": "120000"
    }
    data=self.get(url, options).json()
    if not 'channels' in data.keys():
      print "Device '" + name + "' does not include '" + attribute + "' data"
      print data
      sys.exit(1)
    values=data['channels'][0]['values']
    return values

  def graphNodeAttribute(self, names, attribute, filename, start=None, end=None):
    plt.clf()
    xdata=[]
    ydata=[]
    for name in names:
      values=self.getNodeAttribute(name, attribute, start, end)
      list_of_lists = []
      for value in sorted(values.iterkeys()):
        list_of_lists += [[int(value), values[value]]]
      df = pd.DataFrame(list_of_lists, columns=['timestamp',name])
      df['timestamp_dt'] = pd.to_datetime(df.timestamp, unit='ms')
      df.set_index('timestamp_dt')[name].plot()
    plt.xlabel("Date/Time")
    plt.ylabel(attribute.capitalize())
    legend=plt.legend(loc='center right', bbox_to_anchor=(1.5, 0.5))
    plt.savefig(filename, bbox_extra_artists=(legend,), bbox_inches='tight')
    print "Saved to '" + filename + "'"


