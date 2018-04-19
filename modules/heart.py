#!/usr/bin/env python3

import random

NAME    = 'heart'
ENABLE  = True
PATTERN = '^\$heart (?P<target>[^\s]*)'

RESPONSES = (
  "{} hearts {} with a smile",
  "{} shyly hearts {}",
  "{} hearts {} for the whole irc channel to see",
  "{} will always heart {}"
)

def command(bot, nick, message, channel, target=None):
  source = nick if target != nick else "kittykatbot"
  response = random.choice(RESPONSES).format(source, target)
  bot.send(channel, nick, response)

def register(bot):
  return ((PATTERN, command),)
