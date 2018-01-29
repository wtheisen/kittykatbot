#!/usr/bin/env python2.7

import random
import yaml

NAME    = 'whois'
ENABLE  = True
PATTERN = '^\$whois (?P<target>[^\s]*)[\s\t]*(?P<flag>[^\s]*)'

RESPONSES = yaml.load(open('whois.yaml', 'r'))

def command(bot, nick, message, channel, target=None, flag=None):
  if target not in RESPONSES:
    bot.send(channel, nick, RESPONSES['unknown'].format(target))
    return

  if flag == '-a':
    for line in RESPONSES[target]:
      bot.send(channel, nick, "{}, {}".format(target, line))
    return
    
  response = "{}, {}".format(target, random.choice(RESPONSES[target]))
  bot.send(channel, nick, response)

def register(bot):
  return ((PATTERN, command),)
