'''
Iedereen houdt van koekjes, in het echt en de vitruele variant.
'''
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from stickord.registry import Command, get_easy_logger, role_whitelist

Base = declarative_base() # pylint: disable=invalid-name
LOGGER = get_easy_logger('commands.koekjes')
KOEKTROMMEL = 40


class Koekje(Base)
    ''' Represent a single cookie '''
    __tablename__ = 'koekjes'

    id = sa.Column(sa.Integer, primary_key=True) # pylint: disable=invalid-name
    #save the new cookie count
    count = sa.Column(sa.Integer, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        ''' Represent as <Koekje(id, countm author, created_at)>. '''
        return (f'<Koekje({self.id}, {self.count}, {self.author},'
                f' {self.created_at})>')

@Command('koekje', category='Algemeen')
async def cookie(cont, mesg, client, sessionmaker, *_args, **_kwargs):
    ''' Gives the user a cookie. This cookie has no discernible function,
    representation or value. '''
    session = sessionmaker()
    koektrommel = session.query(Koekje).order_by(Koekje.created_at.desc()).first()

    if not koektrommel:
        LOGGER.info('No koektrommel yet, making one')
        resetkoekjes(session, client.user)
        count = KOEKTROMMEL
        author = client.user.id
        _when = datetime.utcnow()
    else:
        count, author, _when = (
            koektrommel.count,
            koektrommel.author,
            koektrommel.created_at
        )

    num = count - 1

    if num < 0:
        LOGGER.info(
            '%s (%s) tried to get a cookie but couldn\'t',
            mesg.author.mention, mesg.author.id
        )
        response = (f'Oh no! There\'s no cookie in the koektrommel'
                    f'have someone from @Bestuur refill it.')
    else:
        setkoekjes(session, num, mesg.author)
        await client.add_reaction(mesg, '\U0001f36a')
        response = (f'Enjoy your non-existing virtual goodness!')

    session.commit()
    return response

@Command(['vulkoekjes', 'koekjesbijvullen'], category='Algemeen')
@role_whitelist('Admin', 'Bestuur')
async def vultrommel(cont, msg, client, sessionmaker, *_args, **_kwargs):
    session = sessionmaker
    resetkoekjes(session, msg.author)
    return f'Geweldig {msg.author.mention} heeft de koektrommel bijgevuld!'


def resetkoekjes(session, author):
    ''' Reset koektrommel to 40. '''
    setkoekjes(session, KOEKTROMMEL , author)


def setkoekjes(session, count, author):
    LOGGER.debug(
        'Koektrommel set to %s cookies by %s (%s)',
        count, author.mention, author.id
    )

    author_id = author.id
    session.add(Koekje(
        count=count,
        author=author_id
    ))