'''
Add the Amazing feature to co-write fictional or non-fictional epics.
'''
import os
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from stickord.registry import Command, get_easy_logger, role_whitelist, channel_whitelist

Base = declarative_base() # pylint: disable=invalid-name
LOGGER = get_easy_logger('commands.storywriting')


class StoryElement(Base):
    ''' Represents a story piece of 3 words. '''
    __tablename__ = 'stories'

    id = sa.Column(sa.Integer, primary_key=True) # pylint: disable=invalid-name
    story_string = sa.Column(sa.String, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    story_id = sa.Column(sa.Integer, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        ''' Represent as <StoryElement(id, story_string, author,
        story_id, created_at)>.'''
        return (f'<StoryElement({self.id}, {self.story_string}, {self.author},'
                f' {self.story_id}, {self.created_at})>')


@Command(['addstory', 'as'], category='Games')
@channel_whitelist(['storywriting'])
async def add_to_story(cont, mesg, client, sessionmaker, *_args, **_kwargs):
    ''' Adds the (first) three words to the currently active story. '''
    session = sessionmaker()
    curr_story = session.query(StoryElement)\
        .order_by(StoryElement.created_at.desc()).first()

    if not curr_story:
        LOGGER.info('No story yet, setting id to 0')
        curr_story_id = 0
    else:
        curr_story_id = curr_story.story_id

    if len(cont) < 3:
        LOGGER.info(
            '%s wanted to add to %s but did not submit 3 words',
            mesg.author.mention, curr_story_id
        )
        response = (f'Oh! Something went wrong, '
                    f'I could not find 3 words to add to the story')
    elif mesg.author.id == curr_story.author:
        response = (f'You can\'t submit words twice in a row!\n'
                    f'What anarchy that would be..')
    else:
        story_str = ' '.join(cont[:3])
        add_story_element(session, story_str, mesg.author, curr_story_id)
        await client.add_reaction(mesg, '\U0001f4be')
        response = None

    session.commit()
    return response


@Command(['currentstory', 'printstory', 'cs'], category='Games')
@channel_whitelist(['storywriting'])
async def print_current_story(*args, **_kwargs):
    ''' Print the story that the creative masterminds are currently writing. '''
    session = args[3]()
    curr_story = session.query(StoryElement)\
        .order_by(StoryElement.created_at.desc()).first()

    if not curr_story:
        return 'No story yet'
    else:
        curr_story_id = curr_story.story_id

    return format_story(get_story(session, curr_story_id))


@Command(['endstory', 'finishstory'], category='Games')
@role_whitelist(['Admin', 'Moderator'])
async def end_current_story(cont, mesg, client, sessionmaker, *_args, **_kwargs):
    ''' Ends the current story and save it under the name specified (Moderator only). '''
    session = sessionmaker()

    curr_story = session.query(StoryElement)\
        .order_by(StoryElement.created_at.desc()).first()

    if not curr_story:
        LOGGER.info(
            '%s tried to save a story but no story elements were found',
            mesg.author.mention
        )
        return 'No story to save.'

    current_story_id = curr_story.story_id

    story = get_story(session, current_story_id)
    story = format_story(story)
    storyname = ''.join(cont)

    if not storyname:
        return 'You can\'t save a story without a name!'

    save_story(story, storyname)

    add_story_element(session, '', mesg.author, current_story_id + 1)
    session.commit()

    storypost = f'{storyname}\n{story}'
    await post_story(storypost, mesg.server, client)
    return f'Story saved as \'{storyname}\'.'


@Command(['openstory', 'loadstory'], hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def load_story(cont, *_args, **_kwargs):
    ''' Loads a previously ended story by name (Moderator only). '''
    storyname = ''.join(cont)
    if not storyname:
        return 'You have to enter a story name'

    return print_story(storyname)


@Command(['storyundo', 'undostory'], hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def undo_story(cont, mesg, client, sessionmaker, *_args, **_kwargs):
    ''' Deltetes the last x messages from the database (Moderator only). '''
    session = sessionmaker()

    if cont:
        try:
            x = int(cont[0])
        except ValueError:
            return 'Could not parse value, did nothing.'
    else:
        x = 1

    curr_story = session.query(StoryElement) \
        .order_by(StoryElement.created_at.desc()).first()

    s_id = curr_story.story_id

    curr_selection = session.query(StoryElement)\
        .filter(StoryElement.story_id == s_id)\
        .order_by(StoryElement.created_at.desc())[:x]

    for entry in curr_selection:
        session.delete(entry)

    await client.add_reaction(mesg, '\U000023ea')
    session.commit()

    return None


def save_story(story, name):
    ''' Saves a story to a txt file in the Stories folder. '''
    fname = f'{name.lower()}.txt'
    fpath = os.path.join('Stories', fname)

    with open(fpath, 'a') as file:
        file.write(story)

    return None


def print_story(name):
    ''' Get's a saved story from file and returns the string. '''
    fname = f'{name.lower()}.txt'
    fpath = os.path.join('Stories', fname)

    if not os.path.isfile(fpath):
        return 'This story doesn\'t exist.'

    with open(fpath, 'r') as file:
        string = file.read()

    return string


def format_story(string):
    ''' Formats a string text to include endlines after "." and strip whitespaces from beginning and end. '''
    string = string.strip(' \t\n\r')
    string = string.replace('. ', '.\n')
    return string


def get_story(session, story_id):
    ''' Returns a string containing the story with a specific id. '''
    story_segs = session.query(StoryElement).filter(StoryElement.story_id == story_id) \
        .order_by(StoryElement.created_at.asc())

    story = ' '.join(s[0] for s in story_segs.values('story_string'))
    return story

def add_story_element(session, string, author, story):
    ''' Add a database entry for the new story. '''
    LOGGER.debug(
        'Added "%s" to the story %s, committed by %s',
        string, story, author.id
    )

    author_id = author.id
    session.add(StoryElement(
        story_string=string,
        author=author_id,
        story_id=story
    ))

async def post_story(story, server, client):
    ''' Have the Client post the bot to the "stories" channel if it exists. '''
    channel_list = server.channels
    for channel in channel_list:
        if channel.name.lower() == "stories":
            response_channel = channel

    if not channel:
        return
    return await client.send_message(response_channel, story)

