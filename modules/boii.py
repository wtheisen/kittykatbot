#!/usr/bin/env python3

import random

NAME    = 'boii'
ENABLE  = True
PATTERN = '^\$boii (?P<target>[^\s]*)'

RESPONSES = (
  "{} boii's {}",
  "{} AGGRESSIVELY boii's {}",
  "{} boii's {} while laughing",
  "{} boii's {} with a glare"
)

def command(bot, nick, message, channel, target=None):
  source = nick if target != nick else "kittykatbot"
  response = random.choice(RESPONSES).format(source, target)
  bot.send(channel, nick, response)

def register(bot):
  return ((PATTERN, command),)
