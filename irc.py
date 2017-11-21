#!/usr/bin/env python2.7

import socket

class IRC:
  def __init__(self):
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def send(self, chan, msg):
    self.irc.send("PRIVMSG {} {}\n".format(chan, msg))

  def connect(self, server, channel, nick):
    print "connecting to {}".format(server)

    self.irc.connect((server, 6667))
    self.irc.send("USER {} {} {} {}\n".format(nick, nick, nick, nick))
    print self.irc.send("NICK {}\n".format(nick))
    

  def join(self, channel):
    print "joining {}".format(channel)
    print self.irc.send("JOIN {}\n".format(channel))

  def recieve(self):
    msg = self.irc.recv(2040)

    if msg.find("PING") != -1:
      self.irc.send("PONG {}\n".format(msg.split()[1]))

    return msg
