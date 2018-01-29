#!/usr/bin/env python2.7

import random

NAME    = 'cuddle'
ENABLE  = True
PATTERN = '^\$cuddle (?P<target>[^\s]*)'

RESPONSES = (
  "{} jumps up into {}'s lap and falls asleep there",
  "{} sits at the feet of {} and meows, waits to be luffed",
  "{} finds a nice warm spot on {}'s keyboard and lays there",
  "{} sits right next to {} and purrs happily"
)

def command(bot, nick, message, channel, target=None):
  source = nick if target != nick else "kittykatbot"
  response = random.choice(RESPONSES).format(source, target)
  bot.send(channel, nick, response)

def register(bot):
  return ((PATTERN, command),)
