from typing import TYPE_CHECKING
from discord.client import Client
import discord
import asyncio
from src.database.schema import NicknamesTable
from src.database import BaseDataBase
from src.Settings import Settings
from discord.ext import commands
from discord.ext.commands import Bot
import time
from discord.commands import slash_command, ApplicationContext
from src.logger import Logger
import inspirobot

import src.Utilities as utils

import numpy as np


logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class BaseCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Loading Admin Cog")

        self.bot: DiscordBot = bot


    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        '''Shuts bot down. Only usable by bot owner'''
        logger.info("Shutting down bot")
        await ctx.message.delete()
        await self.bot.setRunStatus(status=False)
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def restart(self,ctx):
        '''Restarts bot. Only usable by bot owner'''
        logger.info("Restarting bot")

        await ctx.message.delete()
        await self.bot.setRunStatus(status=True)
        await self.bot.close()
