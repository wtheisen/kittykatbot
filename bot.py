#!/usr/bin/env python2.7

import os
import random
import sys
import yaml

from irc import IRC

def parse_yaml(filename):
  try:
    with open(filename, 'r') as stream:
      return dict(yaml.load(stream))
  except:
    return {}

def parse_config(config):
  # error checking
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

  # parse command line args
  channels = config['channels']
  args = sys.argv[1:]
  while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    
    if arg == '-test':
      channels = config['test']

  servers = config['server']
  nicks = config['nick']

  return channels, servers, nicks


def handle_message(irc, text, sayings):
  try:
    msg_info = text[1:].split()
    user = msg_info[0].split("!")[0]
    channel = msg_info[2] if msg_info[2] != "kittykatbot" else user
    message = ":".join(text[1:].split(":")[1:])
  except:
    return

  handle_keywords(user, message, channel)
  
  if message.startswith('$'):
    if message.startswith('$whois'):
      handle_whois(irc, channel, message, sayings)

    else:
      handle_commands(user, message[1:], channel, sayings)

def handle_whois(irc, channel, text, sayings):
  args = text.split()
  command = args.pop(0)

  # handle name redirection
  name = args[0]
  if name in sayings and sayings[name][0] in sayings:
    key = sayings[name][0]
  else:
    key = name

  flag = filter(lambda x: x[0] == '-', args)

  if key not in sayings:
    irc.send(channel, "I just haven't met them yet")
    return

  if "-a" in flag:
    to_send = ["{}, {}".format(name, s) for s in sayings[key]]
    for msg in to_send:
      irc.send(channel, msg)
  else:
    index = random.randrange(len(sayings[key]))
    irc.send(channel, "{}, {}".format(name, sayings[key][index]))

def handle_keywords(user, text, channel):
  keywords = ["bork", "sbrk", "fark", "womp"]

  for word in keywords:
    if word in text.lower():
      irc.send(channel, "{} {}".format(word, word))

  if "hot" in text and "hott" not in text and user != "gonzobot":
    irc.send(channel, "s/hot/hott/")

  if "deprecat" in text and user != "trogdorthedagron":
    irc.send(channel, "we do not self.deprecate() here friends")

def handle_commands(user, text, channel, sayings):
  args = text.split()
  command = args.pop(0)

  if command == "motivation" or command == "catjoke":
    name = args[0] if len(args) else user
    index = random.randrange(len(sayings[command]))
    irc.send(channel, "{}, {}".format(name, sayings[command][index]))

  if command == "claw":
    target = args[0] if len(args) else user
    source = user if len(args) else "kittykatbot"
    index = random.randrange(len(sayings[command]))

    irc.send(channel, sayings[command][index].format(source, target))

if __name__ == "__main__":
  config = parse_yaml('config.yaml')
  channels, servers, nicks = parse_config(config)

  irc = IRC()
  for i, channel in enumerate(channels):
    irc.connect(servers[i], channels[i], nicks[i])

    text = irc.recieve()

    while text.find("MODE") == -1: 
      text = irc.recieve()

    irc.join(channel)

  irc.send("trogdorthedagron", "is this thing on")
  sayings = parse_yaml("whois.yaml")

  while True:
    text = irc.recieve()

    if text:
      print text.strip()

    if "PRIVMSG" in text:
      handle_message(irc, text, sayings) 
