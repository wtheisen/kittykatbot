#!/usr/bin/env python2.7

import os
import random
import sys
import yaml

from irc import IRC

'''
todo: $motivation or $pickmeup
'''

def parse_yaml(filename):
  with open(filename, 'r') as stream:
    return dict(yaml.load(stream))

def handle_message(text):
  try:
    msg_info = text[1:].split()
    user = msg_info[0].split("!")[0]
    channel = msg_info[2] if msg_info[2] != "kittykatbot" else user
    message = ":".join(text[1:].split(":")[1:])
  except:
    return

  handle_keywords(user, message, channel)
  
  if message[0] == "$":
    handle_commands(user, message[1:], channel, sayings)

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

  if command == "whois":
    name = args[0]
    flag = filter(lambda x: x[0] == '-', args)

    if name not in sayings:
      irc.send(channel, "I just haven't met them yet")
      return

    if "-a" in flag:
      to_send = ["{}, {}".format(name, s) for s in sayings[name]]
      for msg in to_send:
        irc.send(channel, msg)
    else:
      index = random.randrange(len(sayings[name]))
      irc.send(channel, "{}, {}".format(name, sayings[name][index]))

  if command == "motivation":
    name = args[0] if len(args) else user
    index = random.randrange(len(sayings[command]))
    irc.send(channel, "{}, {}".format(name, sayings[command][index]))
    

if __name__ == "__main__":
  channel = "#ndlug"
  server = "irc.snoonet.org"
  nick = "kittykatbot"

  irc = IRC()
  irc.connect(server, channel, nick)

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
      handle_message(text) 
