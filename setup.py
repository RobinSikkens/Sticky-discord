from setuptools import setup

from stickord import VERSION


setup(
    name='stickord',
    version=VERSION,
    description='A bot that talks to the Sticky API, written for Discord',
    url='https://github.com/RobinSikkens/Sticky-discord',
    install_requires=[
        'python-dotenv',
        'discord.py',
        'asyncio',
        'python-dateutil',
        'requests',
    ],
    packages=['stickord'],
    zip_safe=False
)
