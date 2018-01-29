#!/usr/bin/env python2.7

import random

NAME    = 'deprecate'
ENABLE  = True
PATTERN = '(.*deprecat.*)'
IGNORE  = ('gonzobot', 'kittykatbot')

def command(bot, nick, message, channel, target=None):
  if nick == "gonzobot" or nick == "kittykatbot":
    return

  bot.send(channel, nick, '{}: we do not self.deprecate here'.format(nick))

def register(bot):
 return ((PATTERN, command),)
