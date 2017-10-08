# Sticky-discord

To run an instance of this bot:

1. Clone this repository:

run `git clone git@github.com:RobinSikkens/Sticky-bot`

2. Create a virtualenv:

run `python3.6 -m venv virtualenv`

3. Activate the virtualenv:

run `source virtualenv/bin/activate`

4. Install package and dependencies:

run `python setup.py install` or `python setup.py develop`

5. Make an env file

make file `.env` containing token `DISCORD_TOKEN=` and optionally `STICKORD_LOGLEVEL=`

5. Start the bot with the virtualenv active:

run `python -m stickord.bot`
