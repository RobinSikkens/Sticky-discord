'''
Test for hidden, admin-only command.
'''
from stickord.registry import admin_only, Command


@Command('supersecret', hidden=True)
@admin_only
async def admintest(_cont, _mesg):
    ''' Admintest. '''
    return ':tada: Jij zit bij de koele kids klup! :sunglasses: :sunglasses:'
