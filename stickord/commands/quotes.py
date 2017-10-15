'''
Provides commands related to quotes.
'''
import pickle
import random
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from stickord.registry import Command, role_whitelist
from stickord.helpers.logging import get_easy_logger
from stickord.helpers.emoji import Emoji


QUOTEFILE = 'quote_file.pk1'
LOGGER = get_easy_logger('quotes')
BASE = declarative_base()

class Quote(BASE):
    ''' Represents a quote in the database. '''
    __tablename__ = 'quotes'

    id = sa.Column(sa.Integer, primary_key=True) # pylint: disable=invalid-name
    content = sa.Column(sa.Text, nullable=False)
    submitter = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        ''' Represent as <Quote(id, content, submitter, created_at)>. '''
        return (
            f'<Quote({self.id}, {repr(self.content)}, {self.submittter},'
            f' {self.created_at})>')

@Command(['addquote', 'aq'], category='Quotes')
async def add_quote(cont, mesg, client, sessionmaker, *_args, **_kwargs):
    ''' Add a quote to the quotesfile. '''
    session = sessionmaker()
    quote = ' '.join(cont)

    save_quote(session, quote, mesg.author)

    session.commit()
    await client.add_reaction(mesg, Emoji.Floppy.value)
    return None

def save_quote(session, content, author):
    ''' Prepare a new quote to be saved in the database. '''
    quote = Quote(content=content, submitter=author.id)
    session.add(quote)

def random_quote(session, query=None) -> Quote:
    ''' Return a random quote matching the query. '''
    # https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
    dbq = session.query(Quote)

    if query:
        dbq = dbq.filter(Quote.content.like(f'%{query}%'))

    matching = dbq.count()
    if matching:
        offset = random.randrange(0, matching)
        return dbq[offset]

    return None

@Command(['quote', 'q'], category='Quotes')
async def print_quote(cont, _mesg, _c, sema, *_args, **_kwargs):
    ''' Print a random quote. '''
    session = sema()

    query = ' '.join(cont)
    quote = random_quote(session, query)

    if not quote:
        return "No quote found."

    return f'{quote.content} ({quote.id})'

    #if not os.path.isfile(QUOTEFILE):
        #return 'No quotes saved.'

    #with open(QUOTEFILE, 'rb') as qfile:
        #quote_list = pickle.load(qfile)
        #LOGGER.debug('Quotelist: %s', quote_list)
        ## If the list is empty (due to a possible delete) move on.
        #if not quote_list:
            #LOGGER.debug('Empty quotelist found, aborting...')
            #return 'No quotes saved.'

        #if not cont:
            #quote = random.choice(quote_list)
        #else:
            #query = ' '.join(cont).lower()
            #quote = discord.utils.find(
                #lambda s: query in s.lower(), quote_list
            #)

        #return quote

@Command(['deletequote', 'delquote'], category='Quotes')
@role_whitelist(['Admin', 'Moderator'])
async def delete_quote(cont, mesg, _c, sema, *_args, **_kwargs):
    '''Deletes the specified quote from the quotelist by id. (Moderator only)'''
    try:
        ids = [int(x) for x in cont]
    except ValueError as ex:
        return f'Invalid ID given, {ex}'

    LOGGER.info('%s removing quotes %s', mesg.author.mention, ids)

    session = sema()

    toremove = session.query(Quote).filter(Quote.id.in_(ids))
    removed = toremove.count()
    toremove.delete(False)

    session.commit()

    return f'Deleted {removed} from the quote list'

@Command(['migratequotes'], category='Quotes', hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def migrate_pickled_quotes(_cont, _mesg, client, sessionmaker, *_args,
                                 **_kwargs):
    ''' Migrate quotes stored in the quotefile to the database. '''
    session = sessionmaker()

    with open(QUOTEFILE, 'rb') as qfile:
        quote_list = pickle.load(qfile)
        LOGGER.debug('Quotelist: %s', quote_list)
        # If the list is empty (due to a possible delete) move on.
        if not quote_list:
            LOGGER.debug('Empty quotelist found, aborting...')
            return 'No quotes saved.'

    for quote in quote_list:
        save_quote(session, quote, client.user)

    session.commit()
    LOGGER.info('Migrated %s quotes.', len(quote_list))
    return 'Done!'
