'''
Imports all modules in this directory, which registers the commands.
'''
import os.path
import importlib

from stickord.helpers.logging import get_easy_logger


LOGGER = get_easy_logger('commands.loader')

def load_plugins():
    '''
    Import all python files contained in this directory.
    '''
    root = os.path.dirname(__file__)
    LOGGER.info('Loading commands from %s', root)

    for dummy, dummy, filenames in os.walk(root):
        pythonfiles = [f for f in filenames if f.endswith('.py')]
        for codefile in pythonfiles:
            modulename = codefile[:-3] # Strip '.py'
            LOGGER.info('Loading module %s', modulename)

            try:
                # Same effect as doing `import stickord.commands.modulename`
                importlib.import_module(f'.{modulename}', package=__name__)
                LOGGER.debug('%s loaded.', modulename)

            except (NameError, SyntaxError) as ex:
                LOGGER.error('Could not load %s!', modulename)
                LOGGER.exception(ex)
