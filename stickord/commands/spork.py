'''
Commands involving some form of randomness.
*holds up spork*
'''
import random
from stickord.registry import Command

@Command("8ball", category="Spork")
async def eightball(_cont, mesg, *_args, **_kwargs):
    ''' The wise magic 8-ball will know what to do with whatever query you might have. '''
    with open("eightball_responses.txt", "r") as file:
        line = random.choice(file.readlines())
        mention = mesg.author.mention
        response = f"{mention}, the magic 8-ball has spoken!: {line}"
    return response

@Command(['flip', 'coinflip', 'muntje'], category="Spork")
async def flipcoin(*_args, **_kwargs):
    '''Flip a coin: Heads, Tails? Some fine dispute settling here'''
    return random.choice(['Heads', 'Tails'])
