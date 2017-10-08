'''
Provides commands related to WolframAlpha.
'''
import os
import urllib.parse

import wolframalpha

from stickord.registry import get_easy_logger, Command


LOGGER = get_easy_logger('commands.wolframalpha')

if not os.environ.get('WOLFRAMALPHA_TOKEN', ''):
    LOGGER.warning('No WA token set, killing command.')
    LOGGER.warning('Get a free token at '
                   'https://developer.wolframalpha.com/portal/apisignup.html')
    WA_CLIENT = None
else:
    WA_CLIENT = wolframalpha.Client(os.environ['WOLFRAMALPHA_TOKEN'])

@Command(['calc', 'calculate', 'watis'])
async def wolframalpha_cmd(cont, _mesg):
    ''' Send a query to WolframAlpha. '''
    if not WA_CLIENT:
        return 'WolframAlpha support not set up.'

    query = ' '.join(cont)
    res = WA_CLIENT.query(query)

    results = [p.text for p in res.pods
               if p.title in ('Result', 'Value', 'Decimal approximation',
                              'Exact result')]

    if not results:
        results = ["No results or we don't understand them."]

    response = '\n'.join(results)
    response += '\nLink: https://wolframalpha.com/input/?i={}'.format(
        urllib.parse.quote(query).replace('%20', '+'))

    return response
