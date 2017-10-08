import random
from stickord.registry import Command

@Command("8ball", category="Spork")
async def eightball(cont, mesg):
    '''The wise magic 8-ball will know what to do with whatever query you might have'''
    with open("eightball_responses.txt", "r") as f:
        response = random.choice(f.readlines())
    return response

@Command(['flip', 'coinflip', 'muntje'], category="Spork")
async def flipcoin(cont, mesg):
    '''Flip a coin: Heads, Tails? Some fine dispute settling here'''
    return random.choice(['Heads', 'Tails'])