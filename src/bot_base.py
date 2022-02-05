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
import logging

import discord
from discord.ext import commands
import threading as th

from cogs.cog_generators.image_cog_gen import generate_images
generate_images()

from cogs.base_cog import base
from cogs.audio_cog import audio
from cogs.image_cog import images
from cogs.user_cog import users
from cogs.guild_cog import guilds
from cogs.general_cog import general

import functions.profile_fun as pf
from functions.logging import setup_logging


logger = logging.getLogger(__name__)

        
async def run(TOKENS):

    credentials = {"user": TOKENS["SQL_USER"], 
                   "password": TOKENS["SQL_PASS"],
                   "database": TOKENS["SQL_DB"],
                   "host": TOKENS["host"]}
    db = await asyncpg.create_pool(**credentials)

    # Example create table code, you'll probably change it to suit you

    intents = discord.Intents.all()

    bot = Bot( command_prefix=commands.when_mentioned_or("!"),
                        description='Introductiongeneral discord bot',
                        intents=intents,db=db)
    #adding cogs to bot
    bot.add_cog(base(bot))
    bot.add_cog(users(bot))
    bot.add_cog(general(bot))
    bot.add_cog(audio(bot))
    bot.add_cog(images(bot))
    bot.add_cog(guilds(bot))

    logger.info(f'Using Database: {bot.db}')
    try:
        await bot.start(TOKENS["DISCORD_TOKEN"])
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Exiting Program")
        await db.close()
        await bot.logout()



class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=kwargs.pop("command_prefix"),
            intents=kwargs.pop("intents")
        )

        self.db = kwargs.pop("db")

if __name__ == "__main__":
    

    load_dotenv()


    
    
    parser = argparse.ArgumentParser(description="Sets runtime settings for discord bot")
    parser.add_argument('--TEST_MODE', type=int,default=0)
    parser.add_argument('--UPDATE_ALL',type=int,default=1)
    parser.add_argument('--DISABLE_WAKEUP',type=int,default=0)
    parser.add_argument('--TEST_LOAD', type=int, default=0)
    parser.add_argument('--LOG', type=int, default=0)
    args = parser.parse_args()

    

    setup_logging(mode=args.LOG)
    
    logger.info("~~~~~~~~NEW LOG~~~~~~~~")
    logger.info("Discord Bot initialized")


    env = ["DISCORD_TOKEN","SQL_USER","SQL_PASS","SQL_DB","host","LOG_CFG"]
    TOKENS = {}
    
    for key in env:
        try:
            TOKENS[key] = os.getenv(key)
        except KeyError:
            logger.error(f"Invalid enrivoment key on load: {key}")

    

    run_state = True
    if args.TEST_LOAD == 1:
        logger.info("Load was successful. Due to test load being enabled program will now exit.")
        run_state = False

    while run_state:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(TOKENS))
    logger.info("Program Closed")
