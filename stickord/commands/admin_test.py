'''
Test for hidden, admin-only command.
'''
from stickord.registry import admin_only, Command, whitelist_only


@Command('supersecret', hidden=True)
@whitelist_only(["Admin", "Moderator"])
async def admintest(_cont, _mesg):
    ''' Admintest. '''
    return ':tada: Jij zit bij de koele kids klup! :sunglasses: :sunglasses:'

@Command('crashme', hidden=True)
@whitelist_only(["Admin", "Moderator"])
async def crashtest(_cont, _mesg):
    ''' Test command killing on error. '''
    raise NotImplementedError
