#!/usr/bin/env python2.7

import random

NAME    = 'claw'
ENABLE  = True
PATTERN = '^\$claw (?P<target>[^\s]*)'

RESPONSES = (
  "{} claws {} but feels guilty about it afterwards",
  "{} vengefully claws {}"                                          ,
  "{} thinks about clawing {}, but decides it's not worth the battle",
  "{} is beneath clawing {}"
)

def command(bot, nick, message, channel, target=None):
  source = nick if target != nick else "kittykatbot"
  response = random.choice(RESPONSES).format(source, target)
  bot.send(channel, nick, response)

def register(bot):
  return ((PATTERN, command),)
