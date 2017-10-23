'''
Provides some help talking to the xkcds API
'''

import random
import discord
import aiohttp

async def get_recent():
    ''' Get and parse the most recent xkcd comic. '''
    async with aiohttp.get('https://xkcd.com/info.0.json') as r:
        return await r.json()

async def get_by_id(comic_id):
    ''' Get and parse an xkcd comic based on the comic id. '''
    async with aiohttp.get(f'https://xkcd.com/{comic_id}/info.0.json') as r:
        if r.status == 404:
            return await get_recent()
        return await r.json()

async def get_random():
    ''' Get and parse a random xkcd comic. '''
    latest = await get_recent()
    max_id = latest['num']
    rnd = random.randint(1, max_id)
    if rnd == 404:
        return await get_random()
    return await get_by_id(rnd)


async def print_comic(comic):
    ''' Format an xkcd comic to be displayed in an Embed. '''
    embed = discord.Embed(color=discord.Colour(0xffffff))
    embed.title = comic['safe_title']

    embed.set_image(url=comic['img'])

    return embed
