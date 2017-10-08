'''
Contains code needed to register commands.
'''
from collections import defaultdict
from functools import wraps

from stickord.helpers.logging import get_easy_logger


class RegisteringDecorator(object):
    '''
    Generalized decorator for registering case-insensitive commands in a dict.

    Must be overridden to specify the target dict.
    '''
    target_dict = {}

    def __init__(self, name):
        ''' Register command's name or list of names. '''
        self.name = name

    def __call__(self, func):
        ''' Register callable under name. '''

        # If name is an iterable, it is a list and we use all names.
        if isinstance(self.name, list):
            for item in self.name:
                self.target_dict[item.upper()] = func

        else:
            self.target_dict[self.name.upper()] = func

        LOGGER.debug('Registered %s', self.name)
        return func

COMMAND_DICT = {}
''' Maps uppercase commands to callables. '''
COMMAND_CATEGORIES = defaultdict(list)
''' Maps categories to lists of (name, aliases, callable) to generate help. '''

class Command(RegisteringDecorator):
    ''' Decorator for functions that are available as a command, and need to be
    registered in the help. '''

    target_dict = COMMAND_DICT
    help_dict = COMMAND_CATEGORIES

    def __init__(self, name, category=None, hidden=False):
        ''' Store parameters and call supermethod. '''
        self.hidden = hidden
        self.category = category

        super().__init__(name)

    def __call__(self, func):
        ''' Register command in help and call supermethod. '''
        if not self.hidden:
            if isinstance(self.name, str):
                # The command has no aliases.
                self.help_dict[self.category].append(
                    (self.name, None, func)
                )
            else:
                # First name is the canonical name, rest are aliases.
                self.help_dict[self.category].append(
                    (self.name[0], self.name[1:], func)
                )
        return super().__call__(func)

def admin_only(func):
    ''' Helper function to only allow Admins to use command. '''
    @wraps(func)
    def newfunc(cont, mesg): # pylint: disable=missing-docstring
        if mesg.author.permissions_in(mesg.channel).administrator:
            return func(cont, mesg)
        return not_authorized()

    # Make help available
    newfunc.__doc__ = func.__doc__

    return newfunc

def not_authorized():
    ''' Warning for plebeians. '''
    return "You are not authorized to use this command."

class CommandNotFoundError(Exception):
    ''' Custom Exception to signal that a command does not exist. '''
    pass

async def safe_call(target_dict, key, *args, **kwargs):
    '''
    Wrapper to 'safely' call a function and disable the command if an exception
    occurs. A reload of the commands or restart of the bot is needed to
    re-enable the command.
    '''

    fname = key.upper()
    if fname not in target_dict:
        raise CommandNotFoundError(f'Command does not exist: %s', fname)

    try:
        return await target_dict[key.upper()](*args, **kwargs)
    except (NameError, TypeError):
        raise
    except Exception as ex: # pylint: disable=broad-except
        # Disable command
        del target_dict[key]

        LOGGER.error('Command %s disabled')
        LOGGER.exception(ex)

        return "Something broke, command disabled."

LOGGER = get_easy_logger('registry')
