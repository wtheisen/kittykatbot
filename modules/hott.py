#!/usr/bin/env python3

import random

NAME    = 'hott'
ENABLE  = True
PATTERN = '(.*hot[^t].*)'
IGNORE  = ('gonzobot', 'kittykatbot')

def command(bot, nick, message, channel, target=None):
  if nick == "gonzobot" or nick == "kittykatbot":
    return

  bot.send(channel, nick, 's/hot/hott')

def register(bot):
 return ((PATTERN, command),)
