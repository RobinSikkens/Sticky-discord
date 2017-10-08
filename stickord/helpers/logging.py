'''
Contains helper code related to logging.
'''
import logging

import requests


def get_easy_logger(name, level=None):
    ''' Create a logger with the given name and optionally a level. '''
    result = logging.getLogger(name)
    if level:
        result.setLevel(level)
    return result

class DiscordWebhookHandler(logging.Handler):
    ''' Logging handler that emits passed messages to a Discord webhook using
    JSON formatting. '''

    def __init__(self, webhook, *args, **kwargs):
        ''' Store parameters. '''
        self.webhook = webhook
        super().__init__(*args, **kwargs)

    level_emoji = {
        logging.DEBUG: ':bug:',
        logging.INFO: ':information_source:',
        logging.WARNING: ':warning:',
        logging.ERROR: ':no_entry_sign:',
        logging.CRITICAL: ':exclamation:'
    }
    ''' What emoji is used for what level. '''

    def mapLogRecord(self, record): # pylint: disable=invalid-name
        ''' Map log record to JSON dict to send, as in HTTPHandler. '''
        level = record.levelname
        emoji = self.level_emoji[record.levelno]
        exc_info = record.exc_info

        if not exc_info:
            logmsg = record.msg % record.args
            message = f'{emoji} {level}: {logmsg}'
        else:
            message = (f'{emoji} {level}:\n'
                       f'```\n{record.exc_text}\n```')
        return {'content': message}

    def emit(self, record):
        ''' Send data via POST-request. '''
        data = self.mapLogRecord(record)
        requests.post(self.webhook, json=data)
