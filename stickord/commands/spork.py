import random
from stickord.registry import Command

@Command("8ball")
async def eightball(cont, mesg):
    with open("eightball_responses.txt", "r") as f:
        response = random.choice(f.readlines())
    return response

@Command(['flip', 'coinflip', 'muntje'])
async def flipcoin(cont, mesg):
    return random.choice(['Heads', 'Tails'])