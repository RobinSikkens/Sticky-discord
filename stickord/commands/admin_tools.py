'''
Contains some Moderator and Admin only commands that are useful when moderating.
'''
from datetime import datetime, timedelta
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
            async for m in client.logs_from(mesg.channel, limit=amount):
                if datetime.now() - m.timestamp > timedelta(days=14):
                    LOGGER.warning(
                        'Could not delete some messages, '
                        'message might be older than 14 days. Timestamp: %s',
                        m.timestamp
                    )
                    break
                messages.append(m)

            # As bulk deletion only works with more than 2 messages catch exception
            if amount <= 2:
                for message in messages:
                    await client.delete_message(message)
            else:
                await client.delete_messages(messages)
            LOGGER.info(f'Deleted {amount} messages from #{mesg.channel} by order of {mesg.author}')
            return None
        except ValueError:
            pass
    return 'You have to enter the number of messages to be deleted.'


@Command('forceprune', category='Tools', hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def force_prune_message(cont, mesg, client, *_args, **_kwargs):
    '''
    Prunes a channel whithout using bulkdelete (Moderator only).
    May be used to delete messages over 14 days old.
    Might be significantly slower than the regular prune command.
    '''
    if cont:
        try:
            messages = []
            amount = int(cont[0]) + 1

            async for m in client.logs_from(mesg.channel, limit=amount):
                messages.append(m)

            for message in messages:
                await client.delete_message(message)

            LOGGER.info(f'Force-deleted {amount} messages from #{mesg.channel} by order of {mesg.author}')
            return None

        except ValueError:
            pass

    return 'You have to enter the number of messages to be deleted.'


@Command(['exprune', 'excludeprune'], category='Tools', hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def exclusive_prune_messages(cont, mesg, client, *_args, **_kwargs):
    '''
    Deletes up to x messages from the channel this command is posted in,
    skips messages that begin with string specified (Moderator only).
    x does not include the command itself.
    Can only delete messages from the last 14 days, up to 100 (including invocation).
    USAGE: `!exprune 99 !as`
    '''
    if cont:
        try:
            messages = []
            amount = int(cont[0]) + 1
            exclude = ' '.join(cont[1:])

            if amount > 100:
                return 'Can only delete a maximum of 99 messages at a time.'
            async for m in client.logs_from(mesg.channel, limit=amount):
                if datetime.now() - m.timestamp > timedelta(days=14):
                    LOGGER.warning(
                        'Could not delete some messages, '
                        'message might be older than 14 days. Timestamp: %s',
                        m.timestamp
                    )
                    break

                if not m.content.startswith(exclude):
                    messages.append(m)

            delcount = len(messages)

            # As bulk deletion only works with more than 2 messages catch exception
            if amount <= 2:
                for message in messages:
                    await client.delete_message(message)
            else:
                await client.delete_messages(messages)
            LOGGER.info(f'Deleted {delcount} messages from #{mesg.channel} by order of {mesg.author}')
            return None
        except ValueError:
            pass
    return 'You have to enter the number of messages to be deleted.'


@Command(['inprune', 'includeprune'], category='Tools', hidden=True)
@role_whitelist(['Admin', 'Moderator'])
async def inclusive_prune_messages(cont, mesg, client, *_args, **_kwargs):
    '''
    Deletes up to x messages from the channel this command is posted in
    if the message begins with string specified (Moderator only).
    x does not include the command itself.
    Can only delete messages from the last 14 days, up to 100 (including invocation).
    USAGE: `!inprune 99 !help`
    '''
    if cont:
        try:
            messages = []
            amount = int(cont[0]) + 1
            include = ' '.join(cont[1:])

            if amount > 100:
                return 'Can only delete a maximum of 99 messages at a time.'
            async for m in client.logs_from(mesg.channel, limit=amount):
                if datetime.now() - m.timestamp > timedelta(days=14):
                    LOGGER.warning(
                        'Could not delete some messages, '
                        'message might be older than 14 days. Timestamp: %s',
                        m.timestamp
                    )
                    break

                if m.content.startswith(include):
                    messages.append(m)

            delcount = len(messages)

            # As bulk deletion only works with more than 2 messages catch exception
            if amount <= 2:
                for message in messages:
                    await client.delete_message(message)
            else:
                await client.delete_messages(messages)
            LOGGER.info(f'Deleted {delcount} messages from #{mesg.channel} by order of {mesg.author}')
            return None
        except ValueError:
            pass
    return 'You have to enter the number of messages to be deleted.'
