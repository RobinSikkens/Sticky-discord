from setuptools import setup

from stickord import VERSION


setup(
    name='stickord',
    version=VERSION,
    description='A bot that talks to the Sticky API, written for Discord',
    url='https://github.com/RobinSikkens/Sticky-discord',
    install_requires=[
        'SQLAlchemy',
        'alembic',
        'python-dotenv',
        'discord.py',
        'asyncio',
        'python-dateutil',
        'requests',
        'wolframalpha',
    ],
    packages=['stickord'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'runbot=stickord.bot:main'
        ]
    }
)
