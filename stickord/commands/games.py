'''
Fun & Games
'''
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from stickord.registry import Command, get_easy_logger, channel_whitelist


Base = declarative_base() # pylint: disable=invalid-name
LOGGER = get_easy_logger('commands.games')

class Tel(Base):
    ''' Represents one count. '''
    __tablename__ = 'tellen'

    id = sa.Column(sa.Integer, primary_key=True) # pylint: disable=invalid-name
    count = sa.Column(sa.Integer, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        ''' Represent as <Tel(id, count, author, created_at)>. '''
        return (f'<Tel({self.id}, {self.count}, {self.author},'
                f' {self.created_at})>')

@Command(['tellen', 'tel'], category='Games')
@channel_whitelist(['botabuse', 'spam'])
async def counting(cont, mesg, client, sessionmaker, *_args, **_kwargs):
    ''' Allows  users to play the counting game. The command should be entered
    with the number exactly 1 higher than the last time the command was
    entered. Cannot submit a number twice in a row.'''
    session = sessionmaker()
    huidigetel = session.query(Tel).order_by(Tel.created_at.desc()).first()

    if not huidigetel:
        LOGGER.info('Creating first Tel')
        resettellen(session, client.user)
        count = 0
        auth = client.user.id
        _when = datetime.utcnow()
    else:
        count, auth, _when = (
            huidigetel.count,
            huidigetel.author,
            huidigetel.created_at
        )

    if cont:
        try:
            num = int(cont[0])
            nextnum = count + 1

            if num != nextnum:
                resettellen(session, mesg.author)
                LOGGER.info(
                    '%s (%s) messed up counting at %s',
                    mesg.author.mention, mesg.author.id, count
                )
                response = (f'Whoops, you done goof! You should have entered'
                            f' "{nextnum}" but you entered "{num}".')

            elif mesg.author.id == auth:
                response = f'You can\'t submit a number twice in a row! Shame on you {mesg.author.mention}!'
            else:
                settellen(session, nextnum, mesg.author)
                await client.add_reaction(mesg, '\U0001f44c')
                response = None

            session.commit()
            return response

        except ValueError:
            return 'Entered number was not valid.'

@Command(['toptel'], category='Games')
async def get_toptel(*args, **_kwargs):
    ''' Get the highscore of the counting game. '''
    sessionmaker = args[3]
    session = sessionmaker()

    toptel = session.query(Tel).order_by(Tel.count.desc()).first()

    return f'The highest count ever reached is {toptel.count}.'

def resettellen(session, author):
    ''' Reset counting to zero. '''
    settellen(session, 0, author)

def settellen(session, count, author):
    ''' Register new Tel. '''
    LOGGER.debug(
        'Counting game set to %s by %s (%s)',
        count, author.mention, author.id
    )

    author_id = author.id
    session.add(Tel(
        count=count,
        author=author_id
    ))
