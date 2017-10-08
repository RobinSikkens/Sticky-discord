'''
Provides !help by inspecting the registered commands in
stickord.registry.COMMAND_CATEGORIES.
'''
from inspect import cleandoc

from stickord.registry import Command, COMMAND_CATEGORIES


@Command(['help', 'commands', 'watisdit'])
async def command_help(_cont, _mesg):
    ''' Show this help message. '''
    lines = []
    cats = COMMAND_CATEGORIES.keys()

    for cat in cats:
        category = cat or 'Algemeen' # Bij None of niet opgegeven
        lines.append(f'**{category}**:')

        for command in COMMAND_CATEGORIES[cat]:
            main, aliases, func = command

            if func.__doc__:
                helpmsg = cleandoc(func.__doc__)
            else:
                helpmsg = 'No help available.'

            if aliases:
                name = f"`!{main}` (`{'`, `'.join(aliases)}`)"
            else:
                name = f"`!{main}`"

            lines.append(f"{name}: {helpmsg}")

    return "\n".join(lines)
