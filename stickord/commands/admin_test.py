'''
Test for hidden, admin-only commands.
'''
from stickord.registry import Command, role_whitelist


@Command('supersecret', hidden=True)
@role_whitelist(["Admin", "Moderator"])
async def admintest(*_args, **_kwargs):
    ''' Admintest. '''
    return ':tada: Jij zit bij de koele kids klup! :sunglasses: :sunglasses:'

@Command('crashme', hidden=True)
@role_whitelist(["Admin", "Moderator"])
async def crashtest(*_args, **_kwargs):
    ''' Test command killing on error. '''
    raise NotImplementedError
