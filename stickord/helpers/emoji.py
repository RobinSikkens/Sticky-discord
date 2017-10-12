'''
Provides coder-friendly emoji access.
'''
import enum

@enum.unique
class Emoji(enum.Enum):
    ''' Enum with various used emoji. '''
    Cookie = '\U0001f36a'
    Floppy = '\U0001f4be'
    OkHand = '\U0001f44c'
