import asyncio
from dotenv import load_dotenv
import h5py
import time
from datetime import datetime
import argparse
import sys
import os
import numpy as np
import glob
import asyncpg

import discord
from discord.ext import commands




sys.path.append('cogs')
from base_cog import base
from audio_cog import audio
from image_cog import images
from user_cog import users
from guild_cog import guilds
from general_cog import general

sys.path.append('functions')
import profile_fun as pf
#from profile_fun import load_defaults

load_dotenv()
parser = argparse.ArgumentParser(description="Sets runtime settings for discord bot")
parser.add_argument('--TEST_MODE', type=int,default=0)
parser.add_argument('--UPDATE_ALL',type=int,default=1)
parser.add_argument('--DISABLE_WAKEUP',type=int,default=0)

args = parser.parse_args()

#grant all privileges on database server_settings to discordbot;
env = ['DISCORD_TOKEN','SQL_USER','SQL_PASS','SQL_DB','host']

TOKENS = {}

for key in env:
    TOKENS[key] = os.getenv(key)

async def run(TOKENS):

    credentials = {"user": TOKENS["SQL_USER"], "password": TOKENS["SQL_PASS"], "database": TOKENS["SQL_DB"], "host": TOKENS["host"]}
    db = await asyncpg.create_pool(**credentials)

    # Example create table code, you'll probably change it to suit you

    intents = discord.Intents.all()

    bot = Bot( command_prefix=commands.when_mentioned_or("!"),
                        description='Introductiongeneral discord bot',
                        intents=intents,db=db)



    # TODO: Update existing profiles to ensure all fields are satisfied




    # TODO:


    bot.add_cog(base(bot))
    bot.add_cog(users(bot))
    bot.add_cog(general(bot))
    bot.add_cog(audio(bot))
    bot.add_cog(images(bot))
    bot.add_cog(guilds(bot))

    print('Using Database: ',bot.db)
    try:
        await bot.start(TOKENS["DISCORD_TOKEN"])
    except KeyboardInterrupt:
        await db.close()
        print('exiting loop')
        await bot.logout()

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=kwargs.pop("command_prefix"),
            intents=kwargs.pop("intents")
        )

        self.db = kwargs.pop("db")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(TOKENS))