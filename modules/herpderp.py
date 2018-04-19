#!/usr/bin/env python

import random

NAME    = 'herpderp'
ENABLE  = True
PATTERN = '^(?P<target>[hd]erp).*'
IGNORE  = ('gonzobot', 'kittykatbot')

def command(bot, nick, message, channel, target=None):
  if nick == "gonzobot" or nick == "kittykatbot":
    return

  response = 'derp' if 'derp' not in target else 'herp derp'
  bot.send(channel, nick, response)

def register(bot):
 return ((PATTERN, command),)
