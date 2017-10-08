'''
Provides commands to the xkcd system
'''
from stickord.helpers.xkcd_api import get_random, get_by_id, print_comic, get_recent
from stickord.registry import Command

@Command('xkcd', category='xkcd')
async def get_comic(cont, _mesg):
    ''' Search for a comic by id, if no id is provided it will post a random comic. '''
    if cont:
        comic_id = int(cont[0])
        comic = await get_by_id(comic_id)
        return await print_comic(comic)

    comic = await get_random()
    return await print_comic(comic)

@Command('newxkcd', category='xkcd')
async def get_latest_comic(_cont, _mesg):
    ''' Posts the latest xkcd comic. '''
    return await get_recent()
