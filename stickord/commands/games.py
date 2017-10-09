import discord
from stickord.registry import Command

@Command(['tellen', 'tel'], category='Games')
async def counting(cont, mesg, client, *args, **kwargs):
    ''' Allows  users to play the counting game. The command should be entered with the number exactly 1 higher than the last time the command was entered. Cannot submit a number twice in a row.'''
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



