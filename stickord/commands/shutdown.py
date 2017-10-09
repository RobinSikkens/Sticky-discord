'''
Provides command to shut down bot in case of trouble.
'''
from stickord.registry import get_easy_logger, Command, whitelist_only


LOGGER = get_easy_logger('commands.shutdown')

@Command('botshutdown', hidden=True)
@whitelist_only(['Admin', 'Moderator'])
async def shutdown(_cont, mesg, client, *_args, **_kwargs):
    ''' Shutdown bot by sending SIGINT. '''
    LOGGER.critical('Shutdown initiated by %s', mesg.author.mention)
    await client.logout()
    client.loop.stop()
    return None
