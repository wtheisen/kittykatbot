#!/usr/bin/env python2.7

import random

NAME    = 'catjoke'
ENABLE  = True
PATTERN = '^\$catjoke (?P<target>[^\s]*)'

RESPONSES = (
  "what do you call a cat in a station wagon? a car-pet!",
  "what's the unluckiest kind of cat to have? a cat-astrophe!",
  "what do you call a cat that's getting old? a grand-paw!",
  "why did the cat have troble watching a movie? it was on paws!",
  "what's a french cat's favorite dessert? chocolate mou(s)se!",
  "why don't cats play poker in the jungle? too many cheetas!",
  "what do you call a cat that was caught by the cops? a purrpetrator!" ,
  "what do cats eat for breakfast? mice krispies!",
  "why did the cat run from the tree? it was afraid of the bark!",
  "how do cats end a fight? they hiss and make up!",
  "did you hear about the cat that drank 5 bowls of water? she set a new lap record!",
  "why is it so hard for a leopard to hide? he's always spotted!"
)
def command(bot, nick, message, channel, target=None):
  response = "{}, {}".format(target, random.choice(RESPONSES))
  bot.send(channel, nick, response)

def register(bot):
  return ((PATTERN, command),)
