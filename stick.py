#!/bin/env python
import discord
import asyncio
import logging
import os
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
        response = 'Sorry bottu-chan is being reworked into a Sticky-bot, I can\'t hande commands yet :\('
        ans = await client.send_message(message.channel, response)
        logging.info(message.author.name + ': ' + message.content + ' response: ' + response)

client.run(os.environ['DISCORD_TOKEN'])
