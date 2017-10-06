#!/bin/env python3
import discord
import asyncio
import logging
import os
from commands import BotCommands as cmd
from os.path import join, dirname
from dotenv import load_dotenv

logging.basicConfig(filename='bot.log', level=logging.INFO, format='[%(asctime)s]%(levelname)s: %(message)s')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!'):
        message_command, *message_contents = message.content.split()

        message_handlers = {
            "!help": cmd.help_message,
            "!activiteit": cmd.get_activity,
            "!activiteiten": cmd.list_activities,
            "!addquote": cmd.add_quote,
            "!quote": cmd.print_quote
        }

        if message_command not in message_handlers:
            return

        response = await message_handlers[message_command](message_contents, message)

        if not response:
            await client.send_message(message.channel,
                                      "Invalid use of command, or you are not authorized to use this command.")

        if type(response) == discord.Embed:
            await client.send_message(message.channel, embed=response)
        else:
            await client.send_message(message.channel, response)

if __name__ == '__main__':
    client.run(os.environ['DISCORD_TOKEN'])
