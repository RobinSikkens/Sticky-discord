import discord
from stickord.registry import Command

@Command(['tellen', 'tel'])
async def counting(cont, mesg, client, *args, **kwargs):
    count, auth, when = (0, discord.User, None)
    if cont:
        try:
            num = int(cont[0])
            if num != count + 1:
                return f'Whoops, you done goof! you should have entered "{cnt+1}" but you entered "{num}"'
            else if mesg.author.id == auth.id:
                return f'You can\'t submit a number twice in a row! Shame on you {mesg.author.mention}!'
            else:
                #save num
                await client.add_reaction(mesg, '\U0001f44c')
        except ValueError:
            return 'Entered number was not valid.'



