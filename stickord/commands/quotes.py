'''
Provides commands related to quotes.
'''
import os
import pickle
import random

import discord

from stickord.registry import Command
from stickord.helpers.logging import get_easy_logger


QUOTEFILE = 'quote_file.pk1'
LOGGER = get_easy_logger('quotes')

@Command(['addquote', 'aq'], category='Quotes')
async def add_quote(cont, _):
    ''' Add a quote to the quotesfile. '''
    quote = ' '.join(cont)

    if not os.path.isfile(QUOTEFILE):
        quote_list = []

    else:
        with open(QUOTEFILE, 'rb') as qfile:
            quote_list = pickle.load(qfile)

    quote_list.append(quote)

    with open(QUOTEFILE, 'wb') as qfile:
        pickle.dump(quote_list, qfile)

    return 'Quote saved!'

@Command(['quote', 'q'], category='Quotes')
async def print_quote(cont, _):
    ''' Print a random quote. '''
    if not os.path.isfile(QUOTEFILE):
        return 'No quotes saved.'

    with open(QUOTEFILE, 'rb') as qfile:
        quote_list = pickle.load(qfile)
        LOGGER.debug('Quotelist: %s', quote_list)

        if not cont:
            quote = random.choice(quote_list)
        else:
            query = ' '.join(cont).lower()
            quote = discord.utils.find(
                lambda s: query in s.lower(), quote_list
            )

        return quote
