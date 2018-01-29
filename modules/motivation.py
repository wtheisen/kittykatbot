#!/usr/bin/env python2.7

import random

NAME    = 'motivation'
ENABLE  = True
PATTERN = '^\$motivation (?P<target>[^\s]*)'

RESPONSES = (
  "you can do it!",
  "what a wonderful human being you are",
  "take a deep breath",
  "you are smart and more than capable",
  "don't worry, be happy",
  "i believe in you",
  "<3 <3 <3 <3 <3 <3 <3",
  "life won't always be easy, but it will always be worth it",
  "i love you, i hope that counts for something"
)

def command(bot, nick, message, channel, target=None):
  response = "{}, {}".format(target, random.choice(RESPONSES))
  bot.send(channel, nick, response)

def register(bot):
 return ((PATTERN, command),)
