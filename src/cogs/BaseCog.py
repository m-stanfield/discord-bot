from typing import TYPE_CHECKING
from discord.client import Client
import discord
import asyncio
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
        self.bot: DiscordBot = bot

    @slash_command()
    async def inspire(self, ctx:ApplicationContext, member: discord.Member | None = None):
        output = ""
        if isinstance(member, discord.Member):
            output += utils.memberToMentionString(member=member)
            output += "\n"
        output += inspirobot.generate().url
        await self.bot.addMethodToQueue(ctx.respond,output)

    @slash_command()
    async def roll(self, ctx:ApplicationContext, roll_string=""):
        '''Rolls dice. !roll <dice string>. Dice string exmaple: 1d20 -4d2 + 8 -2d2'''
        await self.bot.addMethodToQueue(ctx.respond, utils.roll_dice(roll_string))
         

