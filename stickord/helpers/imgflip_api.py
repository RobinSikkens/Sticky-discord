'''
A helper class that talks to the imgflip API
'''

import json
import discord
import requests
import aiohttp
from stickord.registry import get_easy_logger

LOGGER = get_easy_logger('helpers.imgflip_api')

async def generate_meme(id, text_upper, text_bottom):
    ''' Generates a meme and returns the image link. '''
    url = 'https://api.imgflip.com/caption_image'
    params = {'username': 'imgflip_hubot',
              'password': 'imgflip_hubot',
              'template_id': id,
              'text0': text_upper,
              'text1' : text_bottom}
    async with aiohttp.post(url, params=params) as r:
        LOGGER.info('Doing imgflip POST request')
        return await r.json()


async def print_meme(meme):
    ''' Formats an imgflip response to be returned in an embed. '''
    embed = discord.Embed(color=discord.Color(0x666666))
    embed.set_image(url=meme['data']['url'])

    return embed
