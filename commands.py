import discord
import pickle
import os
import random
from functools import wraps
from sticky_api import StickyAPI as api


class BotCommands:
    @staticmethod
    @is_administrator
    async def help_message(cont, mesg):
        return "this is a help message"

    @staticmethod
    async def get_activity(cont, mesg):
        activity_list = await api.get_activities()
        if len(cont) > 0:
            for act in activity_list:
                if ' '.join(cont).lower() in act["name"].lower():
                    return api.print_activity(act)
            return 'Kon geen activiteit vinden met de naam: \"' + ' '.join(cont) + '\"'
        activity = activity_list[0]
        return api.print_activity(activity)

    @staticmethod
    async def list_activities(cont, mesg):
        activity_list = await api.get_activities()
        ret = "Dit zijn alle aankomende activiteiten:"
        for act in activity_list:
            ret = ret + "\n" + act["name"]
        return ret

    @staticmethod
    async def add_quote(cont, mesg):
        quote = ' '.join(cont)

        if not os.path.isfile("quote_file.pk1"):
            quote_list = []
        else:
            with open("quote_file.pk1", "rb") as file:
                quote_list = pickle.load(file)

        quote_list.append(quote)

        with open("quote_file.pk1", "wb") as file:
            pickle.dump(quote_list, file)

        return "Saved quote to file."


    @staticmethod
    async def print_quote(cont, mesg):
        if not os.path.isfile("quote_file.pk1"):
            return "No quotes saved."

        with open("quote_file.pk1", "rb") as file:
            quote_list = pickle.load(file)

            if len(cont) == 0:
                quote = random.choice(quote_list)
            else:
                quote = discord.utils.find(lambda s: ' '.join(cont.lower()) in s.lower(), quote_list)

            return quote


def is_administrator(func):
    @wraps(func)
    def newfunc(cont, mesg):
        if mesg.author.permissions_in(mesg.channel).administrator:
            return func(cont, mesg)
        return not_authorized()

    return newfunc


async def not_authorized():
    return "You are not authorized to use this command"
