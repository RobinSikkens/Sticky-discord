'''
Provides general helpers for getting activities.
'''
import json

import discord
import dateutil.parser as dateparser
import requests


async def get_activities():
    ''' Get and parse activities list. '''
    response = requests.get('https://koala.svsticky.nl/api/activities')
    return json.loads(response.text)

async def print_activity(act):
    ''' Format an activity into an Embed. '''
    embed = discord.Embed(color=discord.Colour(0xce2029))
    embed.title = act['name']

    start = dateparser.parse(act['start_date'])
    end = dateparser.parse(act['end_date'])

    prts = act.get('participant_counter', '')

    wanneer = duration(start, end)

    embed.add_field(name='Locatie', value=act['location'])

    if prts:
        embed.add_field(name='Inschrijvingen', value=prts)

    embed.add_field(name='Wanneer', value=wanneer)

    embed.set_image(url=act['poster'])

    return embed

def duration(start, end):
    ''' Print a duration in a readable way. '''
    sdate = start.date()
    edate = end.date()
    stime = start.time().strftime('%H:%M')
    etime = end.time().strftime('%H:%M')

    if start.date() != end.date():
        return f'{sdate} {stime} - {edate} {etime}'

    return f'{sdate} {stime} - {etime}'
