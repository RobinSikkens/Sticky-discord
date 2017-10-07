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
            prts = f'\n**Inschrijvingen**: {act["participant_counter"]}'
        if date_begin.date() != date_end.date():
            embed.add_field(name=act["name"], value=f'**Locatie**: {act["location"]}{prts}\n**Begin**: '
                                                    f'{date_begin.date()}: {date_begin.time()}\n**Eind**: '
                                                    f'{date_end.date()}: {date_end.time()}')
        else:
            embed.add_field(name=act["name"], value=f'**Locatie**: {act["location"]}{prts}\n**Datum**: '
                                                    f'{date_begin.date()}\n**Tijd**: {date_begin.time()} - '
                                                    f'{date_end.time()}')
        embed.set_image(url=act["poster"])
        return embed
