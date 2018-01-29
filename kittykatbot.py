#!/usr/bin/env python2.7

import glob
import re
import socket
import sys
import yaml

PING_RE     = re.compile(r'^PING (?P<payload>.*)')
CHANMSG_RE  = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+(?P<channel>#+[-\w]+)\s+:(?P<message>[^\n\r]+)')
PRIVMSG_RE  = re.compile(r':(?P<nick>.*?)!\S+\s+?PRIVMSG\s+[^#][^:]+:(?P<message>[^\n\r]+)')


class KittyKatBot:
  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.modules_dir = "modules"
    self.commands = []
    self.modules = {}

    channels, servers, nicks, botmaster = self.parse_config("config.yaml")

    self.handlers    = [
      (PING_RE    , self.handle_ping),
      (CHANMSG_RE , self.handle_message),
      (PRIVMSG_RE , self.handle_message)
    ]

    for server, channel in zip(servers, channels):
      self.connect(server, channel, "kittykatbot")

    self.load_modules()

    while True:
      self.recieve()


  def load_modules(self):
    modules = {}
    commands = []

    for module_path in glob.glob('{}/*.py'.format(self.modules_dir)):
      module_name = module_path.split('.')[0].replace('/', '.')

      if '__' in module_name:
        continue

      if module_name in self.modules:
        module = self.modules[module_name]
        reload(module)
      else:
        module = __import__(module_name, globals(), locals(), -1)

      if module.ENABLE:
        modules[module_name] = module
        commands.extend(module.register(self))

    self.commands = [(re.compile(p), c) for p, c in commands]
    self.modules = modules


  def parse_config(self, filename):
    try:
      config = dict(yaml.load(open('config.yaml', 'r')))
    except:
      print('Error parsing {}'.format(filename))
      exit(1)
    
    is_error = False
    for keyword in ['channels', 'server', 'nick']:
      if keyword not in config:
        is_error = True
        print "please include '{}' in your config file"
  
    if '-test' in sys.argv and 'test' not in config:
      is_error = True
      print "please include a testing channel if you want to test"
  
    if is_error:
      print "exiting..."
      exit(1)

    channels = config['channels']
    args = sys.argv[1:]
    while len(args) and args[0].startswith('-') and len(args[0]) > 1:
      arg = args.pop(0)

      if arg == '-test':
        channels = config['test']

    servers = config['server']
    nicks = config['nick']
    botmaster = config['botmaster']

    return channels, servers, nicks, botmaster


  def handle_ping(self, payload):
    self.socket.send("PONG {}\n".format(payload))


  def handle_message(self, nick, message, channel=None):
    for pattern, callback in self.commands:
      match = pattern.match(message)
      if match:
        callback(self, nick, message, channel, **match.groupdict())


  def send(self, channel, nick, response):
    recipient = channel if channel else nick
    self.socket.send('PRIVMSG {} {}\n'.format(recipient, response))


  def connect(self, server, channel, nick):
    print "connecting to {}".format(server)

    self.socket.connect((server, 6667))
    self.socket.send("USER {} {} {} {}\n".format(*4*[nick]))
    self.socket.send("NICK {}\n".format(nick))

    message = self.recieve()
    while 'MODE' not in message:
      message = self.recieve()

    self.join(channel)


  def join(self, channel):
    print "joining {}".format(channel)
    print self.socket.send("JOIN {}\n".format(channel))

  def recieve(self):
    message = self.socket.recv(2040)

    for pattern, handler in self.handlers:
      match = pattern.match(message)
      if match:
        handler(**match.groupdict())

    return message

if __name__ == '__main__':
  bot = KittyKatBot()
