import requests
import json


class StickyAPI:
    @staticmethod
    async def get_activities():
        response = requests.get("https://koala.svsticky.nl/api/activities")
        return json.loads(response.text)
