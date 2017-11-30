## kittykatbot: a (very) simple IRC bot

kittykatbot supports the following commands:
* `motivation [user]`: provides a random sentence of motivation to the
  specified user.
* `claw [user]`: will provide a random sentence in which you 'claw' the user.
  kittykatbot is a cat, these things are totally normal.
* `catjoke [user]`: will provide a random cat joke to the user.

Note: For all of the above commands, `kittykatbot` will say the command at you
if no user is specified. All command strings are specified in `commands.yaml`.

If a `whois.yaml` file is provided:
* `whois <name> [-a]`: returns a random sentence (or all sentences if `-a`
  specified) about that user.
* My whois file is top sekrit, so you'll have to
  provide your own.

### Other random things that kittykatbot does:
* If someone says 'hot': kittykatbot will reply 's/hot/hott'. She's mature like
  that, you know?
* If someone uses the words 'deprecate' or 'deprecation': kittykatbot will shut
  that down. Comes from all my friends always saying they're not awesome when
  they are. kittykatbot is an motivational safe haven for all.

## How to use kittykatbot:
A sample `config.yaml` file (the one I use) is provided: necessary fields are
`channels`, `server`, and `nick`. Optionally, you can specify `test` and
`test_server` if you want to be test your bot by joining a different channel.

Run the bot by running `bot.py [-test]`. If `-test` is specified, only the
channels under `test` will be joined.
