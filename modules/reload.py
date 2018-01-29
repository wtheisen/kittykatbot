#!/usr/bin/env python2.7

import random

NAME    = 'reload'
ENABLE  = True
PATTERN = '^\$reload'

RESPONSES = (
  "hottest bott is BACK",
  "guess who's back, back again",
  "the party don't start 'till i walk in",
  "bot got back"
)

def command(bot, nick, message, channel, target=None):
  bot.load_modules()
  response = random.choice(RESPONSES)
  bot.send(channel, nick, response)


def register(bot):
  return ((PATTERN, command),)
