'''
Contains code that allows the user to generate memes through the imgflip
'''

from stickord.helpers.imgflip_api import generate_meme, print_meme
from stickord.registry import Command

@Command('meme')
async def make_meme(cont, *_args, **_kwargs):
    ''' Make a meme. '''
    if not cont  or len(cont) < 3:
        return 'I don\'t know what to do here'

    id = cont[0]
    content = ' '.join(cont[1:])
    content = content.split(';')
    text_up = content[0]
    text_bot = content[1]

    meme = await generate_meme(id, text_up, text_bot)
    return await print_meme(meme)
