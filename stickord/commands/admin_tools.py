'''
Contains some Moderator and Admin only commands that are useful when moderating.
'''
from stickord.registry import Command, get_easy_logger, role_whitelist

LOGGER = get_easy_logger('commands.admin_tools')


@Command('prune', category='Tools', hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def prune_messages(cont, mesg, client, *_args, **_kwargs):
    '''
    Deletes x messages from the channel this command is posted in (Moderator only).
    x does not include the command itself.
    Can only delete messages from the last 14 days, up to 100 (including invocation). 
    '''
    if cont:
        try:
            messages = []
            amount = int(cont[0]) + 1
            if amount > 100:
                return 'Can only delete a maximum of 99 messages at a time.'
            async for m in client.logs_form(mesg.channel, limit=amount):
                messages.append(m)
            await client.delete_messages(messages)
            LOGGER.log(f'Deleted {amount} messaged from {mesg.channel} by order of {mesg.author}')
            return None
        except ValueError:
            pass
    return 'You have to enter the number of messages to be deleted.'
