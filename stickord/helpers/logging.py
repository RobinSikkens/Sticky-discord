'''
Contains helper code related to logging.
'''
import logging


def get_easy_logger(name, level=None):
    ''' Create a logger with the given name and optionally a level. '''
    result = logging.getLogger(name)
    if level:
        result.setLevel(level)
    return result
