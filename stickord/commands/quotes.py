'''
Provides commands related to quotes.
'''
import os
import pickle
import random

import discord

from stickord.registry import Command, role_whitelist
from stickord.helpers.logging import get_easy_logger


QUOTEFILE = 'quote_file.pk1'
LOGGER = get_easy_logger('quotes')


@Command(['addquote', 'aq'], category='Quotes')
async def add_quote(cont, *_args, **_kwargs):
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
async def print_quote(cont, *_args, **_kwargs):
    ''' Print a random quote. '''
    if not os.path.isfile(QUOTEFILE):
        return 'No quotes saved.'

    with open(QUOTEFILE, 'rb') as qfile:
        quote_list = pickle.load(qfile)
        LOGGER.debug('Quotelist: %s', quote_list)
        # If the list is empty (due to a possible delete) move on.
        if not quote_list:
            LOGGER.debug('Empty quotelist found, aborting...')
            return 'No quotes saved.'

        if not cont:
            quote = random.choice(quote_list)
        else:
            query = ' '.join(cont).lower()
            quote = discord.utils.find(
                lambda s: query in s.lower(), quote_list
            )

        return quote


@Command(['deletequote', 'delquote'], category='Quotes')
@role_whitelist(['Admin', 'Moderator'])
async def delete_quote(cont, *_args, **_kwargs):
    '''Deletes the specified quote from the quotelist. Entire quote has to match. (Moderator only)'''
    if not os.path.isfile(QUOTEFILE):
        return 'No quotes to delete.'

    remove_string = ' '.join(cont)

    with open(QUOTEFILE, 'rb') as qfile:
        quote_list = pickle.load(qfile)

    if remove_string in quote_list:
        quote_list.remove(remove_string)
    else:
        return 'No such quote on file.'

    with open(QUOTEFILE, 'wb') as qfile:
        pickle.dump(quote_list, qfile)

    return f'Deleted: {remove_string} from the quote list'
