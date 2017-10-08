'''
Provides commands related to Koala.
'''
from stickord.helpers.sticky_api import get_activities, print_activity
from stickord.registry import Command


@Command('activiteit', category='Sticky')
async def get_activity(cont, _mesg):
    ''' Search for an activity by name, or print the first. '''
    acts = await get_activities()

    if cont:
        query = ' '.join(cont).lower()
        for act in acts:
            if query in act['name'].lower():
                return await print_activity(act)

        return f'Kon geen activiteit vinden met de naam "{query}"'

    act = acts[0]
    return await print_activity(act)

@Command('activiteiten', category='Sticky')
async def list_activities(_cont, _mesg):
    ''' List all upcoming activities. '''
    acts = await get_activities()
    lines = []

    lines.append("Dit zijn alle aankomende activiteiten:")

    for act in acts:
        lines.append(f"- {act['name']}")

    return '\n'.join(lines)
