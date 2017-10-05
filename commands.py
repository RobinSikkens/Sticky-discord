import discord
import dateutil.parser as dateparser
from sticky_api import StickyAPI as api


class BotCommands:
    @staticmethod
    async def help_message(cont, mesg):
        return "this is a help message"

    @staticmethod
    async def get_activity(cont, mesg):
        activity_list = await api.get_activities()
        for act in activity_list:
            if len(cont) == 0:
                break
            if act["name"].lower() == ' '.join(cont.lower()):
                return BotCommands.print_activity(act)
        activity = activity_list[0]
        return BotCommands.print_activity(activity)

    @staticmethod
    async def list_activities(cont, mesg):
        activity_list = await api.get_activities()
        ret = "Dit zijn alle aankomende activiteiten:"
        for act in activity_list:
            ret = ret + "\n" + act["name"]
        return ret


    @staticmethod
    def print_activity(act):
        embed = discord.Embed(color=discord.Colour(0xce2029))

        date_begin = dateparser.parse(act["start_date"])
        date_end = dateparser.parse(act["end_date"])

        if date_begin.date() != date_end.date():
            embed.add_field(name=act["name"], value=f'**Locatie**: {act["location"]}\n**Inschrijvingen**: '
                                                    f'{act["participant_counter"]}\n**Begin**: '
                                                    f'{date_begin.date()}: {date_begin.time()}\n**Eind**: '
                                                    f'{date_end.date()}: {date_end.time()}')
        else:
            embed.add_field(name=act["name"], value=f'**Locatie**: {act["location"]}\n**Inschrijvingen**: '
                                                    f'{act["participant_counter"]}\n**Datum**: '
                                                    f'{date_begin.date()}\n**Tijd**: {date_begin.time()} - '
                                                    f'{date_end.time()}')
        embed.set_image(url=act["poster"])
        return embed
