#!/usr/bin/env python2.7

import os, sys
from irc import IRC

def handle_message(text):
  if not text:
    return
  text = text.lower()
  try:
    user_channel, msg = text[1:].split(":")
    user = user_channel.split("!")[0]
  except:
    user = ""

  for word in ["bork", "sbrk", "fark", "womp"]:
    if word in text:
      irc.send(channel, "{} {}".format(word, word))

  if "hot" in text and "hott" not in text:
    irc.send(channel, "s/hot/hott/")

  if "deprecat" in text and user != "trogdorthedagron":
    irc.send(channel, "we do not self.deprecate() here friends")

if __name__ == "__main__":
  channel = "#ndlug"
  server = "irc.snoonet.org"
  nick = "kittykatbot"

  irc = IRC()
  irc.connect(server, channel, nick)

  text = irc.recieve()

  while text.find("MODE") == -1: 
    text = irc.recieve()

  irc.join(channel)
  irc.send("trogdorthedagron", "i work")

  while True:
    text = irc.recieve()

    if text:
      print text.strip()

    if "PRIVMSG" in text and channel in text:
      handle_message(text) 
