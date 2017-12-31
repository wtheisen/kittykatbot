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


def handle_message(irc, text):
  try:
    msg_info = text[1:].split()
    user = msg_info[0].split("!")[0]
    channel = msg_info[2] if msg_info[2] != "kittykatbot" else user
    message = ":".join(text[1:].split(":")[1:]).strip()
  except:
    return

  handle_keywords(user, message, channel)
  
  if message.startswith('$'):
    if message.startswith('$whois'):
      handle_whois(irc, channel, message)

    else:
      handle_commands(user, message[1:], channel)

def handle_whois(irc, channel, text):
  whois = parse_yaml("whois.yaml")
  args = text.split()
  command = args.pop(0)

  # handle name redirection
  name = args[0]
  if name in whois and whois[name][0] in whois:
    key = whois[name][0]
  else:
    key = name

  flag = filter(lambda x: x[0] == '-', args)

  if key not in whois:
    irc.send(channel, "I just haven't met them yet")
    return

  if "-a" in flag:
    to_send = ["{}, {}".format(name, s) for s in whois[key]]
    for msg in to_send:
      irc.send(channel, msg)
  else:
    index = random.randrange(len(whois[key]))
    irc.send(channel, "{}, {}".format(name, whois[key][index]))

def handle_keywords(user, text, channel):
  text = text.lower()
  keywords = ["bork", "sbrk", "fark", "womp"]

  for word in keywords:
    if word in text:
      irc.send(channel, "{} {}".format(word, word))

  if "hot" in text and "hott" not in text and user != "gonzobot":
    irc.send(channel, "s/hot/hott/")

  if "deprecat" in text:
    irc.send(channel, "we do not self.deprecate() here friends")

  if "herp" in text and "derp" not in text:
    irc.send(channel, "derp")

  if "derp" in text and "herp" not in text:
    irc.send(channel, "herp derp")

def handle_commands(user, text, channel):
  commands = parse_yaml("commands.yaml")
  args = text.split()
  command = args.pop(0)

  if command == "motivation" or command == "catjoke":
    name = args[0] if len(args) else user
    index = random.randrange(len(commands[command]))
    irc.send(channel, "{}, {}".format(name, commands[command][index]))

  if command in ["claw", "cuddle"]:
    target = args[0] if len(args) else user
    source = user if len(args) else "kittykatbot"
    index = random.randrange(len(commands[command]))

    irc.send(channel, commands[command][index].format(source, target))

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

  while True:
    text = irc.recieve()

    if text:
      print text.strip()

    if "PRIVMSG" in text:
      handle_message(irc, text) 
