'''
Provides main entry point for the bot and message handler.
'''
import logging
import os

import discord
from dotenv import load_dotenv

import stickord.commands
from stickord.helpers.logging import get_easy_logger
from stickord.registry import COMMAND_DICT, safe_call, CommandNotFoundError


CLIENT = discord.Client()
''' Main discord.py Client. '''
LOGGER = get_easy_logger('bot')

@CLIENT.event
async def on_ready():
    ''' Print logging info about bot. '''
    logging.info('Logged in as: %s (%s).',
                 CLIENT.user.name, CLIENT.user.id)

@CLIENT.event
async def on_message(message):
    ''' Handle incoming message. '''
    if message.content.startswith('!'):
        message_command, *message_contents = message.content.split()
        LOGGER.debug('Message: %s, %s', message_command, message_contents)

        response = None
        try:
            response = await safe_call(
                COMMAND_DICT, message_command[1:],
                message_contents, message
            )
        except CommandNotFoundError:
            LOGGER.debug('Command %s unknown.', message_command[1:])
            return

        if not response:
            await CLIENT.send_message(
                message.channel,
                'Invalid use of command, or you are not authorized to use'
                ' this command.'
            )
            return

        LOGGER.debug('Sending response %s', response)
        if isinstance(response, discord.Embed):
            await CLIENT.send_message(message.channel, embed=response)
        else:
            await CLIENT.send_message(message.channel, response)

def main():
    ''' Initialize and start the bot. '''
    # Load environment
    dotenv_path = os.path.join(
        os.path.dirname(__file__), '.env'
    )
    load_dotenv(dotenv_path)

    # Setup logging
    loglevel = os.environ.get('STICKORD_LOGLEVEL', 'INFO')
    logging.basicConfig(
        filename='bot.log',
        level=getattr(logging, loglevel),
        format='[%(asctime)s]%(name)s: %(levelname)s: %(message)s'
    )


    # Load commands
    stickord.commands.load_plugins()

    # Connect to discord
    CLIENT.run(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    main()
