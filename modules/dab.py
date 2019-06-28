#!/usr/bin/env python3

import random

NAME    = 'dab'
ENABLE  = True
PATTERN = '(.*dab[^t].*)'
IGNORE  = ('gonzobot', 'kittykatbot')

def command(bot, nick, message, channel, target=None):
  if nick == "gonzobot" or nick == "kittykatbot":
    return

  bot.send(channel, nick, '\_o\ /o_/')

def register(bot):
 return ((PATTERN, command),)
