import requests
import json
import discord
import dateutil.parser as dateparser


class StickyAPI:
    @staticmethod
    async def get_activities():
        response = requests.get("https://koala.svsticky.nl/api/activities")
        return json.loads(response.text)

    @staticmethod
    def print_activity(act):
        embed = discord.Embed(color=discord.Colour(0xce2029))

        date_begin = dateparser.parse(act["start_date"])
        date_end = dateparser.parse(act["end_date"])

        if "partcipant_counter" not in act:
            prts = ""
        else:
            prts = '\n**Inschrijvingen**: %(act["participant_counter"])s' % locals()
        if date_begin.date() != date_end.date():
            embed.add_field(name=act["name"], value='**Locatie**: %(act["location"])s%(prts)s\n**Begin**: '
                                                    '%(date_begin.date())s: %(date_begin.time())s\n**Eind**: '
                                                    '%(date_end.date())s: %(date_end.time())s') % locals()
        else:
            embed.add_field(name=act["name"], value='**Locatie**: %(act["location"])s%(prts)s\n**Datum**: '
                                                    '%(date_begin.date())s\n**Tijd**: %(date_begin.time())s - '
                                                    '%(date_end.time())s') % locals()
        embed.set_image(url=act["poster"])
        return embed
