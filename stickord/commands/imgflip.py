'''
Contains code that allows the user to generate memes through the imgflip
'''

from stickord.helpers.imgflip_api import generate_meme, print_meme, get_meme_id
from stickord.registry import Command

@Command('meme')
async def make_meme(cont, *_args, **_kwargs):
    ''' Make a meme. '''
    if not cont  or len(cont) < 3:
        return 'I don\'t know what to do here'

    content = ' '.join(cont[:])
    content = content.split(';')
    try:
        id = int(content[0])
    except:
        id = get_meme_id(''.join(e for e in content[0].lower() if e.isalnum()))

    if len(content) >= 2:
        text_up = content[1]
    else:
        text_up = ''

    if len(content) >= 3:
        text_bot = content[2]
    else:
        text_bot = ''

    meme = await generate_meme(id, text_up, text_bot)
    return await print_meme(meme)
